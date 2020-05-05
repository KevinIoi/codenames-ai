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
    
    def submitClue(self,clue_word, target_count):
        ''' sends clue to ai to predict associated target_words '''
        guesses = self._ai.evaluateClue(self._game.getCompBoard(), clue_word, target_count)
        

        return guesses
      
    def getClue():
        ''' pulls clue from ai for current target words '''
        pass
    
    def checkGameOver(self):
        ''' checks if game state reflects a completed game'''
        return False

    def drawBoard(self,player=0):
        return self._game.getStrBoard(player)
