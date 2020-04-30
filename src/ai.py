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
    
    def evaluateClue(self,current_board, clue_word, target_count):
        ''' Processes a clue provided from other player'''
        e_dist = []
        c_dist = []

        for word in current_board.getGameWords(active=True):
            c_dist.append((cosine_dist(self.word_vecs[word], self.word_vecs[clue_word]), word))
            e_dist.append((euc_dist(self.word_vecs[word], self.word_vecs[clue_word]), word))

        e_dist =sorted(e_dist, key=lambda x: x[0])
        c_dist =sorted(c_dist, key=lambda x: x[0], reverse=True)
        
        topWords = defaultdict(lambda: 0.0)
        value = 1.0
        for eword, cword in zip(e_dist[:target_count+2], c_dist[:target_count+2]):
            topWords[eword] += value
            topWords[cword] += value*0.75
            value = max([0.2, value-0.2])
        selected_guesses = sorted(topWords.items(), key=lambda x: x[1])[target_count]

        return [guess[0] for guess in selected_guesses]
        
    def produceClue(current_bouard):
        ''' Creates a clue based on current game board '''
        pass