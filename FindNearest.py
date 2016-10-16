
class FindNearest():
    def __init__(self, question, label, questionParsed):
        self.questionParsed = questionParsed
        self.question = question
        self.label = label
        self.verbsPosition = []
        self.parsedTree = []
        self.ParseData()
        self.GetVsPosition()
        
    def ParseData(self):
        #print 'parsing data...'
        #self.questionParsed = dep_parser.raw_parse(self.question)
        for q in self.questionParsed:
            self.parsedTree = q
        print 'finish parsing data'

    def GetVsPosition(self):
        verbsPosition = []
        leaf_values = self.parsedTree.leaves()
        pos = self.parsedTree.pos()
        for i in range(0, len(pos)):
            if str(pos[i][1])[0] == 'V' and self.label[i] != 'T':
                verbsPosition.append({'word': pos[i][0], 'position': i})
        self.verbsPosition = verbsPosition

    def GetNearest(self):
        keywordPos = 0
        for i in range(0, len(self.label)):
            if self.label[i] == 'T':
                keywordPos = i
                break
        position = 100000
        word = ''
        for pairs in self.verbsPosition:
            if abs(pairs['position'] - keywordPos) < abs(position - keywordPos):
                position = pairs['position']
                word = pairs['word']
        if len(self.verbsPosition) == 0:
            return 'No verb'
        else:
            return word
