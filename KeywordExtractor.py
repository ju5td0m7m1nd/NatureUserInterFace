import os
import CRFPP
from parser import *

class KeywordExtractor():
  def __init__ (self):
    self.FP = FeatureParser('', '', 0)
    self.tagger = CRFPP.Tagger("-m ./static/keyword/model")

  def Input(self, question): 
    self.sentence_parsed = self.FP.ParseSentence(question)

  def predict (self):
    keyword = ''
    keyword_array = []
    tagger = self.tagger
    for tag in self.sentence_parsed:
        tagger.add(str(tag))
     
        # parse and change internal stated as 'parsed'
    tagger.parse()
 
    size = tagger.size()
    xsize = tagger.xsize()
    # Serial of "T" means same keywords, otherwise push into different index
    pre_label = ''
    for i in range(0, (size)):
      if (tagger.y2(i) == 'T'):
        keyword = keyword + tagger.x(i, 0)          

    return keyword

if __name__ == "__main__":

  a = KeywordExtractor('give me a word to put behind watch')
  print a.predict()
