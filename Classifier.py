import nltk
import json
from WordRelation import *
from WordCluster import *
from FindNearest import *

class Classifier():
    def __init__(self, question, keyword):
        self.question = question
        self.keyword = keyword
        self.commandList = self.ManageInput()
        self.wrc = WRC()
        self.keywordPos = self.wrc.GetKeyPos(self.keyword[0])
        self.wcluster = WordCluster()
        self.wcluster.generateCluster()
        self.npf = NPF(self.question)
        self.ManageCommandList()
        print self.processedKeyword[0]
        #self.GetCommand()
    
    def ManageInput(self):
        commandList = [];
        if 'how' in self.question.lower() or 'what' in self.question.lower():
            commandList.append('pos')
            commandList.append('anyWord')

        elif len(self.keyword) == 2:
            commandList.append('which')
            commandList.append('optionally')
                
        elif self.question.split(' ')[0] == 'which':
            commandList.append('optionally')
            commandList.append('which')
            commandList.append('similar')
            commandList.append('zero2more')
        return commandList

    def ManageCommandList(self):
        self.queryList = []
        self.processedKeyword = []
        if 'pos' in self.commandList or 'anyWord' in self.commandList:
            self.processedKeyword.append(self.keyword[0])
            closest = self.CalWordRelation()
            commandType = closest['command']
            if commandType == 'pos':
                for pos in self.keywordPos:
                    if pos == 'v':
                        self.queryList.append('adv. ' + self.processedKeyword[0])
                    elif pos == 'n':
                        self.queryList.append('adj. ' + self.processedKeyword[0])
            elif commandType == 'anyWord':
                self.queryList.append('_ _ ' + self.processedKeyword[0] + ' _ _')
        elif 'which' in self.commandList:
            query = self.CompareTwoKey()
            if len(self.processedKeyword) == 1:
                self.queryList.append(query)
            elif len(self.processedKeyword) == 2:
                self.queryList.append(query)

    def CompareTwoKey(self):
        query = ''
        words1 = self.keyword[0].split(' ')
        words2 = self.keyword[1].split(' ')
        if len(words1) > len(words2):
            for word in words1:
                if word not in words2:
                    self.processedKeyword.append(word)
                    query = self.keyword[0].replace(word, '?' + word)
        elif len(words1) < len(words2):
            for word in words2:
                if word not in words1:
                    self.processedKeyword.append(word)
                    query = self.keyword[1].replace(word, '?' + word)
        else:
            for word in words1:
                if word not in words2:
                    self.processedKeyword.append(word)
                    break
            for word in words2:
                if word not in words1:
                    self.processedKeyword.append(word)
                    break
            query = self.keyword[0].replace(self.processedKeyword[0], self.processedKeyword[0] + '/' + self.processedKeyword[1])

        return query
            
        

    def CalWordRelation(self):
        #self.wcluster.insertWord('pos', 'v', 'describe')
        nearestVerb = self.npf.GetNearest(self.keyword[0])
        closest = {'level':1000, 'command':'none'}
        for command in self.commandList:
            verbList = self.wcluster.returnCluster(command)['v']
            for verb in verbList:
                level = self.wrc.FindConnection(nearestVerb,'v',0, verb) 
                if(level < closest['level']):
                    closest['level'] = level
                    closest['command'] = command
        return closest

    def GetQueryList(self):
        print self.queryList
        return self.queryList

if __name__ == "__main__":
    
    question = raw_input()
    CL = Classifier(question)
    print CL.CheckInput()
    
