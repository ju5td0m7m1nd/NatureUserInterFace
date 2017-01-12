import nltk
from nltk.parse.stanford import StanfordParser
import json
import os
import csv
import pickle
import json

class AutoGenerateTrainData():
  def __init__(self):

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
        fTEXT.close()
