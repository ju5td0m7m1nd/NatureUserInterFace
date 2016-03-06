import nltk
import json
tagList = {'PRP$': 2, 'FW': 4, 'WP': 5, 'VBN': 1, 'POS': 1, 'VBP': 1, 'WDT': 1, 'JJ': 1, 'VBZ': 1, 'VBG': 1, 'DT': 1, 'RP': 1, '$': 1, 'NN': 1, 'RBR': 1, 'VBD': 1, ',': 1, '.': 1, 'TO': 1, 'LS': 1, 'RB': 1, 'NNS': 1, 'NNP': 1, 'VB': 1, 'WRB': 1, 'CC': 1, 'PDT': 1, 'RBS': 1, 'PRP': 1, 'CD': 1, 'EX': 1, 'IN': 1, 'WP$': 1, 'MD': 1, 'NNPS': 1, 'JJS': 1, 'JJR': 1, 'SYM': 1, 'UH': 1}

rawText = raw_input()
text = nltk.word_tokenize(rawText)
print(nltk.pos_tag(text))
print("push to git")

