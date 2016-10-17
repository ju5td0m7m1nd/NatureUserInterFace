from nltk.corpus import wordnet as wn
from QuestionTypeTools import FeatureExtractor, Predictor, QueryManager

class MainApp():
    def __init__(self):
        #activate wordnet
        self.wn = wn.synsets('describe','v')
        self.FE = FeatureExtractor()
        print "Main App: Feature Extractor init"
        self.QM = QueryManager()
        print "Main App: Classified Manager init"
        self.predictor = Predictor()
        print "Main App: Predictor init"

    #user input entry point
    def Input(self, inputQuestion):
        #get collected features
        features = [self.FE.GetFeature(inputQuestion, wn)]
        #predict question type
        questionType = self.predictor.Predict(features)
        #return processed query
        return self.QM.GetQuery(questionType, inputQuestion, self.FE.GetKeyword())

if __name__ == "__main__":
    mainApp = MainApp()
    while True:
        print mainApp.Input(raw_input())
