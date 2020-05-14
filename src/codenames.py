#!/usr/bin/env python3


from gamemaster import GameMaster
import os

def main():
	gm = GameMaster()
	player_turn = 1

	while gm.checkGameState() <= 3:

		os.system('clear')
		print(gm.drawBoard(player=1))

		if player_turn ==1:
			print("It is your turn to give a clue")
			print(f"Enter a clue (single word:")
			word = getStrInput("Please enter a single word", lambda x: len(x.split()) == 1)
			word = word.strip()

			print(f"How many words does this clue apply to?")
			count = getIntInput()

			guesses = gm.submitClue(word, count, 1)

			print("The computer has guessed: {}".format(" ".join(guesses)))
			print("Press enter to contine...")
			input()
			player_turn = 2
		else:
			print("It is the computer's turn to give a clue")
			print("Please wait while it thinks...")
			clue, target_count = gm.getClue()
			print("The clue is: {}".format(clue))
			if target_count >1:
				print("It is directed at {} target words".format(target_count))
			else:
				print("It is directed at {} target word".format(target_count))

			guess_count = 0
			while guess_count < target_count:
				print("please enter a target word to guess")
				guess = getStrInput()

			player_turn = 1

	


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