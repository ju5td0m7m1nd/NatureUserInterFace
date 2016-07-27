from nltk.corpus import wordnet as wn

word = 'describe'


'''
describe = wn.synset('describe.v.01')
depict = wn.synset('depict.v.01')
print describe
for i in wn.synsets(word, 'v'):
    print '------------------------------' 
    print i
    print wn.path_similarity(i, describe)
    for j in i._lemma_names:
        print j + str(wn.path_similarity())

'''

word1 = 'replace'
word2 = 'change'

maximum = 0
for i in wn.synsets(word1, 'v'):
    for j in wn.synsets(word2, 'v'):
        similarity = wn.path_similarity(i, j)
        print str(i) + " and " + str(j) + ": " + str(similarity)
        if similarity > maximum:
            maximum = similarity
print maximum
