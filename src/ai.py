from utils import cosine_dist, euc_dist
import numpy as np
import os
import pickle
from tqdm import tqdm
from collections import defaultdict
import clustering


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
    
    def produceClue(self,target_words, bomb_words):
        ''' Gets a word that is most related to target_words
            and unrelated to bomb_words

            params:

        '''

        generalized_target_vector, best_target_words = \
            self.getOptimalWordCluster(target_words, bomb_words)

        # use cluster centriod for similarity search on full lexicon
        clue_words = self.rankWordAssociation(list(self.word_vecs.keys()), \
                                            generalized_target_vector, ignore=target_words)

        num_targets = len(best_target_words)

        print(best_target_words)
        return clue_words[0][0], num_targets

    def getOptimalWordCluster(self, target_words, bomb_words):
        ''' Creates clusters of words by cosine similarity, with increasing
            centriod count until a cluster is created containing only target_words

            params:
                target_words (iterable, str):
                    words to maximize in clusters
                bomb_words (iterable, str):
                    words to be avoided in clusters
            returns:
                potential_groups (tuple)
                    A tuple containing the best cluster of words
                    format -> (group center word embedding, list of words in group)
        '''
        if len(target_words) < 1:
            raise ValueError("Empty target word list provided")
        if len(target_words) == 1:
            return target_words[0]

        full_word_set = np.array(target_words+bomb_words)

        embeddings = self.getWordEmbeddings(full_word_set)

        potential_groups = []
        num_groups = 2

        # keep clustering until found a group of similar words without bomb_words
        # increase number of clusters after each failed iteration
        while not potential_groups:
            grouper = clustering.kmeans(k=num_groups, measure='cosine')
            grouper.fit(embeddings)
            cluster_labels = np.array(grouper.train_labels)

            for cluster in np.unique(cluster_labels):
                cluster_indices = cluster_labels==cluster
                current_cluster_words = full_word_set[cluster_indices]

                if len(current_cluster_words)>0 and \
                    not any([word in bomb_words for word in current_cluster_words]):
                    potential_groups.append((grouper.centroids[cluster],current_cluster_words))

            num_groups+=1

        # sort potential_groups by number of group members
        potential_groups = sorted(potential_groups, key=lambda x: len(x[1]))        

        return potential_groups[0]

    def getWordEmbeddings(self, wordList):
        ''' retrieves the stored embedding for each word provided

            params:
                words (list, str):
                    the words to get embeddings for
            returns:
                embeddings (list, array, float):
                    word embeddings
        '''
        if len(wordList) < 1:
            raise ValueError("Empty list provided")

        embeddings = []

        try:
            for word in wordList:
                embeddings.append(self.word_vecs[word])      
        except:
            raise ValueError("Word embeddings not available for all provided words: \
                            {}".format(wordList))

        return embeddings

    def evaluateClue(self,available_words, clue_word, target_count):
        ''' Processes a clue provided from other player

            params:
                available_words (list , str):
                    list of words to compare against clue word
                clue_word (str):
                    word used as base for similarity measure
                target_count (int):
                    number of guess words to be returned 
            returns
                list of available game words found most similar to the clue
        '''
        
        ranked_words = self.rankWordAssociation(available_words, clue_word)

        best_guesses = ranked_words[:target_count]

        return [guess[0] for guess in best_guesses]

    def rankWordAssociation(self, lexicon, target, ignore=[]):
        ''' Ranks list of words by association to the target word.
            Uses a combination of cosine and euclidian distance on word embeddings

            params:
                lexicon (list, str):
                    list of words to rank by similarity
                target (str or array):
                    word to use as target for similarity calculations
                        or
                    embedding to use as target for similarity calculations 
                ignore (list, str):
                    list of words to not include in search
            returns:
                ranked_similarity (list, tuple, (str, float)):
                    List of words ordered by similarity to target, descending   
        '''

        if isinstance(target, str):
            target_vec = self.word_vecs[target_word]
        elif isinstance(target, np.ndarray):
            target_vec = target
        else:
            raise ValueError("Invalid target format provided {} \n must be str or ndarray".format(target))

        euc_rating = []
        cosine_rating = []

        for word in lexicon:# get euc and cosine distance for all words on board
            if word not in ignore: 
                euc_rating.append((euc_dist(self.word_vecs[word], target_vec), word))
                cosine_rating.append((cosine_dist(self.word_vecs[word], target_vec), word))

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