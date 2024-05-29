class TicTacToe:
    def __init__(self, board):
        self.board = board
        self.winner = ""

    def checkMove(self, position):
        if self.board[position] == "E":
            return True
        
        return False

    def makeMove(self, symbol, position):
        if position >= 0 and position <=8 and self.board[position] == "E":
            self.board = self.board[:position]+symbol+self.board[position+1:]
            return True
        
        return False

    def freeBoardPositions(self):
        freePositions = 0

        for i in range(0, 9):
            if self.board[i] == "E":
                freePositions += 1
        
        return freePositions
    
    def getUniquePossibleMovement(self):
        for i in range(0, 9):
            if self.board[i] == "E":
                return i
    
        return -1

    def noPossibleMove(self):
        for i in range(0, 9):
            if self.board[i] == "E":
                return False
        
        return True

    def checkGameOver(self):
        for i in range(0, 3):
            # Vertical line
            if self.board[i] != "E" and self.board[i] == self.board[i+3] and self.board[i] == self.board[i+6]:
                self.winner = self.board[i]
                return True
            
            # Horizontal line
            if self.board[i*3] != "E" and self.board[i*3] == self.board[i*3+1] and self.board[i*3] == self.board[i*3+2]:
                self.winner = self.board[i*3]
                return True
            
        # Diagonal lines
        if self.board[0] != "E" and self.board[0] == self.board[4] and self.board[0] == self.board[8]:
            self.winner = self.board[0]
            return True
        
        elif self.board[2] != "E" and self.board[2] == self.board[4] and self.board[2] == self.board[6]:
            self.winner = self.board[2]
            return True
        
        # No more spaces to play
        for i in range(0, 9):
            if self.board[i] == "E":
                return False

        self.winner = "D"
        return True

    def dumpBoard(self):
        for i in range(0, 3):
            print(f"|{self.board[i*3]}|{self.board[i*3+1]}|{self.board[i*3+2]}|")
