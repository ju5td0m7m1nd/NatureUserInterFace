import nltk
from nltk.parse.stanford import StanfordParser
#import matplotlib.pyplot as plt
import json
import os
import csv
import pickle
import json
from nltk import pos_tag, word_tokenize
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
        #for q in self.question[0: (len(self.question)/10)*7]:
        for q in self.question[0: len(self.question)]:
            try:
                #question = dep_parser.raw_parse(q[self.command])
                text = word_tokenize(q[self.command])
                question = pos_tag(text)
                questionParsed.append({'tokenize': question, 'original': q[self.command]})
            except:
                continue
        self.questionParsed = questionParsed
    def SaveToJson(self):
        questionFeature = []
        fTEXT = open('./static/keyword/TrainData/v2/train_data' + str(self.command) + '.txt', 'wb')
        for q in self.questionParsed:
          feature = {} 
          KEYWORD_SYMBOL = 'F' 
          '''
          Parse sentence into object with the datatype
          {`someword`: `flag`} 
          for example: {'how': 'F', 'to': 'F', 'describe': 'F', 'beach': 'T'} 
          '''

          for word_pos in q['tokenize']:
            feature[word_pos[0]] = KEYWORD_SYMBOL 
            if (word_pos[0] == '``'):
              KEYWORD_SYMBOL = 'T' 
            elif (word_pos[0] == '\'\''):
              KEYWORD_SYMBOL = 'F' 
          split_question = q['original'].split('"')
          combine_question = ''
          for split_q in split_question:
            combine_question += split_q
          words_pos = pos_tag(word_tokenize(combine_question)) 
          for w in words_pos:
            fTEXT.write(w[0] + '    '+ w[1] + '    ' + feature[w[0]] + '\n')
          
          fTEXT.write('\n')
        '''
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
        '''
        fTEXT.close()


if __name__ == "__main__":
    #FP = FeatureParser('./static/keywordRawInput.csv', 'train', 0)
    #FP = FeatureParser('./static/keywordRawInput.csv', 'train', 1)
    #FP = FeatureParser('./static/keywordRawInput.csv', 'train', 2)
    #FP = FeatureParser('./static/keywordRawInput.csv', 'train', 3)
    #FP = FeatureParser('./static/keywordRawInput.csv', 'train', 4)
    #FP = FeatureParser('./static/keywordRawInput.csv', 'train', 5)
    #FP = FeatureParser('./static/keywordRawInput.csv', 'train', 6)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 0)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 1)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 2)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 3)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 4)
    FP = FeatureParser('./static/keywordRawInput_v2.csv', 'train', 5)
