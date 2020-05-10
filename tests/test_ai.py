
import gamemaster

def main():
	gm=gamemaster.GameMaster()

	print(gm.drawBoard(player=1))
	print(gm.getClue())

if __name__ == '__main__':
	main()