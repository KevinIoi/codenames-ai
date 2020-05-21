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
        self.submitGuess(guesses, player=player)
        return guesses

    def getClue(self):
        ''' pulls clue from ai for current target words '''
        target_words = self._game.getTargetWords(player=2, active=True)
        bomb_words = self._game.getBombWords(player=2)
        clueWord, num_targets = self._ai.produceClue( target_words, bomb_words)
        return clueWord, num_targets
    
    def checkGameState(self):
        ''' evaluates the game state based off the current board '''
        state = self._game.getGameState()
        print(state)
        return state 

    def submitGuess(self, guesses, player):
        return self._game.guessTargetWords(guesses, player=player)

    def drawBoard(self,player=1):
        return self._game.getStrBoard(player)
