from FeatureExtractor import FeatureExtractor
from ClassifiedManager import ClassifiedManager
#from KeywordExtractor import *
import pickle
import os

class MainApp():
    def __init__(self):
        #self.KE = KeywordExtractor()
        self.FE = FeatureExtractor()
        print "Main App: Feature Extractor init"
        MODEL_PATH = ''
        if 'NatureUserInterface' in os.environ['PWD']:
          MODEL_PATH = './'
        else :
          MODEL_PATH = os.path.abspath(os.path.dirname(__name__)) + '/Main/NatureUserInterface/'
        self.loaded_model = pickle.load(open(MODEL_PATH+'model.sav', 'rb'))
        print "Main App: Model loaded "
        self.CM = ClassifiedManager()
        print "Main App: Classified Manager init"
    def Input(self, question):

        #self.KE.Input(question)
        #self.keyword = self.KE.Predict()
        #print self.keyword
        feature = [self.FE.GetFeature(question)]
        typeOfQuestion = self.loaded_model.predict(feature)[0]
        return self.CM.Classify(typeOfQuestion, question, self.FE.GetKeyword())

if __name__ == "__main__":
    question = ['which one is right, "listen to music" or "listen music"', 'how to describe "beach"', 'how to use "possible"', '"too premature in" or "too premature to", which one is right?', 'how to replace "happy" in "I am happy about"', 'Which word can I replace "happy" in "I am happy about"', '"in the afternoon" or "at the afternoon"', 'describe "beach"']
    mainApp = MainApp()
    #for q in question:
    #    print mainApp.Input(q)
    while True:
        print mainApp.Input(raw_input())
