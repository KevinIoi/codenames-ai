CC = g++
INCLUDE=./include/
BIN=./bin/
SRC=./src/

CFLAGS = -Wall -Wextra -Werror -I$(INCLUDE)



all: controller

controller: $(SRC)gamecontroller.cpp $(INCLUDE)gamecontroller.h
	$(CC) $(CFLAG) -c $(SRC)gamecontroller.cpp -o $(BIN)gamecontroller.o

test:
	$(CC) $(CFLAG) $(SRC)test.cpp -o $(BIN)testme

clean:
	-rm -f bin/*.o
	-rm -f bin/*.a
