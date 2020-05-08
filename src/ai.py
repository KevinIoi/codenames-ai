from utils import cosine_dist, euc_dist
import numpy as np
import os
import pickle
from tqdm import tqdm
from collections import defaultdict

DATAPATH = "../resources/"

class ComputerPlayer(object):
    
    def __init__(self, ):
        self.loadEmbeddings()
        
    def loadEmbeddings(self):
        ''' Prepares embeddings '''

        #load serialized embeddings if available
        if os.path.exists(os.path.join(DATAPATH,"word_vecs.pickle")):
            with open(f"{DATAPATH}word_vecs.pickle","rb") as fp:
                embeddings_index = pickle.load(fp)

        #load raw embeddings
        elif os.path.exists(os.path.join(DATAPATH, "glove.6B.300d.txt")): 
            embeddings_index = dict()
            with open(os.path.join(DATAPATH, "glove.6B.300d.txt"),encoding="utf8") as fp:
                for line in tqdm(fp,total=400000,position=0, leave=True):
                    values = line.split()
                    word = values[0]
                    coefs = np.asarray(values[1:], dtype='float32')
                    embeddings_index[word] = coefs

            # save serialized object for next time
            with open(f"{DATAPATH}word_vecs.pickle","wb") as fp:
                pickle.dump(embeddings_index, fp)
        else:
            raise EmbeddingNotFoundException(f"No word embeddings found in {DATAPATH}")

        self.word_vecs = embeddings_index
    
    def produceClue(target_words, bomb_words):
        ''' Creates a clue based on current game board '''

        # compare all target_words to eachother

        # save count of words that are a similiarity of >0.7? for each word 

        # cluster possible clue words
        # get optimal cluster of clue words based on that group?



        pass

    def evaluateClue(self,available_words, clue_word, target_count):
        ''' Processes a clue provided from other player

            params:
                current_board (Board)

                clue_word (str)

                target_count (int)

            returns
                list of available game words found most similar to the clue
        '''
        
        ranked_words = self.rankWordAssociation(available_words, clue_word)

        best_guesses = ranked_words[:target_count]

        return [guess[0] for guess in best_guesses]

    def rankWordAssociation(self, lexicon, target_word):
        ''' Ranks list of words by association to the target word.
            Uses a combination of cosine and euclidian distance on word embeddings

            params:
                lexicon (list, str):
                    list of words to rank by similarity
                target_word (str):
                    word to use as target for similarity calculations
            returns:
                ranked_similarity (list, tuple, (str, float)):
                    List of words ordered by similarity to target, descending   
        '''
        euc_rating = []
        cosine_rating = []

        for word in lexicon:# get euc and cosine distance for all words on board
            euc_rating.append((euc_dist(self.word_vecs[word], self.word_vecs[target_word]), word))
            cosine_rating.append((cosine_dist(self.word_vecs[word], self.word_vecs[target_word]), word))

        euc_rating =sorted(euc_rating, key=lambda x: x[0])
        cosine_rating =sorted(cosine_rating, key=lambda x: x[0], reverse=True)

        # word rank is sum of cosine and euc rank
        # euc rank discounted by 0.75 
        topWords = defaultdict(lambda: 0.0)
        value = 1.0
        for eword, cword in zip(euc_rating, cosine_rating):
            topWords[cword[1]] += value
            topWords[eword[1]] += value*0.75
            value = max([0.2, value-0.1])

        ranked_similarity = sorted(topWords.items(), key=lambda x: x[1], reverse=True)

        return ranked_similarity