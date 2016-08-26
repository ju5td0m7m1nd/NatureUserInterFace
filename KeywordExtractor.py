import os
import CRFPP
from parser import *

class KeywordExtractor():
  def __init__ (self):
    self.FP = FeatureParser('', '', 0)
    self.tagger = CRFPP.Tagger("-m ./static/keyword/model")

  def Input(self, question): 
    self.sentence_parsed = self.FP.ParseSentence(question)

  def Predict (self):
    keyword = ''
    keyword_array = []
    label_serial = []

    tagger = self.tagger
    for tag in self.sentence_parsed:
        tagger.add(str(tag))
     
        # parse and change internal stated as 'parsed'
    tagger.parse()
 
    size = tagger.size()
    xsize = tagger.xsize()
    # Serial of "T" means same keywords, otherwise push into different index
    pre_label = 'F'
    array_length = -1
    for i in range(0, (size)):
      if (tagger.y2(i) == 'T'):
        keyword = tagger.x(i, 0)
        if (pre_label != 'T'):
          array_length += 1 
          keyword_array.append(keyword)
        else:
          keyword_array[array_length] = keyword_array[array_length] + ' ' + keyword          
      label_serial.append(tagger.y2(i))
      pre_label = tagger.y2(i)
    return {'keyword': keyword_array, 'label': label_serial}

if __name__ == "__main__":

  a = KeywordExtractor()
  a.Input('How to describe beach')
  print a.Predict()
