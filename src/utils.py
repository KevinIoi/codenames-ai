import numpy as np

# utils
def strikeout(word):
    ''' Creates a strikethrough font in terminal '''
    newWord = []
    for char in word:
        if char.isalpha():
            newWord.append(f"\u0336{char}")
        else:
            newWord.append(" ")
    return "".join(newWord)

# Distance Funcs
def cosine_dist(x, y):
    return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))

def euc_dist(x,y):
    return np.sqrt(np.sum((x - y) ** 2))