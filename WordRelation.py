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
import Queue
import collections

class WRC():
    def __init__(self):
        self.level = 0
        pass
    def findLemma(self,word,pos,level,target):
        diffwords = [word]
        q = Queue.Queue()
        prevCount = 0
        nowCount = 0
        tempCount = 0
        nowLevel = 1
        for i in wn.synsets(word, pos):
            for j in i._lemma_names:
                if diffwords.count(j) == 0:
                    diffwords.append(j)
                    print str(nowLevel) + ' ' + word + ' -> '+ j
                    if j == target:
                        return 'Level ' + str(nowLevel) 
                    q.put(j)
                    prevCount += 1
        '''
        for i in wn.synset(word + '.' + pos + '.01')._lemma_names:
            if diffwords.count(i) == 0:
                diffwords.append(i)
                print str(nowLevel) + ' ' + word + ' -> '+ i
                if i == target:
                    return 'Level ' + str(nowLevel) 
                q.put(i)
                prevCount += 1
        '''
        nowLevel += 1
        while not q.empty():
            i = q.get()
            tempCount += 1
            if tempCount > prevCount:
                prevCount = nowCount
                nowCount = 0
                nowLevel += 1
                tempCount = 1;
            if nowLevel > 5:
                return  False
            for j in wn.synsets(i, pos):
                for k in j._lemma_names:
                    if diffwords.count(k) == 0:
                        diffwords.append(k)
                        print str(nowLevel) + ' ' + i + ' -> ' + k
                        if k == target:
                            return 'Level ' + str(nowLevel) 
                        q.put(k)
                        nowCount += 1
            '''
            for j in wn.synset(i + '.' + pos + '.01')._lemma_names:
                if diffwords.count(j) == 0:
                    diffwords.append(j)
                    print str(nowLevel) + ' ' + i + ' -> ' + j
                    if j == target:
                        return 'Level ' + str(nowLevel) 
                    q.put(j)
                    nowCount += 1
            '''

if __name__ == '__main__':
    words = ['describe']
    for word in words :
        w = WRC()
        print w.findLemma(word,'v',0,'elaborate') 
