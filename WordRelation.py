'''
This class can calculate a relation between
"User's word" and our "Preserve word"'s relation.

For example, 
the preserver verb contain : describe, elaborate.
Now I want to figure out if the word "modify" can be find
within 5 level of describe and elaborate.
if I find in first level, and the score of "modify" is [describe's score]*1
if find in secord level , the score will be [describe's score] * 0.8, and soon.
'''

'''
WRC stands for word relation calculator
'''
class WRC():

