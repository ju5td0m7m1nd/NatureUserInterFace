from KeywordExtractor import *
from ExtractFeatureTools import NearestFinder, WordRelationCounter
import pickle
import os

PARSER_PATH = ''
if 'NatureUserInterface' in os.environ['PWD']:
  PARSER_PATH = '/stanford-parser/'
else :
  PARSER_PATH = '/Main/NatureUserInterface/stanford-parser/'
parser_path = os.path.abspath(os.path.dirname(__name__)) + PARSER_PATH
os.environ['STANFORD_PARSER'] = parser_path + 'stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parser_path + 'stanford-parser-3.5.2-models.jar'

class FeatureExtractor:
    def __init__(self):
        self.depParser = StanfordParser(model_path=parser_path+'englishPCFG.ser.gz')

    def GetFeature(self, inputQuestion, wn):
        self.inputQuestion = inputQuestion
        self.parsedQuestion = [node for node in self.depParser.raw_parse(inputQuestion)]
        KE = KeywordExtractor(self.parsedQuestion)
        KE.Input(inputQuestion)
        keywordAndLabel = KE.Predict()
        print keywordAndLabel
        self.keyword = keywordAndLabel['keyword']
        self.label = keywordAndLabel['label']

        features = []
        features.append(self.FindQuestionAdverb())
        features.extend(self.CalculateSimilarity(wn))
        return features
    
    def FindQuestionAdverb(self):
        questionAdverbs = ['how', 'which', 'what', 'when']
        for i in range(0, len(questionAdverbs)):
            if questionAdverbs[i] in self.inputQuestion.lower():
                return i+1
        return 0

    def CalculateSimilarity(self, wn):
        NF = NearestFinder(self.inputQuestion, self.label, self.parsedQuestion)
        nearestVerb = NF.GetNearest('V')
        WRC = WordRelationCounter()
        similarities = []
        similarities.append(WRC.FindSimilarity(nearestVerb, 'describe', 'v', wn))
        similarities.append(WRC.FindSimilarity(nearestVerb, 'use', 'v', wn))
        similarities.append(WRC.FindSimilarity(nearestVerb, 'replace', 'v', wn))
        return similarities

    def GetKeyword(self):
        return self.keyword

class Predictor:
    def __init__(self):
        self.model = self.LoadModel()
    def LoadModel(self):
        modelPath = ''
        if 'NatureUserInterface' in os.environ['PWD']:
          modelPath = './'
        else :
          modelPath = os.path.abspath(os.path.dirname(__name__)) + '/Main/NatureUserInterface/'
        return pickle.load(open(modelPath+'model.sav', 'rb'))
    def Predict(self, features):
        return self.model.predict(features)[0]

class QueryManager:
    #def __init__(self):
    def GetQuery(self, questionType, inputQuestion, keyword):
        result = {'parse': True, 'command': ''}
        try:
            if questionType == 0:
                result['command'] = self.HowToUse(keyword)
            elif questionType == 1:
                result['commmand'] = self.WhichIsRight(inputQuestion, keyword)
            elif questionType == 2:
                result['command'] = self.AddPartOfSpeech(inputQuestion, keyword)
            elif questionType == 3:
                result['command'] = self.ReplaceWord(inputQuestion, keyword)
        except:
            result['parse'] = False
        return result

    def HowToUse(self, keyword):
        query = '_ _ ' + keyword[0] + ' _ _'
        return query

    def WhichIsRight(self, inputQuestion, keyword):
        query = ''
        keyword1 = keyword[0].split()
        keyword2 = keyword[1].split()
        #in/at the afternoon
        if len(keyword1) == len(keyword2):
            for i in range(0, len(keyword1)):
                if keyword1[i] != keyword2[i]:
                    query += keyword1[i] + "/" + keyword2[i] + " "
                else:
                    query += keyword1[i] + " "
        #listen ?to music
        else:
            if len(keyword1) > len(keyword2):
                for word in keyword1:
                    if word not in keyword2:
                        query += "?"
                    query += word + " "
            else:
                for word in keyword2:
                    if word not in keyword1:
                        query += "?"
                    query += word + " "
        return query

    def AddPartOfSpeech(self, inputQuestion, keyword):
        query = 'adj. ' + keyword[0]
        return query

    def ReplaceWord(self, inputQuestion, keyword):
        query = ''
        target = keyword[0] if len(keyword[0]) < len(keyword[1]) else keyword[1]
        sentence = keyword[1] if len(keyword[0] < len(keyword[1])) else keyword[1]
        for word in sentence.split():
            if target == word:
                query += "~"
            query += word + " "
        return query
