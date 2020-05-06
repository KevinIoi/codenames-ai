from ai import ComputerPlayer
from game import Game

class GameMaster(object):
    
    def __init__(self, *args):
        print("Preparing Game...")
        self._ai = ComputerPlayer()
        self.setNewGame()

    def setNewGame(self):
        ''' sets board '''
        self._game = Game()
    
    def submitClue(self,clue_word, target_count, player):
        ''' sends clue to ai to predict associated target_words '''

        activeGameWords = self._game.gameboard.getGameWords(active=True)
        guesses = self._ai.evaluateClue(activeGameWords, clue_word, target_count)
        self._game.guessTargetWords(guesses, player=player)

    def getClue():
        ''' pulls clue from ai for current target words '''
        activeGameWords = self._game.gameboard.getGameWords(active=True)
        guesses = self._ai.getClue(activeGameWords, target_words, bomb_words)
    
    def checkGameState(self):
        ''' evaluates the game state based off the current board '''
        state = self._game.getGameState()
        print(state)
        return state 

    def drawBoard(self,player=1):
        return self._game.getStrBoard(player)
