from FeatureExtractor import FeatureExtractor
from ClassifiedManager import ClassifiedManager
#from KeywordExtractor import *
import pickle
import os
from nltk.corpus import wordnet as wn



class MainApp():
    def __init__(self):
        #self.KE = KeywordExtractor()
        self.wn = wn.synsets('describe','v')
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
        #try:
        feature = [self.FE.GetFeature(question, wn)]
        typeOfQuestion = self.loaded_model.predict(feature)[0]
        return {
          'parse': True,
          'command': self.CM.Classify(typeOfQuestion, question, self.FE.GetKeyword())
        }
        '''
        except:
            # Default command _ _ keyword _ _
            # We should predict a most related command to user
            return {
              'parse': False,
              'command': '_ _ '+ self.FE.GetKeyword()[0] + ' _ _'
            }
        '''

if __name__ == "__main__":
    mainApp = MainApp()
    while True:
        print mainApp.Input(raw_input())
