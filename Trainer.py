import csv
from sklearn.naive_bayes import GaussianNB
import pickle
from FeatureExtractor import *
import numpy as np

'''
0: _ _ possible _ _
1: in/at the afternoon, listen ?to music
2: adj. chair, adv. surprised
3: I am ~happy about

how : 1
which : 2
what : 3
when : 4
'''


class Trainer:
    def __init__(self, filename):
        quesAndTags = self.ReadFile(filename)
        questions = quesAndTags['questions']
        tags = np.array(quesAndTags['tags'])
        #for i in range(0, len(questions)):
        #    print str(tags[i]) + ': ' + questions[i]
        features = np.array(self.PileFeatures(questions))

        self.gnb = GaussianNB()
        self.y_pred = self.gnb.fit(features, tags)
        pickle.dump(self.y_pred, open('./model.sav', 'wb+'))

    def ReadFile(self, filename):
        f = open(filename, 'r')  
        fileQuestion = [] 
        index = 0
        for row in csv.reader(f):
            if index != 0:
                fileQuestion.append(row[3:9])
            index += 1
        f.close()
        questions = []
        tags = []
        for qs in fileQuestion:
            for i in range(0, len(qs)):
                questions.append(qs[i])
                if i == 0:
                    tags.append(0)
                elif i == 1 or i == 2:
                    tags.append(1)
                elif i == 3 or i == 4:
                    tags.append(2)
                else:
                    tags.append(3)
        return {'questions': questions, 'tags': tags}

    def PileFeatures(self, questions):
        index = 0
        features = []
        for question in questions:
            index += 1
            print index
            FE = FeatureExtractor()
            feature = FE.GetFeature(question)
            features.append(feature)
        return features

if __name__ == "__main__":
    question = ['which one is right, "listen to music" or "listen music"', 'how to describe "beach"', 'how to use "possible"']
    trainer = Trainer('./static/questionnaireProcessed.csv')
