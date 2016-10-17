from nltk.corpus import wordnet as wn
from QuestionTypeTools import FeatureExtractor, Predictor, QueryManager

class MainApp():
    def __init__(self):
        self.wn = wn.synsets('describe','v')
        self.FE = FeatureExtractor()
        print "Main App: Feature Extractor init"
        self.QM = QueryManager()
        print "Main App: Classified Manager init"
        self.predictor = Predictor()
        print "Main App: Predictor init"

    def Input(self, inputQuestion):
        features = [self.FE.GetFeature(inputQuestion, wn)]
        questionType = self.predictor.Predict(features)
        return self.QM.GetQuery(questionType, inputQuestion, self.FE.GetKeyword())

if __name__ == "__main__":
    mainApp = MainApp()
    while True:
        print mainApp.Input(raw_input())
