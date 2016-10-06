import re
from FindNearest import FindNearest
from WordRelation import WRC
from KeywordExtractor import *

PARSER_PATH = ''
if 'NatureUserInterface' in os.environ['PWD']:
  PARSER_PATH = '/stanford-parser/'
else :
  PARSER_PATH = '/Main/NatureUserInterface/stanford-parser/'
parser_path = os.path.abspath(os.path.dirname(__name__)) + PARSER_PATH
os.environ['STANFORD_PARSER'] = parser_path + 'stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parser_path + 'stanford-parser-3.5.2-models.jar'



class FeatureExtractor:
    def GetFeature(self, question, wn):
      
        dep_parser = StanfordParser(model_path=parser_path+'englishPCFG.ser.gz')
        self.questionParsed = [node for node in dep_parser.raw_parse(question)]
        print ("FeatureExtractor: Get Feature")
        KE = KeywordExtractor(self.questionParsed)
        print ("FeatureExtractor: Init KeywordExtractor")
        KE.Input(question)
        keywordAndLabel = KE.Predict()
       
        print keywordAndLabel        
        self.question = question
        self.keyword = keywordAndLabel['keyword']
        self.label = keywordAndLabel['label']
        

        #for "please tell me which one is right, in the afternoon or at the afternoon"
        #self.keyword = ['in the afternoon', 'at the afternoon']
        #self.label = ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'T', 'T', 'T', 'F', 'T', 'T', 'T']
        #for "listen music or listen to music"
        #self.keyword = ['listen music', 'listen to music']
        #self.label = ['T', 'T', 'F', 'T', 'T', 'T']

        feature = []

        feature.append(self.FindQuestionAdverb())

        feature.extend(self.CalculateSimilarity(wn))

        return feature
    
    def FindQuestionAdverb(self):
        questionAdverbs = ['how', 'which', 'what', 'when']
        for i in range(0, len(questionAdverbs)):
            if questionAdverbs[i] in self.question.lower():
                return i+1
        return 0

    def CalculateSimilarity(self, wn):
        FN = FindNearest(self.question, self.label, self.questionParsed)
        nearestVerb = FN.GetNearest()
        print 'calculating similarity......'
        wrc = WRC()
        similarities = []
        print 'calculating first verb.'
        similarities.append(wrc.FindSimilarity(nearestVerb, 'describe', 'v', wn))
        print 'calculating second verb.'
        similarities.append(wrc.FindSimilarity(nearestVerb, 'use', 'v', wn))
        print 'calculating third verb.'
        similarities.append(wrc.FindSimilarity(nearestVerb, 'replace', 'v', wn))
        print 'finish calculating similarity'
        return similarities

    def GetKeyword(self):
        return self.keyword

if __name__ == "__main__":
    FE = FeatureExtractor()
    print FE.GetFeature('how to describe "beach"?')
        
