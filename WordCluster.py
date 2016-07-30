import pickle
import os
pickle_path = os.path.abspath(os.path.dirname(__name__))+'/Main/NatureUserInterface/static/'

'''
zero2more
optionally
pos
which
similar
anyword
'''

class WordCluster():
  def __init__(self):
    self.cluster = {}
    self.generateCluster()

  def generateCluster(self):
    print "cluster generating"
    self.cluster = pickle.load(open(pickle_path + "wordcluster.p", "rb"))
    print "load success"
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
    pickle.dump(self.cluster, open(pickle_path + "wordcluster.p", "wb"))

if __name__ == '__main__':
    wc = WordCluster()
    wc.generateCluster()
    print wc.returnCluster('_all')
