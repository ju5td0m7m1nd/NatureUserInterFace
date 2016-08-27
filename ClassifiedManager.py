from nltk import pos_tag
from nltk.corpus import wordnet as wn

'''
typeOfQuestion:
0: _ _ possible _ _
1: in/at the afternoon, listen ?to music
2: adj. chair, adv. surprised
3: I am ~happy about
'''

class ClassifiedManager:
    def Classify(self, typeOfQuestion, question, keyword):
        query = ''
        if typeOfQuestion == 0:
            query = self.FirstType(question, keyword)
        elif typeOfQuestion == 1:
            query = self.SecondType(question, keyword)
        elif typeOfQuestion == 2:
            query = self.ThirdType(question, keyword)
        elif typeOfQuestion == 3:
            query = self.ForthType(question, keyword)
        return query
    def FirstType(self, question, keyword):
        query = '_ _ ' + keyword[0] + ' _ _'
        return query
    def SecondType(self, question, keyword):
        query = ''
        first = keyword[0].split()
        second = keyword[1].split()
        if len(first) == len(second):
            for i in range(0, len(first)):
                if first[i] != second[i]:
                    query += first[i] + "/" + second[i] + " "
                else:
                    query += first[i] + " "
        else:
            if len(first) > len(second):
                for word in first:
                    if word not in second:
                        query += "?"
                    query += word + " "
            else:
                for word in second:
                    if word not in first:
                        query += "?"
                    query += word + " "
        return query
    def ThirdType(self, question, keyword):
        query = 'adj. ' + keyword[0]
        return query
    def ForthType(self, question, keyword):
        query = ''
        shorter = ''
        longer = ''
        if len(keyword[0]) > len(keyword[1]):
            longer = keyword[0]
            shorter = keyword[1]
        else:
            longer = keyword[1]
            shorter = keyword[0]
        for word in longer.split():
            if shorter == word:
                query += "~"
            query += word + " "
        return query
