import pickle

class WordCluster():
  def __init__(self):
    self.cluster = {}

  def generateCluster(self):
    self.cluster = pickle.load(open("./static/wordcluster.p", "rb"))
  def returnCluster(self, command):
    if (command == '_all'):
      return self.cluster
    return self.cluster[command]
  def insertWord(self, command, pos, word):
    self.cluster[command][pos] = word
    self.writePickle
  def writePickle(self):
    pickle.dump(self.cluster, open("wordcluster.p", "wb"))

if __name__ == '__main__':
    wc = WordCluster()
    wc.generateCluster()
    print wc.returnCluster('_all')
