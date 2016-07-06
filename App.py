from WordRelation import *
from FindNearest import *
from Classifier import *
from WordCluster import *

class MainApp():
    def __init__(self, question, keyword):
        self.question = question
        self.keyword = keyword
        classifier = Classifier(self.question)
        self.npf = NPF(self.question)
        self.wc = WordCluster()
        self.wc.generateCluster()
        self.commandList = classifier.CheckInput()
        self.FindNearest()
    def FindNearest(self):
        nearestVerb = self.npf.GetNearest(self.keyword)
        print nearestVerb

if __name__ == '__main__': 
    #question = raw_input();
    question = 'how to describe "beach"'
    keyword = re.findall('"([^"]*)"', question)
    question =  question.replace('\"', '')
    mainApp = MainApp(question, keyword[0])
        
