from nltk.parse.stanford import StanfordParser
import os
os.environ['STANFORD_PARSER'] = 'standford-parser.jar'
os.environ['STANFORD_MODELS'] = 'stanford-parser-3.5.2-models.jar' 
dep_parser = StanfordParser(model_path='englishPCFG.ser.gz')
s = 'how to describe beach'
sentences = dep_parser.raw_parse(s)

a = iter(sentences)

for i in a:
    b = iter(i)
    for j in b:
        print (j)

