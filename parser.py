import nltk
from nltk.parse.stanford import StanfordParser
import json
import os
import csv
os.environ['STANFORD_PARSER'] = './stanford-parser/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = './stanford-parser/stanford-parser-3.5.2-models.jar' 
dep_parser = StanfordParser(model_path='./stanford-parser/englishPCFG.ser.gz')

sentence_level = ['S','SBAR','SBARQ','SINV','SQ']

tagList = {'PRP$': 2, 'FW': 4, 'WP': 5, 'VBN': 1, 'POS': 1, 'VBP': 1, 'WDT': 1, 'JJ': 1, 'VBZ': 1, 'VBG': 1, 'DT': 1, 'RP': 1, '$': 1, 'NN': 1, 'RBR': 1, 'VBD': 1, ',': 1, '.': 1, 'TO': 1, 'LS': 1, 'RB': 1, 'NNS': 1, 'NNP': 1, 'VB': 1, 'WRB': 1, 'CC': 1, 'PDT': 1, 'RBS': 1, 'PRP': 1, 'CD': 1, 'EX': 1, 'IN': 1, 'WP$': 1, 'MD': 1, 'NNPS': 1, 'JJS': 1, 'JJR': 1, 'SYM': 1, 'UH': 1}
f = open('questionary.csv', 'r')  
Question =[] 
for row in csv.reader(f):
    Question.append(row[3:])


QuestionFeature = []

for q in Question[1:2]:
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


print QuestionFeature  
