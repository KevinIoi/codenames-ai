from utils import cosine_dist, euc_dist
import numpy as np
import pickle
from tqdm import tqdm
from collections import defaultdict

DATAPATH = "../resources/"

class ComputerPlayer(object):
    
    def __init__(self, ):
        self.loadEmbeddings()
        
    def loadEmbeddings(self):
        ''' Prepares embeddings '''

        # embeddings_index = dict()
        # with open(f'{DATAPATH}glove.6B.300d.txt',encoding="utf8") as fp:
        #     for line in tqdm(fp,total=400000,position=0, leave=True):
        #         values = line.split()
        #         word = values[0]
        #         coefs = np.asarray(values[1:], dtype='float32')
        #         embeddings_index[word] = coefs

        with open(f"{DATAPATH}word_vecs.pickle","rb") as fp:
            embeddings_index = pickle.load(fp)

        self.word_vecs = embeddings_index
    
    def produceClue(current_bouard):
        ''' Creates a clue based on current game board '''
        pass

    def evaluateClue(self,current_board, clue_word, target_count):
        ''' Processes a clue provided from other player'''
        
        ranked_words = self.rankWordAssociation(current_board.getGameWords(active=True), clue_word)

        best_guesses = ranked_words[:target_count]

        return [guess[0] for guess in best_guesses]

    def rankWordAssociation(self, lexicon, target_word):
        e_dist = []
        c_dist = []

        for word in lexicon:
            c_dist.append((cosine_dist(self.word_vecs[word], self.word_vecs[target_word]), word))
            e_dist.append((euc_dist(self.word_vecs[word], self.word_vecs[target_word]), word))

        e_dist =sorted(e_dist, key=lambda x: x[0])
        c_dist =sorted(c_dist, key=lambda x: x[0], reverse=True)

        topWords = defaultdict(lambda: 0.0)
        value = 1.0
        for eword, cword in zip(e_dist, c_dist):
            topWords[cword[1]] += value
            topWords[eword[1]] += value*0.75
            value = max([0.2, value-0.1])

        ranked_similarity = sorted(topWords.items(), key=lambda x: x[1], reverse=True)

        return ranked_similarity