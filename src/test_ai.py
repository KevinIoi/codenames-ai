
import gamemaster

def main():
	gm=gamemaster.GameMaster()

	print(gm.drawBoard(player=2))
	print(gm.getClue())

if __name__ == '__main__':
	main()