import re
from FindNearest import FindNearest
from WordRelation import WRC

class FeatureExtractor:
    def GetFeature(self, question):
        feature = []

        feature.append(self.FindQuestionAdverb(question))

        feature.extend(self.CalculateSimilarity(question))

        return feature
    
    def FindQuestionAdverb(self, question):
        questionAdverbs = ['how', 'which', 'what', 'when']
        for i in range(0, len(questionAdverbs)):
            if questionAdverbs[i] in question.lower():
                return i+1
        return 0

    def CalculateSimilarity(self, question):
        nearestVerb = self.FindNearestVerb(question)
        wrc = WRC()
        similarities = []
        similarities.append(wrc.FindSimilarity(nearestVerb, 'describe', 'v'))
        similarities.append(wrc.FindSimilarity(nearestVerb, 'use', 'v'))
        similarities.append(wrc.FindSimilarity(nearestVerb, 'replace', 'v'))
        return similarities


    def FindNearestVerb(self, question):
        keyAndQuest = self.GetKeyword(question)
        keyword = keyAndQuest['keyword']
        question = keyAndQuest['question']
        FN = FindNearest(question)
        nearestVerb = FN.GetNearest(keyword[0])
        return nearestVerb

    def GetKeyword(self, question):
        keyword = re.findall('"([^"]*)"', question)
        for k in keyword:
            question =  question.replace('\"' + k + '\"', 'KKEEYYWWOORRDD')
        return {'keyword': keyword, 'question' : question}

if __name__ == "__main__":
    FE = FeatureExtractor()
    print FE.GetFeature('how to describe "beach"?')
        
