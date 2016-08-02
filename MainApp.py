from FeatureExtractor import FeatureExtractor
from ClassifiedManager import ClassifiedManager
import pickle

class MainApp():
    def __init__(self):
        self.FE = FeatureExtractor()
        self.loaded_model = pickle.load(open('./model.sav', 'rb'))
        self.CM = ClassifiedManager()
    def Input(self, question):
        feature = []
        feature.append(self.FE.GetFeature(question))
        typeOfQuestion = self.loaded_model.predict(feature)[0]
        return self.CM.Classify(typeOfQuestion, question, self.FE.GetKeyword(question)['keyword'])

if __name__ == "__main__":
    question = ['which one is right, "listen to music" or "listen music"', 'how to describe "beach"', 'how to use "possible"', '"too premature in" or "too premature to", which one is right?', 'how to replace "happy" in "I am happy about"', 'Which word can I replace "happy" in "I am happy about"', '"in the afternoon" or "at the afternoon"', 'describe "beach"']
    mainApp = MainApp()
    for q in question:
        print mainApp.Input(q)
