import nltk
from nltk.parse.stanford import StanfordParser
#import matplotlib.pyplot as plt
import json
import os
import csv
import pickle
import json
PARSER_PATH = ''
if 'NatureUserInterface' in os.environ['PWD']:
  PARSER_PATH = '/stanford-parser/'
else :
  PARSER_PATH = '/Main/NatureUserInterface/stanford-parser/'
parser_path = os.path.abspath(os.path.dirname(__name__)) + PARSER_PATH
os.environ['STANFORD_PARSER'] = parser_path + 'stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parser_path + 'stanford-parser-3.5.2-models.jar'
dep_parser = StanfordParser(model_path=parser_path+'englishPCFG.ser.gz')

class FeatureParser():
    '''
    Command 0 : _ _ keyword _ _
    Command 1 : keyword/keyword 
    Command 2 : listen ?keyword music
    Command 3 : adj. keyword
    Command 4 : adv. keyword 
    Command 5 : ~keyword
    Command 6 : run out _ 
    '''  
    def __init__(self,filename, dataType ,command):
        self.fileName = filename
        self.command = command
        '''
        if user just need to use the feature,
        pass the parameter PARSEDATA with FALSE.
        '''
        if dataType == 'train':
            self.ReadQuestionFromFile()
            self.ParseData()
            self.SaveToJson()
        elif dataType == 'test':
            self.ReadQuestionFromFile()
            self.GenerateTestData()
            self.SaveTestData()
        elif dataType == 'correct':
            self.ReadQuestionFromFile()
            self.GenerateCorrectAnswer()
            self.SaveCorrectAnswer()
    def GenerateTestData(self):
        questionParsed = []
        print('Parsing For Test' + str(self.command))
        question_length = len(self.question)
        for q in self.question[(question_length/10) * 7: question_length]:
            try:
                question = self.dep_parser.raw_parse(q[self.command])
                questionParsed.append(question)
            except:
                continue
        self.questionParsed = questionParsed
  
    def SaveTestData(self):
        questionFeature = []  
        fTEXT = open('./static/keyword/TestData/test_data' + str(self.command) + '.txt', 'wb')
        for q in self.questionParsed:
             feature = []
             for question in q:
                q = question
                KEYWORD_SYMBOL = False
             for leave in q.subtrees(lambda t: t.height() == 2):
                #print leave[0]
                if (leave[0] == '\''):
                  KEYWORD_SYMBOL = not KEYWORD_SYMBOL 
                elif (leave[0] == '`'):
                  KEYWORD_SYMBOL = not KEYWORD_SYMBOL 
                else :
                  if (KEYWORD_SYMBOL):
                    keyword_label = 'T'
                  else :
                    keyword_label = 'F'
                  feature.append(leave[0] + '   ' + leave.label() +'\n')
                  fTEXT.write(leave[0] + '    ' + leave.label() +'\n')
             questionFeature.append(feature)
             fTEXT.write('\n')
        fTEXT.close()

    def GenerateCorrectAnswer(self):
        questionParsed = []
        print('Parsing For Test' + str(self.command))
        question_length = len(self.question)
        for q in self.question[(question_length/10) * 7: question_length]:
            try:
                question = self.dep_parser.raw_parse(q[self.command])
                questionParsed.append(question)
            except:
                continue
        self.questionParsed = questionParsed

    def SaveCorrectAnswer(self):
        questionFeature = []  
        fTEXT = open('./static/keyword/TestData/correct_data' + str(self.command) + '.txt', 'wb')
        for q in self.questionParsed:
             feature = []
             for question in q:
                q = question
                KEYWORD_SYMBOL = False
             for leave in q.subtrees(lambda t: t.height() == 2):
                #print leave[0]
                if (leave[0] == '\''):
                  KEYWORD_SYMBOL = not KEYWORD_SYMBOL 
                elif (leave[0] == '`'):
                  KEYWORD_SYMBOL = not KEYWORD_SYMBOL 
                else :
                  if (KEYWORD_SYMBOL):
                    keyword_label = 'T'
                  else :
                    keyword_label = 'F'
                  feature.append(leave[0] + '   ' + leave.label() +'\n')
                  fTEXT.write(leave[0] + '    ' + leave.label() + '   '+ keyword_label + '\n')
             questionFeature.append(feature)
             fTEXT.write('\n')
        fTEXT.close()


    def ParseSentence(self, question):
        #question = self.dep_parser.raw_parse(sentence)
        feature = []
        for q in question:
          question = q
        KEYWORD_SYMBOL = False
        for leave in question.subtrees(lambda t: t.height() == 2):
            if (leave[0] == '\''):
              KEYWORD_SYMBOL = not KEYWORD_SYMBOL 
            elif (leave[0] == '`'):
              KEYWORD_SYMBOL = not KEYWORD_SYMBOL 
            else :
              if (KEYWORD_SYMBOL):
                keyword_label = 'T'
              else :
                keyword_label = 'F'
              feature.append(leave[0] + '   ' + leave.label())
        return feature
    def ReadQuestionFromFile(self):
        f = open(self.fileName, 'r')  
        question =[] 
        for row in csv.reader(f):
            question.append(row[0:])
        self.question = question
        f.close()
   
    # different colums in self.question
    def ParseData(self):
        questionParsed = []
        print('Parsing For Command' + str(self.command))
        for q in self.question[0: (len(self.question)/10)*7]:
            try:
                question = dep_parser.raw_parse(q[self.command])
                questionParsed.append(question)
            except:
                continue
        self.questionParsed = questionParsed 
    def SaveToJson(self):  
        questionFeature = []  
        fTEXT = open('./static/keyword/TrainData/v2/train_data' + str(self.command) + '.txt', 'wb')
        for q in self.questionParsed:
             feature = []
             for question in q:
                q = question
                KEYWORD_SYMBOL = False
             for leave in q.subtrees(lambda t: t.height() == 2):
                #print leave[0]
                if (leave[0] == '\''):
                  KEYWORD_SYMBOL = not KEYWORD_SYMBOL 
                elif (leave[0] == '`'):
                  KEYWORD_SYMBOL = not KEYWORD_SYMBOL 
                else :
                  if (KEYWORD_SYMBOL):
                    keyword_label = 'T'
                  else :
                    keyword_label = 'F'
                  feature.append(leave[0] + '   ' + leave.label() + '   ' + keyword_label + '\n')
                  fTEXT.write(leave[0] + '    ' + leave.label() + '    ' + keyword_label + '\n')
             questionFeature.append(feature)
             fTEXT.write('\n')
        #fJSON = open('./features/command'+str(self.command)+'.json','wb')
        #json.dump(questionFeature,fJSON)
        #fJSON.close()
        fTEXT.close()
        print questionFeature
     
    
