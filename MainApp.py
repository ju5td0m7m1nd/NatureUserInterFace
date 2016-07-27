from FeatureExtractor import *
import pickle

class MainApp():
    def __init__(self):
        self.FE = FeatureExtractor()
        self.loaded_model = pickle.load(open('./model.sav', 'rb'))
    def Input(self, question):
        feature = self.FE.GetFeature(question)
        print self.loaded_model.predict(feature)

if __name__ == "__main__":
    question = ['which one is right, "listen to music" or "listen music"', 'how to describe "beach"', 'how to use "possible"']
    mainApp = MainApp()
    for q in question:
        mainApp.Input(q)
