from WordRelation import *
from FindNearest import *
from Classifier import *
from WordCluster import *

class MainApp():
    def __init__(self, question):

        self.keyword = re.findall('"([^"]*)"', question)[0]
        self.question =  question.replace('\"', '')

        self.classifier = Classifier(self.question)
        self.npf = NPF(self.question)
        self.wcluster = WordCluster()
        self.wrc = WRC()
        
        self.keywordPos = self.wrc.GetKeyPos(self.keyword)

        self.wcluster.generateCluster()
        self.commandList = self.classifier.CheckInput()
        self.FindNearest()
        
        self.GetCommand()
        
    def FindNearest(self):
        #self.wcluster.insertWord('pos', 'v', 'describe')
        nearestVerb = self.npf.GetNearest(self.keyword)
        self.smallest = []
        self.smallest.append(1000)
        self.smallest.append('none')
        for command in self.commandList:
            verbList = self.wcluster.returnCluster(command)['v']
            for verb in verbList:
                level = self.wrc.findLemma(nearestVerb,'v',0, verb) 
                if(level < self.smallest[0]):
                    self.smallest[0] = level
                    self.smallest[1] = command
                print verb
        print nearestVerb

        print self.smallest[0]
        print self.smallest[1]
    def GetCommand(self):
        queryList = []
        commandType = self.smallest[1]
        if commandType == 'pos':
            for pos in self.keywordPos:
                if pos == 'v':
                    queryList.append('adv. ' + self.keyword)
                elif pos == 'n':
                    queryList.append('adj. ' + self.keyword)
        elif commandType == 'anyWord':
            queryList.append('_ _ ' + self.keyword + ' _ _')
        print queryList
        return queryList
        

if __name__ == '__main__': 
    question = 'how to elaborate "house"'
    mainApp = MainApp(question)
        
