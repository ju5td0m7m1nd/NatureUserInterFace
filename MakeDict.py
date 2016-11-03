import pickle

dictionary = {
    'before': [
        'how to describe keyword',
        'which word can describe keyword',
        'please give me a word can describe keyword',
        'how keyword',
        'what can I do with role',
        'what go before keyword'
    ], 
    'after': [
        'what can be described by keyword',
        'what goes after the word keyword',
        'what go after keyword'
    ], 
    'both': [
        'what nouns usually go with keyword'
        'what go with keyword',
    ]
}

pickle.dump( dictionary, open( "./static/SentenceDict.p", "wb" ) )
