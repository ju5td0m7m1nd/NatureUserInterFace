import nltk
from nltk.parse.stanford import StanfordParser
import json
import os
import csv
import pickle
import json
os.environ['STANFORD_PARSER'] = './stanford-parser/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = './stanford-parser/stanford-parser-3.5.2-models.jar' 
dep_parser = StanfordParser(model_path='./stanford-parser/englishPCFG.ser.gz')

FILENAME = 'feature.data'

class FeatureParser():

    sentenceLevel = []
    phraseLevel = []
    wordLevel = []
    questionFeature = []   
 
    def InitData(self): 
        self.sentenceLevel = ['S','SBAR','SBARQ','SINV','SQ']
        self.phraseLevel = ['ADJP','ADVP','CONJP','FRAG','INTJ','LST','NAC','NP','NX','PP','PRN','PRT','QP','RRC','UCP','VP',
                        'WHADJP','WHAVP','WHNP','WHPP','X']
        self.wordLevel=['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS','PRP','PRP$','RB',
                    'RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']

    def ReadDataFromFile(self):
        f = open('questionary.csv', 'r')  
        Question =[] 
        for row in csv.reader(f):
            Question.append(row[3:])
        QuestionFeature = []
        for q in Question[1:]:
            try:
                questionParsed = dep_parser.raw_parse(q[0])
                for q in questionParsed:
                    feature = {}
                    current_label = '';
                    for leaves in q.subtrees():
                        label = leaves.label()
                        if label == 'ROOT':
                             continue
                        elif label in sentence_level:
                            feature[label] = []
                            current_label = label
                        else :
                            feature[current_label].append(label)
                    QuestionFeature.append(feature)
            except:
                continue

        f = open(FILENAME,'wb')
        json.dump(QuestionFeature,f)
        f.close()
    def ReadDataFromJson(self):
        Feature_json = open(FILENAME).read()
        self.questionFeature = json.loads(Feature_json) 
    def __PrintData__(self):
        
        print self.questionFeature

FP = FeatureParser()
FP.ReadDataFromJson()

for f in FP.questionFeature:
    print f

