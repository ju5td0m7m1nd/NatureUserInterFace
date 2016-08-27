import re
from FindNearest import FindNearest
from WordRelation import WRC
from KeywordExtractor import *

class FeatureExtractor:
    def GetFeature(self, question):
        KE = KeywordExtractor()
        keywordAndLabel = KE.Predict()
       
        
        self.question = question
        self.keyword = keywordAndLabel['keyword']
        self.label = keywordAndLabel['label']
        

        #for "please tell me which one is right, in the afternoon or at the afternoon"
        #self.keyword = ['in the afternoon', 'at the afternoon']
        #self.label = ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'T', 'T', 'T', 'F', 'T', 'T', 'T']

        feature = []

        feature.append(self.FindQuestionAdverb())

        feature.extend(self.CalculateSimilarity())

        return feature
    
    def FindQuestionAdverb(self):
        questionAdverbs = ['how', 'which', 'what', 'when']
        for i in range(0, len(questionAdverbs)):
            if questionAdverbs[i] in self.question.lower():
                return i+1
        return 0

    def CalculateSimilarity(self):
        FN = FindNearest(self.question, self.label)
        nearestVerb = FN.GetNearest()
        print 'calculating similarity......'
        wrc = WRC()
        similarities = []
        print 'calculating first verb.'
        similarities.append(wrc.FindSimilarity(nearestVerb, 'describe', 'v'))
        print 'calculating second verb.'
        similarities.append(wrc.FindSimilarity(nearestVerb, 'use', 'v'))
        print 'calculating third verb.'
        similarities.append(wrc.FindSimilarity(nearestVerb, 'replace', 'v'))
        print 'finish calculating similarity'
        return similarities

    def GetKeyword(self):
        return self.keyword

if __name__ == "__main__":
    FE = FeatureExtractor()
    print FE.GetFeature('how to describe "beach"?')
        
