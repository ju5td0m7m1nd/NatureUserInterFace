'''
NPF stands for nearest pos finder
'''
'''
This class can calculate a relation between
"User's word" and our "Preserve word"'s relation.

For example, 
the preserver verb contain : describe, elaborate.
Now I want to figure out if the word "modify" can be find
within 5 level of describe and elaborate.
if I find in first level, and the score of "modify" is [describe's score]*1
if find in secord level , the score will be [describe's score] * 0.8, and soon.
'''

'''
WRC stands for word relation calculator
'''
from nltk.corpus import wordnet as wn
from nltk.parse.stanford import StanfordParser
import os
import numpy
import re
os.environ['STANFORD_PARSER'] = '../stanford-parser/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = '../stanford-parser/stanford-parser-3.5.2-models.jar' 
dep_parser = StanfordParser(model_path='../stanford-parser/englishPCFG.ser.gz')

class WRC():
    def __init__(self, question):
        self.verbsPosition = []
        self.parsedTree = []
        self.question = question
        self.ParseData()
        self.GetVsPosition()
        
    def ParseData(self):
        print('Parsing.')
        questionParsed = dep_parser.raw_parse(self.question)
        self.questionParsed = questionParsed
        for q in self.questionParsed:
            self.parsedTree = q

    def GetVsPosition(self):
        verbsPosition = []
        leaf_values = self.parsedTree.leaves()
        for pairs in self.parsedTree.pos():
            if str(pairs[1])[0] == 'V':
                verbsPosition.append([pairs[0], leaf_values.index(pairs[0])])
        self.verbsPosition = verbsPosition
        #print self.verbsPosition
    def GetNearest(self, keyword):
        leaf_values = []
        leaf_values = self.parsedTree.leaves()
        keywordPos = leaf_values.index(keyword)
        minimum = 100000
        for pairs in self.verbsPosition:
            if abs(pairs[1] - keywordPos) < abs(minimum - keywordPos):
                minimum = pairs[1]
        if len(self.verbsPosition) == 0:
            return 'No verb'
        else:
            return self.parsedTree.pos()[minimum][0]

if __name__ == '__main__':
    question = 'please help me to find a word which can describe "chair"'
    keyword = re.findall('"([^"]*)"', question)
    question =  question.replace('\"', '')
    WRC = WRC(question)
    print WRC.GetNearest('chair')
