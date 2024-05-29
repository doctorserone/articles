import os

from tictactoe import TicTacToe

# -------------------------------------------------------------------------------------------

def playerPlay(game, symbol):
    validMove = False
    while not validMove:
        position = int(input(f'Player {symbol}: Make your move (from 0 to 8): '))

        #x, y = map(int, input(f'Player {symbol}: Make your move (x,y from 1 to 3): ').split(","))
        #position = ((x-1)*3)+(y-1)
        
        validMove = game.makeMove(symbol, position)
        if validMove:
            print(f"Player {symbol}: Plays {symbol} at position {position} | State: {game.board}")
            game.dumpBoard()

        else:
            print(f"Player {symbol}: Invalid move at position {position}! | State: {game.board}")

    return game.checkGameOver()

# -------------------------------------------------------------------------------------------

emptyBoard = "EEEEEEEEE"
game = TicTacToe(emptyBoard)

player = 'O'
while not game.checkGameOver() and not game.noPossibleMove():
    position = playerPlay(game, player)

    if game.checkGameOver():
        print(f"Player {player} wins!")
        break

    player = ('O' if player == 'X' else 'X')
