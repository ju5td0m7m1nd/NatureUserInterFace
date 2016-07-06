import nltk
import json
import os
import csv
import pickle
import json

class Classifier():
    def __init__(self,question):
        self.question = question
    
    def CheckInput(self):
        commandList = [];
        if 'how' in self.question.lower() or 'what' in self.question.lower():
            commandList.append('pos')
            commandList.append('anyWord')
        elif self.question.split(' ')[0] == 'which':
            commandList.append('optionally')
            commandList.append('which')
            commandList.append('similar')
            commandList.append('zero2more')
        return commandList
 
if __name__ == "__main__":
    
    question = raw_input()
    CL = Classifier(question)
    print CL.CheckInput()
    
