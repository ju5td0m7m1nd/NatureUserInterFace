from nltk.parse.stanford import StanfordParser
 
#dep_parser = StanfordParser('stanford-parser.jar', 'stanford-parser-3.5.2-models.jar')
input1 = raw_input()
input2 = raw_input()
sentences = dep_parser.raw_parse_sents((input1, input2))

a = iter(sentences)

for i in a:
    b = iter(i)
    for j in b:
        print j

