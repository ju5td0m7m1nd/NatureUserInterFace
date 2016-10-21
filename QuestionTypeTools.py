from KeywordExtractor import *
from ExtractFeatureTools import SpecPosFinder, WordRelationCounter
import pickle
import os
from nltk import pos_tag, word_tokenize

PARSER_PATH = ''
if 'NatureUserInterface' in os.environ['PWD']:
  PARSER_PATH = '/stanford-parser/'
else :
  PARSER_PATH = '/Main/NatureUserInterface/stanford-parser/'
parser_path = os.path.abspath(os.path.dirname(__name__)) + PARSER_PATH
os.environ['STANFORD_PARSER'] = parser_path + 'stanford-parser.jar'
os.environ['STANFORD_MODELS'] = parser_path + 'stanford-parser-3.5.2-models.jar'

#a tool which collect all the feature
class FeatureExtractor:
    def __init__(self):
        self.depParser = StanfordParser(model_path=parser_path+'englishPCFG.ser.gz')
        self.WRC = WordRelationCounter()
        self.SPF = SpecPosFinder()

    def GetFeature(self, inputQuestion, wn):
        self.inputQuestion = inputQuestion
        #self.parsedQuestion = [node for node in self.depParser.raw_parse(inputQuestion)][0]
        #self.parsedTree = self.parsedQuestion[0]
        text = word_tokenize(self.inputQuestion)
        self.questionPos = pos_tag(text)

        KE = KeywordExtractor(self.questionPos)
        KE.Input(inputQuestion)
        keywordAndLabel = KE.Predict()
        print keywordAndLabel

        text = word_tokenize(self.inputQuestion)
        self.questionPos = pos_tag(text)

        self.keyword = keywordAndLabel['keyword']
        self.label = keywordAndLabel['label']

        features = []
        features.append(self.FindQuestionAdverb())
        features.extend(self.CalculateSimilarity(wn))
        features.append(self.FindPreposition())
        #self.FindAllSpecPOS('N', wn)
        return features
   
    #first feature: question adverb
    def FindQuestionAdverb(self):
        questionAdverbs = ['how', 'which', 'what', 'when']
        for i in range(0, len(questionAdverbs)):
            if questionAdverbs[i] in self.inputQuestion.lower():
                return i+1
        return 0

    #other features (temporary): 
    #find the similarity of the specified part-of-speach word nearest to the keyword
    #with the words in the dictionary 
    def CalculateSimilarity(self, wn):
        nearestVerb = self.SPF.GetNearest(['V'], self.label, self.questionPos)
        nouns = self.SPF.GetAll('N', self.label, self.questionPos)
        #print nearestVerb
        similarities = []
        similarities.append(self.WRC.FindSimilarity([nearestVerb], 'describe', 'v', wn))
        similarities.append(self.WRC.FindSimilarity([nearestVerb], 'use', 'v', wn))
        similarities.append(self.WRC.FindSimilarity([nearestVerb], 'replace', 'v', wn))
        similarities.append(self.WRC.FindSimilarity(nouns, 'synonym', 'n', wn))
        similarities.append(self.WRC.FindSimilarity(nouns, 'usage', 'n', wn))
        return similarities

    # find the nearest of ['or', 'with', 'to'] to the keyword
    def FindPreposition(self):
        nearestPrep = self.SPF.GetNearest(['I', 'C', 'T'], self.label, self.questionPos)
        if nearestPrep.lower() == 'or':
            return 1
        elif nearestPrep.lower() == 'with':
            return 2
        elif nearestPrep.lower() == 'to':
            return 3
        return 0

    def FindAllSpecPOS(self, partOfSpeach, wn):
        nouns = self.SPF.GetAll('N', self.label, self.questionPos)
        similarity = self.WRC.FindSimilarity(nouns, 'synonym', 'n', wn)
        print similarity
        #s = self.WRC.FindSimilarity(['same'], 'same', 'a', wn)

    def GetKeyword(self):
        return self.keyword

#load trained model and predict question type
class Predictor:
    def __init__(self):
        self.model = self.LoadModel()
    def LoadModel(self):
        modelPath = ''
        if 'NatureUserInterface' in os.environ['PWD']:
          modelPath = './'
        else :
          modelPath = os.path.abspath(os.path.dirname(__name__)) + '/Main/NatureUserInterface/'
        return pickle.load(open(modelPath+'model_v2.sav', 'rb'))
    def Predict(self, features):
        return self.model.predict(features)[0]

#make query according to the predicted question type with some if else judgements
class QueryManager:
    def GetQuery(self, questionType, inputQuestion, keyword, wn):
        result = {'parse': True, 'command': ''}
        try:
            print questionType
            if questionType == 0:
                result['command'] = self.HowToUse(keyword)
            elif questionType == 1:
                result['command'] = self.WhichIsRight(inputQuestion, keyword)
            elif questionType == 2:
                result['command'] = self.AddPartOfSpeech(inputQuestion, keyword, wn)
            elif questionType == 3:
                result['command'] = self.ReplaceWord(inputQuestion, keyword)
        except:
            raise
            #result['parse'] = False
        return result

    # '_ _ posibble _ _'
    def HowToUse(self, keyword):
        query = '* ' + keyword[0] + ' *'
        return query

    # 'in/at the afternoon', 'listen ?to music'
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

    # 'adj. beach'
    def AddPartOfSpeech(self, inputQuestion, keyword, wn):
        keywordSyns = wn.synsets(keyword[0])
        keyPosList = {}
        pickedPos = {'pos': '', 'count': 0}
        # verb, adj, noun, adv
        wanted = ['v', 'a', 'n', 'r']
        for syn in keywordSyns:
            pos = syn.pos()
            if pos in wanted:
                if pos in keyPosList:
                    keyPosList[pos] += 1
                    if keyPosList[pos] > pickedPos['count']:
                        pickedPos = {'pos': pos, 'count': keyPosList[pos]}
                else:
                    keyPosList[pos] = 1
                    if pickedPos['pos'] == '':
                        pickedPos = {'pos': pos, 'count': keyPosList[pos]}
        if pickedPos['pos'] == 'n':
            query = 'adj. ' + keyword[0]
        elif pickedPos['pos'] == 'v' or pickedPos['pos'] == 'a':
            query = 'adv. ' + keyword[0]
        return query

    # 'I am ~happy about'
    def ReplaceWord(self, inputQuestion, keyword):
        query = ''
        target = keyword[0] if len(keyword[0]) < len(keyword[1]) else keyword[1]
        sentence = keyword[1] if len(keyword[0]) < len(keyword[1]) else keyword[1]
        for word in sentence.split():
            if target == word:
                query += "~"
            query += word + " "
        return query
