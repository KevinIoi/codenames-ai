# Paths
INCLUDE=./include/
BIN=./bin/
SRC=./src/

# Compiler settings
CC = g++
CFLAGS = -std=c++11 -Wall -Wextra -Werror -pedantic -I$(INCLUDE)

# Package links
LDFLAGS = -larmadillo -lmlpack


all: controller

controller: $(SRC)gamecontroller.cpp $(INCLUDE)gamecontroller.h
	$(CC) $(CFLAG) -c $(SRC)gamecontroller.cpp -o $(BIN)gamecontroller.o

test:
	$(CC) $(CFLAG) $(SRC)test.cpp -o $(BIN)testme $(LDFLAGS) 

clean:
	-rm -f bin/*.o
	-rm -f bin/*.a
