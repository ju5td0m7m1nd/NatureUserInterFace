

class NearestFinder():
    def __init__(self, inputQuestion, label, parsedQuestion):
        self.inputQuestion = inputQuestion
        self.parsedTree = parsedQuestion[0]
        self.label = label
       
    def GetTargetPosition(self, partOfSpeach):
        targetPosition = []
        pos = self.parsedTree.pos() 
        for i in range(0, len(pos)):
            if str(pos[i][1])[0] == partOfSpeach and self.label[i] != 'T':
                targetPosition.append({'word': pos[i][0], 'position': i})
        return targetPosition

    def DistanceToKeyword(self, position):
        keywording = False
        keywordPos = []
        for i in range(0, len(self.label)):
            if self.label[i] == 'F':
                if keywording and not (i-1) in keywordPos:
                    keywordPos.append(i-1)
                keywording = False
            elif self.label[i] == 'T':
                if not keywording:
                    keywordPos.append(i)
                keywording = True
        
        minDistance = 100000
        distance = 0
        for kp in keywordPos:
            if abs(position - kp) < minDistance:
                minDistance = abs(position - kp)
        return minDistance

    def GetNearest(self, partOfSpeach):
        targetPosition = self.GetTargetPosition(partOfSpeach)
         
        minDistance = 100000
        word = ''
        for target in targetPosition:
            if self.DistanceToKeyword(target['position']) < minDistance:
                position = target['position']
                word = target['word']
        if len(targetPosition) == 0:
            return 'No ' + partOfSpeach
        else:
            return word
            
class WordRelationCounter():
    def FindSimilarity(self, word1, word2, partOfSpeach, wn):
        maxSimilarity = 0
        for i in wn.synsets(word1, partOfSpeach):
            for j in wn.synsets(word2, partOfSpeach):
                similarity = wn.path_similarity(i, j)
                if similarity > maxSimilarity:
                    maxSimilarity = similarity
        return maxSimilarity
