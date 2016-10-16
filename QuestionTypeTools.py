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
