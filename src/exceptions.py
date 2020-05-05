# exceptions

class InvalidBoardException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
    def __str__(self):
        return self.message
    
class InvalidGuessException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
    def __str__(self):
        return self.message

class InvalidPlayerException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
    def __str__(self):
        return self.message