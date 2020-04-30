from exceptions import InvalidBoardException, InvalidGuessException
from math import floor

TGREEN =  "\033[32m"
TRED =  "\033[31m"
RESETC = "\033[m"


class Board(object):
    
    def __init__(self, game_words,targets, bombs):
        self.setGameWords(game_words)
        self.setTargets(targets)    
        self.setBombs(bombs)
        self.guessedWords = []
        
    def setGameWords(self, words):
        ''' setter for full list of game words'''
        set_size = len(words)
        if (set_size**0.5 - floor(set_size**0.5)) != 0:# round about way to verify square gridsize
            raise InvalidBoardException(f"Game words can not be fit into square grid\n {words}") 
        if len(set(words)) != len(words):# make sure no duplicate words
            raise InvalidBoardException(f"Duplicate game words on board\n {words}")
        self.words = words
            
    def setTargets(self, targets):
        ''' setter for target words '''
        if len(set(targets)) != len(targets):# make sure no duplicate words
            raise InvalidBoardException(f"Duplicate words in target set\n {targets}")
        self.targets = targets
    
    def setBombs(self, bombs):
        ''' setter for bomb words '''
        if len(set(bombs)) != len(bombs):# make sure no duplicate words
            raise InvalidBoardException(f"Duplicate words in bomb set\n {bombs}")
        if any(word in bombs for word in self.targets):
            raise InvalidBoardException(f"Overlapping target and bomb sets\n{self.targets}\n{self.bombs}") 
        self.bombs = bombs
        
    def addGuess(self, guess):
        if guess not in self.getGameWords():
            raise InvalidGuessException("Guessed word is not on the board")
        if guess in self.getGuessWords():
            raise InvalidGuessException("Guessed word has already been guessed")
        self.guessedWords.append(guess)
    
    def getTargets(self, remaining=False):
        ''' getter for target words'''
        if remaining:# only return words that have not been cleared already
            idx = [word not in self.getGuessedWords for word in self.targets]
            return self.targets[idx]
        else:
            return self.targets
    
    def getBombs(self):
        ''' getter for bomb words'''        
        return self.bombs
    
    def getGameWords(self, active=False):
        ''' getter for current words on board'''
        if active:
            return [word for word in self.words if word not in self.getGuessedWords()]
        else:
            return self.words
    
    def getGuessedWords(self):
        ''' getter for all guessed words'''
        return self.guessedWords
    
    def __str__(self):
        ''' converts current gameboard to string format '''
        out = ''
        rowSize = int(len(self.words)**(0.5))
        for rowIdx in range(0, rowSize):
            for word in self.getGameWords()[rowIdx*rowSize:rowIdx*rowSize+rowSize]:
                
                #create strikeout font if word has been guessed 
                if word in self.getGuessedWords():
                    writeWord = strikeout(word)
                else:
                    writeWord = word
                
                # colourize word based on word set
                if word in self.getTargets():
                    c = TGREEN
                elif word in self.bombs:
                    c = TRED
                else:
                    c = RESETC
                    
                out = "".join([out,c,'{0:<15}'.format(writeWord)])
            out = "".join([out, RESETC,'\n'])
        return out