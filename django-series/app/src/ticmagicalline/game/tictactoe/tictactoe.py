class TicTacToe:
    def __init__(self, board):
        self.board = board
        self.winner = ""

    def checkMove(self, position):
        if self.board[position] == "E":
            return True
        
        return False

    def makeMove(self, symbol, position):
        if self.checkMove(position):
            self.board = self.board[:position]+symbol+self.board[position+1:]
            print(f"The player {symbol} makes a move at position {position}. Current board: [{self.board}]")
            return True
        
        print(f"Invalid movement! The position {position} is already occupied. Current board: [{self.board}]")
        return False

    def checkGameOver(self):
        for i in range(0, 3):
            # Vertical line
            if self.board[i] != "E" and self.board[i] == self.board[i+3] and self.board[i] == self.board[i+6]:
                self.winner = self.board[i]
                print(f"Win condition reached (vertical line)! Winner: {self.winner} | Current board: [{self.board}]")
                return True
            
            # Horizontal line
            if self.board[i*3] != "E" and self.board[i*3] == self.board[i*3+1] and self.board[i*3] == self.board[i*3+2]:
                self.winner = self.board[i*3]
                print(f"Win condition reached (horizontal line)! Winner: {self.winner} | Current board: [{self.board}]")
                return True
            
        # Diagonal lines
        if self.board[0] != "E" and self.board[0] == self.board[4] and self.board[0] == self.board[8]:
            self.winner = self.board[0]
            print(f"Win condition reached (diagonal \\ line)! Winner: {self.winner} | Current board: [{self.board}]")
            return True
        
        elif self.board[2] != "E" and self.board[2] == self.board[4] and self.board[2] == self.board[6]:
            self.winner = self.board[2]
            print(f"Win condition reached (diagonal / line)! Winner: {self.winner} | Current board: [{self.board}]")
            return True
        
        # No more spaces to play
        for i in range(0, 9):
            if self.board[i] == "E":
                return False

        self.winner = "D"
        print(f"No more spaces to play, draw! Winner: {self.winner} | Current board: [{self.board}]")
        return True
