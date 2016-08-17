import os
import CRFPP
from parser import *

class KeywordExtractor():
  def __init__ (self, sentence):
    FP = FeatureParser('', '', 0)
    self.sentence_parsed = FP.ParseSentence(sentence)
    print self.sentence_parsed
    
