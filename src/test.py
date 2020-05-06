from gamemaster import GameMaster
import os

def main():
	gm = GameMaster()

	while gm.checkGameState() <= 3:
		os.system('clear')
		print(gm.drawBoard())

		print(f"Enter a clue (single word:")
		word = getStrInput("Please enter a single word", lambda x: len(x.split()) == 1)
		word = word.strip()

		print(f"How many words does this clue apply to?")
		count = getIntInput()

		gm.submitClue(word, count, 1)

def getIntInput(retrymessage = "Enter a valid whole number", vailditiyCheck = lambda x:True):
	''' gets command line int input 

		params:
			retrymessage (str): 
				Message that will be printed out after each invalid input
			vailditiyCheck (func):
				Funciton used to check the validity of the input
	'''
	valid=False

	while not valid:
		num = input()
		try:
			num = int(num.strip())
			if vailditiyCheck(num):
				valid=True
			else:
				valid=False
				print(retrymessage)
		except Exception as e:
			valid = False
			print(retrymessage)
	return num


def getStrInput(retrymessage = "Enter a valid string", vailditiyCheck = lambda x: True):
	''' gets command line string input 

		params:
			retrymessage (str): 
				Message that will be printed out after each invalid input
			vailditiyCheck (func):
				Funciton used to check the validity of the input
	'''
	valid=False
	while not valid:
		strInput = input()
		if vailditiyCheck(strInput):
			valid=True
		else:
			valid=False
			print(retrymessage)
	
	return strInput


if __name__ == '__main__':
	main()