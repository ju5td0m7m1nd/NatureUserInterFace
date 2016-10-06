'''
'''
'''
WRC stands for word relation calculator
'''
from nltk.corpus import wordnet as wn
from nltk.parse.stanford import StanfordParser
import os
import re
from WordRelation import WRC

'''
PARSER_PATH = ''
if 'NatureUserInterface' in os.environ['PWD']:
  PARSER_PATH = '/stanford-parser/'
else :
  PARSER_PATH = '/Main/NatureUserInterface/stanford-parser/'
parser_path = os.path.abspath(os.path.dirname(__name__)) + PARSER_PATH
os.environ['STANFORD_PARSER'] = parser_path + 'stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parser_path + 'stanford-parser-3.5.2-models.jar'
dep_parser = StanfordParser(model_path=parser_path+'englishPCFG.ser.gz')
'''
'''
os.environ['STANFORD_PARSER'] = './stanford-parser/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = './stanford-parser/stanford-parser-3.5.2-models.jar'
dep_parser = StanfordParser(model_path='./stanford-parser/englishPCFG.ser.gz')
'''
class FindNearest():
    def __init__(self, question, label, questionParsed):
        self.questionParsed = questionParsed
        self.question = question
        self.label = label
        self.verbsPosition = []
        self.parsedTree = []
        self.ParseData()
        self.GetVsPosition()
        
    def ParseData(self):
        #print 'parsing data...'
        #self.questionParsed = dep_parser.raw_parse(self.question)
        for q in self.questionParsed:
            self.parsedTree = q
        print 'finish parsing data'

    def GetVsPosition(self):
        verbsPosition = []
        leaf_values = self.parsedTree.leaves()
        pos = self.parsedTree.pos()
        for i in range(0, len(pos)):
            if str(pos[i][1])[0] == 'V' and self.label[i] != 'T':
                verbsPosition.append({'word': pos[i][0], 'position': i})
        self.verbsPosition = verbsPosition

    def GetNearest(self):
        keywordPos = 0
        for i in range(0, len(self.label)):
            if self.label[i] == 'T':
                keywordPos = i
                break
        position = 100000
        word = ''
        for pairs in self.verbsPosition:
            if abs(pairs['position'] - keywordPos) < abs(position - keywordPos):
                position = pairs['position']
                word = pairs['word']
        if len(self.verbsPosition) == 0:
            return 'No verb'
        else:
            return word
