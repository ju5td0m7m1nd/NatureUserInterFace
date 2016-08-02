import nltk
from nltk.parse.stanford import StanfordParser
#import matplotlib.pyplot as plt
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
    '''
    Command 0 : _ _ keyword _ _
    Command 1 : keyword/keyword 
    Command 2 : listen ?keyword music
    Command 3 : adj. keyword
    Command 4 : adv. keyword 
    Command 5 : ~keyword
    Command 6 : run out _ 
    '''  
    def __init__(self,filename,PARSEDATA,command):
        self.fileName = filename
        self.command = command
        self.sentenceLevel = {'S':'30','SBAR':'10','SBARQ':'20','SINV':'10','SQ':'10'}
        self.phraseLevel = {'ADJP':'30','ADVP':'30',
                            'CONJP':'30','FRAG':'20',
                            'INTJ':'0','LST':'0',
                            'NAC':'0','NP':'50',
                            'NX':'0','PP':'30',
                            'PRN':'0','PRT':'0',
                            'QP':'0','RRC':'0',
                            'UCP':'0','VP':'50',
                            'WHADJP':'30','WHAVP':'30',
                            'WHNP':'30','WHPP':'30','X':'0'}
        '''
        Coordinating Conjunction: for, and, nor, but, or, yet, so.
        PRP$ : Possessive Pronoun - yours, mine
        Modal : canl, could, may, might, will, would... 
        '''

        self.wordLevel={'CC':'30','CD':'0','DT':'0',
                        'EX':'0','FW':'10','IN':'10',
                        'JJ':'10','JJR':'10','JJS':'10',
                        'LS':'0','MD':'30','NN':'10',
                        'NNS':'10','NNP':'1','NNPS':'10',
                        'PDT':'0','POS':'0','PRP':'0',
                        'PRP$':'0','RB':'1','RBR':'20',
                        'RBS':'20','RP':'0','SYM':'0',
                        'TO':'10','UH':'0','VB':'30',
                        'VBD':'20','VBG':'20','VBN':'20',
                        'VBP':'20','VBZ':'20','WDT':'10',
                        'WP':'10','WP$':'10','WRB':'30'}
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
        for q in self.question[1:]:
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
             current_label = ''
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
        f = open('./features/feature'+str(self.command)+'.data','wb')
        json.dump(questionFeature,f)
        f.close()
    def ReadDataFromJson(self):
        Feature_json = open('./features/feature'+str(self.command)+'.data').read()
        self.questionFeature = json.loads(Feature_json) 
    
    def CalculateLayer(self):
        layer = []
        for q in self.questionFeature:
            layer.append(len(q))
        self.layer = layer   
 
    def CalculatePhraseLevel(self):
        phraseLevel = []
        wordLevel = []
        for feature in self.questionFeature:
            count = 0
            level = 1
            for key in feature: 
                for f in feature[key]:
                    if f in self.phraseLevel:
                        if f in self.questionPhraseLevel:
                            count = count + 2 * level
                        else:
                            count = count +1*level
                level = level+1
            phraseLevel.append(count)
            self.phraseCount = phraseLevel
    def CalculatePhraseWeight(self):
        phraseWeight = []
        for feature in self.questionFeature:
                totalWeight = 0
                for key in feature:
                    phrase_weight = 0
                    word_weight = 0 
                    for f in feature[key]:
                        if f in self.phraseLevel:
                            totalWeight = totalWeight + phrase_weight * word_weight
                            phrase_weight = int(self.phraseLevel[f])
                        elif f in self.wordLevel:
                            word_weight = word_weight + int(self.wordLevel[f])
                phraseWeight.append(totalWeight)
        self.phraseWeight = phraseWeight
    def CalculateSentenceWeight(self):
        sentenceWeight = []
        for feature in self.questionFeature:
            total_weight = 0
            for key in feature:
                sentence_weight = int(self.sentenceLevel[key])
                phrase_weight = 0
                for f in feature[key]:
                    if f in self.phraseLevel:
                        phrase_weight = phrase_weight + int(self.phraseLevel[f])
                total_weight = phrase_weight * sentence_weight
            sentenceWeight.append(total_weight)
        self.sentenceWeight = sentenceWeight 
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
      
    FP = {}
    _StartWithHowQuestion = []
    _WhQuestion = []
    _RemainQuestion = []
    _whWord = ['which','where','who']
    FP = FeatureParser('./static/questionnaire.csv',True,1)
    FP = FeatureParser('./static/questionnaire.csv',True,2)
    FP = FeatureParser('./static/questionnaire.csv',True,3)
    FP = FeatureParser('./static/questionnaire.csv',True,4)
    FP = FeatureParser('./static/questionnaire.csv',True,5)
    FP = FeatureParser('./static/questionnaire.csv',True,6)
    
    
