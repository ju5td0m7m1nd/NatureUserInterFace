import os
import CRFPP
from FeatureParser import *

Path = ''
if 'NatureUserInterface' in os.environ['PWD']:
  PATH = '/'
else :
  PATH = '/Main/NatureUserInterface/'
model_path = os.path.abspath(os.path.dirname(__name__)) + PATH + 'static/keyword/model'

class KeywordExtractor():
  def __init__ (self, questionParsed):
    self.questionParsed = questionParsed
    print ("KeywordExtractor: init")
    self.FP = FeatureParser('', '', 0)
    print ("KeywordExtractor: Feature Parser Init")
    self.tagger = CRFPP.Tagger("-m "+model_path)
    print ("KeywordExtractor: load model succeed")

  def Input(self, question): 
     
    for item in self.questionParsed:
      self.tagger.add(str(item[0] + '   ' + item[1]))
    #self.sentence_parsed = self.FP.ParseSentence(self.questionParsed)

  def Predict (self):
    print ("KeywordExtractor: Predict")
    keyword = ''
    keyword_array = []
    label_serial = []

    tagger = self.tagger
    #for tag in self.sentence_parsed:
    #    tagger.add(str(tag))
     
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
  a.Input('listen music or listen to music')
  print a.Predict()
