'''
'''
'''
WRC stands for word relation calculator
'''
from nltk.corpus import wordnet as wn
from nltk.parse.stanford import StanfordParser
import os
import numpy
import re
from WordRelation import *
os.environ['STANFORD_PARSER'] = '../stanford-parser/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = '../stanford-parser/stanford-parser-3.5.2-models.jar' 
dep_parser = StanfordParser(model_path='../stanford-parser/englishPCFG.ser.gz')

class FindNearest():
    def __init__(self, question):
        self.question = question
        self.verbsPosition = []
        self.parsedTree = []
        self.ParseData()
        self.GetVsPosition()
        
    def ParseData(self):
        #print('Parsing.')
        self.questionParsed = dep_parser.raw_parse(self.question)
        for q in self.questionParsed:
            self.parsedTree = q

    def GetVsPosition(self):
        verbsPosition = []
        leaf_values = self.parsedTree.leaves()
        for pairs in self.parsedTree.pos():
            if str(pairs[1])[0] == 'V':
                verbsPosition.append([pairs[0], leaf_values.index(pairs[0])])
        self.verbsPosition = verbsPosition
    def GetNearest(self, keyword):
        leaf_values = []
        leaf_values = self.parsedTree.leaves()
        keywordPos = leaf_values.index('KKEEYYWWOORRDD')
        minimum = 100000
        for pairs in self.verbsPosition:
            if abs(pairs[1] - keywordPos) < abs(minimum - keywordPos):
                minimum = pairs[1]
        if len(self.verbsPosition) == 0:
            return 'No verb'
        else:
            return self.parsedTree.pos()[minimum][0]

if __name__ == '__main__':
    question = 'please help me to find a word which can describe "find"'
    keyword = re.findall('"([^"]*)"', question)
    for k in keyword:
        question =  question.replace('\"' + k + '\"', 'KKEEYYWWOORRDD')
    Finder = FindNearest(question)
    nearestVerb = Finder.GetNearest(keyword[0])
    print nearestVerb
    w = WRC()
    #print w.FindConnection(nearestVerb,'v',0,'portray') 
    print w.FindSimilarity(nearestVerb, 'depict', 'v')
