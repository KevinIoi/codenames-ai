'''
    The Game Board object for codenames
'''

from math import floor
from utils import strikeout

TGREEN =  "\033[32m"
TRED =  "\033[31m"
RESETC = "\033[m"


class Board(object):
    
    def __init__(self, game_words, p1_targets, p1_bombs, p2_targets, p2_bombs):
        self.setGameWords(game_words)
        self.setTargets(p1_targets, 1)
        self.setTargets(p2_targets, 2)    
        self.setBombs(p1_bombs, 1)
        self.setBombs(p2_bombs, 2)
        self.p1_guessedWords = []
        self.p2_guessedWords = []
        
    def setGameWords(self, words):
        ''' setter for full list of game words'''
        set_size = len(words)
        if (set_size**0.5 - floor(set_size**0.5)) != 0:# round about way to verify square gridsize
            raise ValueError(f"Game words can not be fit into square grid\n {words}") 
        if len(set(words)) != len(words):# make sure no duplicate words
            raise ValueError(f"Duplicate game words on board\n {words}")
        self.words = words
            
    def setTargets(self, targets, player):
        ''' setter for target words '''
        if len(set(targets)) != len(targets):# make sure no duplicate words
            raise ValueError(f"Duplicate words in target set\n {targets}")
        if player==1:
            self.p1_targets = targets
        elif player==2:
            self.p2_targets = targets
        else:
            raise ValueError(f"Invalid player given target words <{player}>.\n MUST be 1 or 2")
    
    
    def setBombs(self, bombs, player):
        ''' setter for bomb words '''
        if len(set(bombs)) != len(bombs):# make sure no duplicate words
            raise ValueError(f"Duplicate words in bomb set\n {bombs}")

        if player == 1:
            if any(word in bombs for word in self.p1_targets):
                raise ValueError(f"Overlapping target and bomb sets\n{self.p1_targets}\n{bombs}") 
            self.p1_bombs = bombs
        elif player == 2:
            if any(word in bombs for word in self.p2_targets):
                raise ValueError(f"Overlapping target and bomb sets\n{self.p2_targets}\n{bombs}") 
            self.p2_bombs = bombs
        else:
            raise ValueError(f"Invalid player given bomb words <{player}>.\n MUST be 1 or 2")
    
    def addGuess(self, guess, player):
        ''' adds a list of words to the guessed words'''
        # if guess not in self.getGameWords():
        #     raise ValueError("Guessed word is not on the board")
        # if guess in self.getGuessedWords():
        #     raise ValueError("Guessed word has already been guessed")

        if player == 1:
            self.p1_guessedWords.extend(guess)
        elif player == 2:
            self.p2_guessedWords.extend(guess)
            if guess[0] in self.p2_bombs:
                return "Bomb"
            elif guess[0] in self.p2_targets:
                return "Target"
            else:
                return "Normal"
    
    def getTargets(self, player, active=False):
        ''' getter for target words

            params:
                player (int):
                    the player who's targets to retrieve
                    MUST be 1 or 2
                active (bool):
                    if only the words that have not been guessed should be retrieved
        '''

        if player == 1:
            if active:# only return words that have not been cleared already
                activeWords = list(set(self.p1_targets)-set(self.getGuessedWords()))
                return activeWords
            else:
                return self.p1_targets
        if player == 2:
            if active:# only return words that have not been cleared already
                activeWords = list(set(self.p2_targets)-set(self.getGuessedWords()))
                return activeWords
            else:
                return self.p2_targets
        else:
            raise ValueError("Invalid player chosen. MUST be MUST be \{1,2\}")

    def getBombs(self, player):
        ''' getter for bomb words'''
        if player == 1:
            return self.p1_bombs
        if player == 2:
            return self.p2_bombs
        else:
            raise ValueError("Invalid player chosen. MUST be MUST be \{1,2\}")
    
    def getGameWords(self, active=False):
        ''' getter for current words on board'''
        if active:
            return list(set(self.words)-set(self.getGuessedWords()))
        else:
            return self.words
    
    def getGuessedWords(self, player=None):
        ''' getter for guessed words, will return all guessed words unless a player
            is specified
            
            params:
                player (int):
                    the player who's guessed words should be retrieved
        '''
        if player == 1:
            return self.p1_guessedWords
        elif player == 2:
            return self.p2_guessedWords
        else:
            return self.p1_guessedWords + self.p2_guessedWords

    def validateBoard(self):
        ''' evaluates board to see if game has ended due to bad guess or complete board

            returns:
                gameState (int):
                    Reflects the current state of the game
                        1 -> Valid game, both players have targets remaining  
                        2 -> Valid game, only p1 has targets remaining
                        3 -> Valid game, only p2 has targets remaining
                        4 -> Completed game, p1 bomb word guessed
                        5 -> Completed game, p2 bomb word guessed
                        6 -> Completed game, all targets have been guessed
        '''

        if any(word in self.getGuessedWords(1) for word in self.p1_bombs):
            return 4
        if any(word in self.getGuessedWords(2) for word in self.p2_bombs):
            return 5
        if len(self.getTargets(1, active=True) + self.getTargets(2, active=True)) == 0:
            return 6
        if len(self.getTargets(1, active=True))==0 & len(self.getTargets(2, active=True))==0:
            return 1
        if len(self.getTargets(1, active=True))!=0:
            return 2
        if len(self.getTargets(2, active=True))!=0:
            return 3
        else:
            raise Exception("Whaa!?")

    def getBoardStr(self, player=1):
        ''' Converts current gameboard to string format 
            Defaults to printing player 1's board 
        '''
        out = ''
        rowSize = int(len(self.words)**(0.5))
        for rowIdx in range(0, rowSize):
            for word in self.getGameWords()[rowIdx*rowSize:rowIdx*rowSize+rowSize]:
                               
                # colourize word based on word set
                if word in self.getTargets(player):
                    c = TGREEN
                elif word in self.getBombs(player):
                    c = TRED
                else:
                    c = RESETC
                
                #create strikeout font if word has been guessed 
                if word in self.getGuessedWords():
                    out = "".join([out,c,strikeout('{0:<15}'.format(word))])
                else:
                    out = "".join([out,c,'{0:<15}'.format(word)])

            out = "".join([out, RESETC,'\n'])
        return out

    def __str__(self):
        return self.getBoardStr()
