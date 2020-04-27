/**
	Word_Affliation_AI, gameboard.cpp



	@author Kevin ioi
	@version 1.0
*/

#include <string>
#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <Python.h>

using namespace std;

struct GameBoard{
	string *board;
	int *target_words;
	int *bomb_words;
};

class GameController{
	map <string, int> wordDict;
	struct GameBoard board;


	/**

		@return a generated gameboard
	*/
	struct GameBoard resetGame(){

		return NULL;
	}
};