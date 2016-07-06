import pickle

class WordCluster():
  def __init__(self):
    self.cluster = {}
    self.generateCluster()

  def generateCluster(self):
    self.cluster = pickle.load(open("./static/wordcluster.p", "rb"))
  def returnCluster(self, command):
    if (command == '_all'):
      return self.cluster
    return self.cluster[command]
  def insertWord(self, command, pos, word):
    self.cluster[command][pos].append(word)
    self.writePickle()
  def emptyCluster(self, command, pos):
    self.cluster[command][pos] = []
    self.writePickle()
  def writePickle(self):
    pickle.dump(self.cluster, open("./static/wordcluster.p", "wb"))

if __name__ == '__main__':
    wc = WordCluster()
    wc.generateCluster()
    print wc.returnCluster('_all')