if __name__ == "__main__":
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 0)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 1)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 2)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 3)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 4)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 5)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 6)
    '''
    FP = FeatureParser('./static/keywordRawInput.csv', 'test', 0)
    FP = FeatureParser('./static/keywordRawInput.csv', 'test', 1)
    FP = FeatureParser('./static/keywordRawInput.csv', 'test', 2)
    FP = FeatureParser('./static/keywordRawInput.csv', 'test', 3)
    FP = FeatureParser('./static/keywordRawInput.csv', 'test', 4)
    FP = FeatureParser('./static/keywordRawInput.csv', 'test', 5)
    FP = FeatureParser('./static/keywordRawInput.csv', 'test', 6)
    '''
    '''
    FP = FeatureParser('./static/keywordRawInput.csv', 'correct', 0)
    FP = FeatureParser('./static/keywordRawInput.csv', 'correct', 1)
    FP = FeatureParser('./static/keywordRawInput.csv', 'correct', 2)
    FP = FeatureParser('./static/keywordRawInput.csv', 'correct', 3)
    FP = FeatureParser('./static/keywordRawInput.csv', 'correct', 4)
    FP = FeatureParser('./static/keywordRawInput.csv', 'correct', 5)
    FP = FeatureParser('./static/keywordRawInput.csv', 'correct', 6)
    '''


