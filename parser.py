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
 
    def __init__(self,filename,PARSEDATA):
        self.fileName = filename 
        self.sentenceLevel = ['S','SBAR','SBARQ','SINV','SQ']
        self.phraseLevel = ['ADJP','ADVP','CONJP','FRAG','INTJ','LST','NAC','NP','NX','PP','PRN','PRT','QP','RRC','UCP','VP','WHADJP','WHAVP','WHNP','WHPP','X']
        self.wordLevel=['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS','PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']
        self.ReadDataFromJson()
        self.ReadQuestionFromFile()
        '''
        if user just need to use the feature,
        pass the parameter PARSEDATA with FALSE.
        '''
        if PARSEDATA:
            self.ParseData()
 
    def ReadQuestionFromFile(self):
        f = open(self.fileName, 'r')  
        question =[] 
        for row in csv.reader(f):
            question.append(row[3:])
        self.question = question
        f.close() 
   
    def ParseData(self):
        questionParsed = []
        print('Parsing.')
        for q in self.question[1:]:
            try:
                print '.'
                question = dep_parser.raw_parse(q[0])
                questionParsed.append(question)
            except:
                continue
        self.questionParsed = questionParsed 
    def SaveToJson(self):  
        questionFeature = []  
        for q in self.questionParsed:
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
             questionFeature.append(feature)
        f = open('feature.data','wb')
        json.dump(questionFeature,f)
        f.close()
    def ReadDataFromJson(self):
        Feature_json = open('feature.data').read()
        self.questionFeature = json.loads(Feature_json) 
    
    def MakeFeature(self):
        for feature in self.questionFeature: 
            for key in feature:
                print key 

    def __PrintProduction__(self):
        for q in self.questionParsed:
            for tree in list(q):
                print tree.productions()
    def __PrintPos__(self):
        for q in self.questionParsed:
            for tree in list(q):
                print tree.pos()

if __name__ == "__main__":
    FP = FeatureParser('questionary.csv',False)
    FP.MakeFeature()
    # test for print production
    #FP.__PrintProduction__()
    # test for print pos
    #FP.__PrintPos__()
