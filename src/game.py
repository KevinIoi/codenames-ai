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
        ''' creates new board instance '''
        gamewords = np.random.choice(self.gameword_lexicon, size=self.board_dim**2, replace=False)
        player_target, player_bomb = self.createTargetBombWords(gamewords)
        comp_target, comp_bomb = self.createTargetBombWords(gamewords)
        
        self.gameboard = Board(gamewords, player_target, player_bomb, comp_target, comp_bomb)
    
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
        ''' gets the board for a specific player

            param:
                player (int):
                    1 for human player's board
                    2 for ai player's board
        '''
        return str(self.gameboard.getBoardStr(player))

    def guessTargetWords(self, words, player):
        ''' adds guessed words to the board 

            params:
                words (list, str):
                    list of words that were guessed
                player (int):
                    denotes the player who's target words are being guessed (player who provided clue)
        '''         
        self.gameboard.addGuess(words, player)

    def getTargetWords(self, player, active=False):
        return self.gameboard.getTargets(player, active=active)

    def getBombWords(self, player):
        return self.gameboard.getBombs(player)

    def getGameState(self):
        return self.gameboard.validateBoard()