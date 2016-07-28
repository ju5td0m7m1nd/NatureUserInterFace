import csv
from sklearn.naive_bayes import GaussianNB
import pickle
from FeatureExtractor import FeatureExtractor

'''
usage : 0
which : 1
optional : 2
pos : 3
replace : 4
anyword : 5


how : 1
which : 2
what : 3
when : 4
'''


class Trainer:
    def __init__(self, filename):
        quesAndTags = self.ReadFile(filename)
        questions = quesAndTags['questions']
        tags = quesAndTags['tags']

        features = self.PileFeatures(questions, tags)

        self.gnb = GaussianNB()
        self.y_pred = self.gnb.fit(features, tags)
        pickle.dump(self.y_pred, open('./model.sav', 'wb'))

    def ReadFile(self, filename):
        f = open(filename, 'r')  
        fileQuestion = [] 
        index = 0
        for row in csv.reader(f):
            if index != 0:
                fileQuestion.append(row[3:8])
            index += 1
        f.close()
        questions = []
        tags = []
        for qs in fileQuestion:
            for i in range(0, len(qs)):
                questions.append(qs[i])
                tags.append(i)
        return {'questions': questions, 'tags': tags}

    def PileFeatures(self, questions, tags):
        index = 0
        features = []
        for question in questions:
            index += 1
            print index
            FE = FeatureExtractor()
            feature = FE.GetFeature(question)
            #feature = self.GetFeatures(question)
            features.append(feature)
        return features

if __name__ == "__main__":
    question = ['which one is right, "listen to music" or "listen music"', 'how to describe "beach"', 'how to use "possible"']
    trainer = Trainer('./static/questionnaireProcessed.csv')
