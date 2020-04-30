from ai import ComputerPlayer
from game import Game

class GameMaster(object):
    
    def __init__(self, *args):
        print("Preparing Game...")
        self.ai = ComputerPlayer()
        self.setNewGame()

    def setNewGame(self):
        ''' sets board '''
        self.game = Game()
    
    def submitClue(self,clue_word, target_count):
        ''' sends clue to ai to predict associated target_words '''
        guesses = self.ai.evaluateClue(self.game.getCompBoard(), clue_word, target_count)
        print(guesses)
        
    def getClue():
        ''' pulls clue from ai for current target words '''
        pass
    
    def drawBoard(self,player=0):
        return self.game.getStrBoard(player)
