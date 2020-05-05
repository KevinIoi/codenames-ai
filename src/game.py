from board import Board
import numpy as np
import random
import json
from exceptions import InvalidBoardException

DATAPATH = "../resources/"

class Game(object):
    
    def __init__(self,board_dim = 5, target_count = 8, bomb_count = 3):
        self.gameword_lexicon = self.loadGameWords()
        self.setGameStructure(board_dim, target_count, bomb_count)
        self.resetBoard()
    
    def setGameStructure(self, board_dim, target_count, bomb_count):
        ''' define the parameters of the game '''
        self.board_dim = board_dim
        self.target_count = target_count
        self.bomb_count = bomb_count
    
    def resetBoard(self):
        ''' reset gameboard '''
        gamewords = np.random.choice(self.gameword_lexicon, size=self.board_dim**2, replace=False)
        player_target, player_bomb = self.createTargetBombWords(gamewords)
        comp_target, comp_bomb = self.createTargetBombWords(gamewords)
        
        self._player_board = Board(gamewords, player_target, player_bomb)
        self._comp_board = Board(gamewords, comp_target, comp_bomb)
    
    def createTargetBombWords(self, gamewords):
        ''' Randomly select target and bomb words from currect game_word sellection'''
        target_words = np.random.choice(gamewords, size=self.target_count, replace=False)
        bomb_words = random.sample(set(gamewords).difference(set(target_words)), self.bomb_count)
        return target_words, bomb_words
        
    def loadGameWords(self):
        ''' loads list of possible game words '''
        with open(f"{DATAPATH}lexicon.txt",'r') as fp:
            gameword_lexicon = json.load(fp)
        return gameword_lexicon

    def getStrBoard(self, player):
        ''' gets the board for a specifiv player

            param:
                player (int):
                    0 for human player's board
                    1 for ai player's board
        '''
        if player == 0:
            return str(self.getPlayerBoard())
        elif player == 1:
            return str(self.getComBoard())
        else:
            raise InvalidBoardException(f"No Board Exists for player {player}")

    def guessTargetWords(self, words, player=0):
        self.getPlayerBoard(player).addGuess(words)
        boardStatus = self.getPlayerBoard(player).validateBoard()



        pass

    # Getters
    def getPlayerBoard(self):
        return self._player_board
    def getCompBoard(self):
        return self._comp_board