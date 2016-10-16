from KeywordExtractor import *
from ExtractFeatureTools import NearestFinder, WordRelationCounter

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
        NF = NearestFinder(self.question, self.label, self.questionParsed)
        nearestVerb = NF.GetNearest('V')
        print 'calculating similarity......'
        wrc = WordRelationCounter()
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

        
