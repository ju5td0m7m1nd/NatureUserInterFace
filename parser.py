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
        self.sentenceLevel = {'S':'3','SBAR':'1','SBARQ':'2','SINV':'1','SQ':'1'}
        self.phraseLevel = {'ADJP':'3','ADVP':'3',
                            'CONJP':'3','FRAG':'2',
                            'INTJ':'0','LST':'0',
                            'NAC':'0','NP':'5',
                            'NX':'0','PP':'3',
                            'PRN':'0','PRT':'0',
                            'QP':'0','RRC':'0',
                            'UCP':'0','VP':'5',
                            'WHADJP':'2','WHAVP':'2',
                            'WHNP':'2','WHPP':'2','X':'0'}
        '''
        Coordinating Conjunction: for, and, nor, but, or, yet, so.
        '''

        self.wordLevel={'CC','CD','DT',
                        'EX','FW','IN',
                        'JJ','JJR','JJS',
                        'LS','MD','NN',
                        'NNS','NNP','NNPS',
                        'PDT','POS','PRP',
                        'PRP$','RB','RBR',
                        'RBS','RP','SYM',
                        'TO','UH','VB',
                        'VBD','VBG','VBN',
                        'VBP','VBZ','WDT',
                        'WP','WP$','WRB'}
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
                            phrase_weight = self.phraseLevel.index(f)
                        elif f in self.wordLevel:
                            word_weight = word_weight + self.wordLevel.index(f)
                phraseWeight.append(totalWeight)
        self.phraseWeight = phraseWeight
    def CalculateSentenceWeight(self):
        sentenceWeight = []
        for feature in self.questionFeature:
            total_weight = 0
            for key in feature:
                sentence_weight = self.sentenceLevel.index(key)
                phrase_weight = 0
                for f in feature[key]:
                    if f in self.phraseLevel:
                        phrase_weight = phrase_weight + self.phraseLevel.index(f)
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
    FP[0] = FeatureParser('questionnaire.csv',True,0)
    '''
    for i in range(0,6):
        FP[i] = FeatureParser('questionnaire.csv',False,i)
        FP[i].CalculateSentenceWeight()
        FP[i].CalculatePhraseWeight()
        color = ''
        color_num = i
        for c in range(0,6):
            color_num = color_num+1 
            if color_num >= 10: 
                color_num = 0
            color = color+str(color_num)  
        print len(FP[i].phraseWeight) 
        print len(FP[i].sentenceWeight) 
        plt.figure(i)
        plt.axis((0,10000,0,500))
        plt.scatter(FP[i].phraseWeight,FP[i].sentenceWeight,color="#"+color)
        plt.savefig('command'+str(i)+'.png',bbox_inches='tight')
    '''
    # test for print production
    #FP.__PrintProduction__()
    # test for print pos
    #FP.__PrintPos__()
