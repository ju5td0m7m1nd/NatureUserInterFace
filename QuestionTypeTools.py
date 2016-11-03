from KeywordExtractor import *
from ExtractFeatureTools import SpecPosFinder, WordRelationCounter
import pickle
import os
from nltk import pos_tag, word_tokenize

#a tool which collect all the feature
class FeatureExtractor:
    def __init__(self):
        self.depParser = StanfordParser(model_path=parser_path+'englishPCFG.ser.gz')
        self.WRC = WordRelationCounter()
        self.SPF = SpecPosFinder()

    def GetFeature(self, inputQuestion, wn):
        self.inputQuestion = inputQuestion
        text = word_tokenize(self.inputQuestion)
        self.questionPos = pos_tag(text)
        print self.questionPos

        KE = KeywordExtractor(self.questionPos)
        KE.Input(inputQuestion)
        keywordAndLabel = KE.Predict()
        print keywordAndLabel

        self.keyword = keywordAndLabel['keyword']
        self.label = keywordAndLabel['label']

        features = []
        features.append(self.FindQuestionAdverb())
        features.extend(self.CalculateSimilarity(wn))
        features.append(self.FindPreposition())
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
        similarities = []
        targets = [
                {'list': [nearestVerb], 'word': 'describe', 'pos': 'v'},
                {'list': [nearestVerb], 'word': 'use',      'pos': 'v'},
                {'list': [nearestVerb], 'word': 'replace',  'pos': 'v'},
                {'list': nouns,         'word': 'synonym',  'pos': 'n'},
                {'list': nouns,         'word': 'usage',    'pos': 'n'}
        ]
        for t in targets:
            similarities.append(self.WRC.FindSimilarity(t['list'], t['word'], t['pos'], wn))
        return similarities

    # find the nearest of ['or', 'with', 'to'] to the keyword
    def FindPreposition(self):
        nearestPrep = self.SPF.GetNearest(['I', 'C', 'T'], self.label, self.questionPos).lower()
        targets = ['or', 'with', 'to', 'before', 'after']
        if nearestPrep in targets:
            return targets.index(nearestPrep) + 1
        return 0

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
        return pickle.load(open(modelPath+'static/questionType/model_v3.sav', 'rb'))
    def Predict(self, features):
        return self.model.predict(features)[0]

#make query according to the predicted question type with some if else judgements
class QueryManager:
    def __init__(self):
        self.WRC = WordRelationCounter()
    def GetQuery(self, questionType, inputQuestion, keyword, wn):
        result = {'parse': True, 'command': ''}
        dispatcher = [self.HowToUse, self.WhichIsRight, self.AddPartOfSpeech, self.ReplaceWord]
        try:
            print questionType
            result['command'] = dispatcher[questionType](inputQuestion, keyword, wn)
        except:
            #raise
            result['parse'] = False
        return result

    # '_ _ posibble _ _'
    def HowToUse(self, inputQuestion, keyword, wn):
        query = '* ' + keyword[0] + ' *'
        return query

    # 'in/at the afternoon', 'listen ?to music'
    def WhichIsRight(self, inputQuestion, keyword, wn):
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
        #temp = inputQuestion
        addPosType = self.WRC.GetAddPOSType(inputQuestion.replace(keyword[0], 'keyword'))
        query = ''
        dispatcher = {'before': self.BeforeKeyword, 'after': self.AfterKeyword, 'both': self.BothKeyword}
        query = dispatcher[addPosType](inputQuestion, keyword, wn)
        return query


    # 'I am ~happy about'
    def ReplaceWord(self, inputQuestion, keyword, wn):
        query = ''
        target = keyword[0] if len(keyword[0]) < len(keyword[1]) else keyword[1]
        sentence = keyword[1] if len(keyword[0]) < len(keyword[1]) else keyword[1]
        for word in sentence.split():
            if target == word:
                query += "~"
            query += word + " "
        return query

    #-----------------
    #for type 'AddPartOfSpeech'
    def BeforeKeyword(self, inputQuestion, keyword, wn):
        query = ''
        wantedPos = ['v', 'a', 's', 'n']
        pickedPos = self.GetPopularUsage(keyword[0], wantedPos, wn)
        if pickedPos == 'n':
            query = 'adj. ' + keyword[0]
        elif pickedPos in ['v', 'a', 's']:
            query = 'adv. ' + keyword[0]
        return query

    def AfterKeyword(self, inputQuestion, keyword, wn):
        query = ''
        wantedPos = ['v', 'a', 's', 'n', 'r']
        pickedPos = self.GetPopularUsage(keyword[0], wantedPos, wn)
        print 'picked', pickedPos
        if pickedPos in ['v', 'a', 's']:
            #print keyword[0]
            query = keyword[0] + ' n.'
        elif pickedPos == 'r':
            query = keyword[0] + ' v./adj.'
        return query

    def BothKeyword(self, inputQuestion, keyword, wn):
        query = '* ' + keyword[0] + ' *'
        return query
    #-----------------

    def GetPopularUsage(self, keyword, wantedPos, wn):
        keywordSyns = wn.synsets(keyword)
        keyPosList = {}
        pickedPos = {'pos': '', 'count': 0}
        # verb, adj, noun, adv
        for syn in keywordSyns:
            pos = syn.pos()
            if pos in wantedPos:
                if pos in keyPosList:
                    keyPosList[pos] += 1
                    if keyPosList[pos] > pickedPos['count']:
                        pickedPos = {'pos': pos, 'count': keyPosList[pos]}
                else:
                    keyPosList[pos] = 1
                    if pickedPos['pos'] == '':
                        pickedPos = {'pos': pos, 'count': keyPosList[pos]}
        return pickedPos['pos']


