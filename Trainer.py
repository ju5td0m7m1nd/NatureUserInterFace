import csv
from sklearn.naive_bayes import GaussianNB
import pickle
from QuestionTypeTools import FeatureExtractor
from nltk.corpus import wordnet

class Trainer:
    def __init__(self):
        self.rawData = self.ReadFile()
        self.featuresPile = self.CollectFeaturesPile()
        self.TrainModel()

    # read file, extract questions, mark type
    def ReadFile(self):
        f = open('./static/questype.csv', 'r')
        rawQuestions = []
        addTypeQuestions = []
        tags = []
        for row in csv.reader(f):
            for i in range(0, len(row[:5])):
                rawQuestions.append(row[i])
                if i >= 2:
                    tags.append(i-1)
                else:
                    tags.append(i)
        f.close()
        return {'questions': rawQuestions, 'tags': tags}

    def CollectFeaturesPile(self):
        wn = wordnet.synsets('describe','v')
        featuresPile = []
        index = 0
        for rawQuestion in self.rawData['questions']:
            index += 1
            print index
            FE = FeatureExtractor()
            featuresPile.append(FE.GetFeature(rawQuestion, wordnet))
        return featuresPile

    def TrainModel(self):
        GNB = GaussianNB()
        yPred = GNB.fit(self.featuresPile, self.rawData['tags'])
        pickle.dump(yPred, open('./questionType/model_v3.sav', 'wb'))


trainer = Trainer()
