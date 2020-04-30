from gamemaster import GameMaster

def getIntInput(retrymessage = "Enter a valid number"):
	valid=False
	while not valid:
		num = input()
		try:
			num = int(num.strip())
			valid=True
		except Exception as e:
			valid = False
			print(retrymessage)
	return num

def main():
	gm = GameMaster()
	print(gm.drawBoard())

	print(f"Enter a clue (single word:")
	word = input()
	word = word.strip()
	print(f"How many words does this clue apply to?")
	count = getIntInput()

	gm.submitClue(word, count)

if __name__ == '__main__':
	main()