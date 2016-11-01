import pickle

dictionary = {
    'before': [
        'how to describe keyword',
        'which word can describe keyword',
        'please give me a word can describe keyword',
        'how keyword'
    ], 
    'after': [
        'what can be described by keyword'
    ], 
    'both': [
        'what verbs go with keyword', 
        'what nouns usually go with keyword'
    ]
}

pickle.dump( dictionary, open( "./static/SentenceDict.p", "wb" ) )
