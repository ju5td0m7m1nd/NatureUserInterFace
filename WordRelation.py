'''
This class can calculate a relation between
"User's word" and our "Preserve word"'s relation.

For example, 
the preserver verb contain : describe, elaborate.
Now I want to figure out if the word "modify" can be find
within 5 level of describe and elaborate.
if I find in first level, and the score of "modify" is [describe's score]*1
if find in secord level , the score will be [describe's score] * 0.8, and soon.
'''

'''
WRC stands for word relation calculator
'''
from nltk.corpus import wordnet as wn

class WRC():
    
    def __init__(self):
        self.level = 0
        pass

    def findLemma(self,word,pos,level,target):
        if level == 5:
            return False
        synsetName = word+'.'+pos+'.01'
        for word in wn.synset(synsetName)._lemma_names:
            print word +' '+target
            if word == target : 
                return level
            #print str(level) +' '+word
            self.findLemma(word,'v',level+1,target) 


if __name__ == '__main__':
    words = ['describe']
    for word in words :
        w = WRC()
        print w.findLemma(word,'v',0,'elaborate') 
