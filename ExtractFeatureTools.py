
# a tool to find the nearest part of speach you want to the keyword
class SpecPosFinder():
    # get the specified part of speach words position
    def GetTargets(self, partOfSpeach, label, questionPos):
        targets = []
        for i in range(0, len(questionPos)):
            if questionPos[i][1][0] in partOfSpeach and label[i] != 'T':
                targets.append({'word': questionPos[i][0], 'position': i})
        return targets

    # return minimum distance of a word to keyword
    def DistanceToKeyword(self, position, label):
        keywording = False
        keywordPos = []
        for i in range(0, len(label)):
            if label[i] == 'F':
                if keywording and not (i-1) in keywordPos:
                    keywordPos.append(i-1)
                keywording = False
            elif label[i] == 'T':
                if not keywording:
                    keywordPos.append(i)
                keywording = True
        
        minDistance = 100000
        distance = 0
        for kp in keywordPos:
            if abs(position - kp) < minDistance:
                minDistance = abs(position - kp)
        return minDistance

    # find the nearest one
    def GetNearest(self, partOfSpeach, label, questionPos):
        targets = self.GetTargets(partOfSpeach, label, questionPos)
         
        minDistance = 100000
        word = ''
        for target in targets:
            if self.DistanceToKeyword(target['position'], label) < minDistance:
                position = target['position']
                word = target['word']
        if len(targets) == 0:
            return 'No specified part-of-speach'
        else:
            return word

    def GetAll(self, partOfSpeach, label, questionPos):
        targets = self.GetTargets(partOfSpeach, label, questionPos)
        targetWords = []
        for target in targets:
            targetWords.append(target['word'])
        return targetWords

# a tool to count the similarity between two words
class WordRelationCounter():
    def FindSimilarity(self, word1list, word2, partOfSpeach, wn):
        maxSimilarity = 0
        for word1 in word1list:
            maximum = 0
            for i in wn.synsets(word1, partOfSpeach):
                for j in wn.synsets(word2, partOfSpeach):
                    similarity = wn.path_similarity(i, j)
                    if similarity > maximum:
                        maximum = similarity
            print "Similarity between '" + word1 + "' and '" + word2 + "' = " + str(maximum)
            if maximum > maxSimilarity:
                maxSimilarity = maximum
        return maxSimilarity
