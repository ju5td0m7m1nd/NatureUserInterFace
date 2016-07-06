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
        if 'how' in self.question.lower():
            return 'how'
        elif self.question.split(' ')[0] == 'which':
            return 'which'
 
if __name__ == "__main__":
    
    question = raw_input()
    CL = Classifier(question)
    print CL.CheckInput()
    
