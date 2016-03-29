import nltk
from nltk.parse.stanford import StanfordParser
import matplotlib.pyplot as plt
import json
import os
import csv
import pickle
import json
os.environ['STANFORD_PARSER'] = './stanford-parser/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = './stanford-parser/stanford-parser-3.5.2-models.jar' 
dep_parser = StanfordParser(model_path='./stanford-parser/englishPCFG.ser.gz')

'''
self attribute
@question:
    read question from csv file.
@questionParsed:
    parse question with StanfordParser.
@questionFeature:
    use the label to classify each question's pos,
    sentenceLevel's pos will be use as key in dictionary.
@sentenceLevel:
    part of speech represented of sentence level.
@phraseLevel
    part of speech represented of phrase level.
@wordLevel
    part of speech represented of word level.
'''
class FeatureParser():
 
    def __init__(self,filename,PARSEDATA,command):
        self.fileName = filename
        self.command = command 
        self.sentenceLevel = ['S','SBAR','SBARQ','SINV','SQ']
        self.phraseLevel = ['ADJP','ADVP','CONJP','FRAG','INTJ','LST','NAC','NP','NX','PP','PRN','PRT','QP','RRC','UCP','VP','WHADJP','WHAVP','WHNP','WHPP','X']
        self.wordLevel=['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS','PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']
        self.ReadQuestionFromFile()
        '''
        if user just need to use the feature,
        pass the parameter PARSEDATA with FALSE.
        '''
        if PARSEDATA:
            self.ParseData()
            self.SaveToJson()
        self.ReadDataFromJson()
    def ReadQuestionFromFile(self):
        f = open(self.fileName, 'r')  
        question =[] 
        for row in csv.reader(f):
            question.append(row[3:])
        self.question = question
        f.close() 
   
    # different colums in self.question
    def ParseData(self):
        questionParsed = []
        print('Parsing.')
        for q in self.question[1:30]:
            try:
                print '.'
                question = dep_parser.raw_parse(q[self.command])
                questionParsed.append(question)
            except:
                continue
        self.questionParsed = questionParsed 
    def SaveToJson(self):  
        questionFeature = []  
        for q in self.questionParsed:
             feature = {}
             for question in q:
                q = question
             current_label = '';
             for leaves in q.subtrees():
                 label = leaves.label()
                 if label == 'ROOT':
                      continue
                 elif label in self.sentenceLevel:
                     feature[label] = []
                     current_label = label
                 else :
                     if current_label == '':
                        continue
                     else: 
                        feature[current_label].append(label)
             questionFeature.append(feature)
        f = open('feature'+str(self.command)+'.data','wb')
        json.dump(questionFeature,f)
        f.close()
    def ReadDataFromJson(self):
        Feature_json = open('feature'+str(self.command)+'.data').read()
        self.questionFeature = json.loads(Feature_json) 
    
    def CalculateLayer(self):
        layer = []
        for q in self.questionFeature:
            layer.append(len(q))
        self.layer = layer   
 
    def CalculatePhraseLevel(self):
        phraseLevel = []
        for feature in self.questionFeature:
            count = 0
            for key in feature: 
                for f in feature[key]:
                    if f in self.phraseLevel:
                       count = count +1
            phraseLevel.append(count)
            self.phraseCount = phraseLevel

    def MakeFeature(self):
        for feature in self.questionFeature: 
            for key in feature:
                print key
                print "    "+str(feature[key])
    def __PrintProduction__(self):
        for q in self.questionParsed:
            for tree in list(q):
                print tree.productions()
    def __PrintPos__(self):
        for q in self.questionParsed:
            for tree in list(q):
                print tree.pos()
    def __PrintQuestionParsed__(self):
        for q in self.questionParsed:
            for t in list(q):
                print t    
if __name__ == "__main__":
    
    FP2 = FeatureParser('questionary.csv',True,2)
    FP2.CalculateLayer()
    FP2.CalculatePhraseLevel()
    
    FP4 = FeatureParser('questionary.csv',True,4)
    FP4.CalculateLayer()
    FP4.CalculatePhraseLevel()
     
    plt.scatter(FP2.phraseCount,FP2.layer,color="r")
    plt.scatter(FP4.phraseCount,FP4.layer,color="g")
    
    plt.show()
    # test for print production
    #FP.__PrintProduction__()
    # test for print pos
    #FP.__PrintPos__()
