from WordRelation import *
from FindNearest import *
from Classifier import *
from WordCluster import *

class MainApp():
    def __init__(self, question):

        self.keyword = re.findall('"([^"]*)"', question)
        self.question =  question.replace('\"', '')

        self.classifier = Classifier(self.question, self.keyword)
        self.queryList = self.classifier.GetQueryList()

if __name__ == '__main__':
    question = []
    question.append('how to describe "beach"')
    question.append('which one is right, "listen to music" or "listen music"')
    question.append('"in the afternoon" or "at the afternoon"')
    mainApp = MainApp(question[2])
