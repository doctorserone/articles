import numpy as np
from tensorflow.keras.models import load_model
import os
import random

from dragonagent import DragonAgent
from tictactoe import TicTacToe

# -------------------------------------------------------------------------------------------

def boardToState(board):
    state = []

    for cell in board:
        if cell == 'E':
            state.append(0)
        elif cell == 'X':
            state.append(1)
        elif cell == 'O':
            state.append(-1)

    return state

# -------------------------------------------------------------------------------------------

def agentPlay(game, agent, symbol):
    validMove = False
    while not validMove:
        position = agent.start(boardToState(game.board))
        
        validMove = game.makeMove(symbol, position)
        if validMove:
            print(f"Agent: Plays {symbol} at position {position} | State: {game.board}")
            game.dumpBoard()

        else:
            print(f"Agent: Invalid move at position {position}! | State: {game.board}")

    return game.checkGameOver()

# -------------------------------------------------------------------------------------------

def playerPlay(game, symbol):
    validMove = False
    while not validMove:    
        x, y = map(int, input(f'Player: Make your move (x,y from 1 to 3): ').split(","))
        position = ((x-1)*3)+(y-1)
        
        validMove = game.makeMove(symbol, position)
        if validMove:
            print(f"Player: Plays {symbol} at position {position} | State: {game.board}")
            game.dumpBoard()

        else:
            print(f"Player: Invalid move at position {position}! | State: {game.board}")

    return game.checkGameOver()

# -------------------------------------------------------------------------------------------

agent = DragonAgent()
if os.path.exists('dragon.keras'):
    agent.model = load_model('dragon.keras')

emptyBoard = "EEEEEEEEE"
game = TicTacToe(emptyBoard)

agentIsO = random.choice([True, False])
print(f"NOTE: The initial player is the {'dragon' if agentIsO else 'player'}")

while not game.checkGameOver() and not game.noPossibleMove():
    if agentIsO:
        # Give an immediate reward on 1 if the agent wins
        position = agentPlay(game, agent, 'O')
        if game.checkGameOver():
            print(f"Agent wins! Agent's reward is: +1")
            agent.learn(boardToState(game.board), position, 1, None)
            break

        # Give an immediate penalty regard on -1 if the player wins
        position = playerPlay(game, 'X')
        if game.checkGameOver():
            print(f"Player wins! Agent's reward is: -1")
            agent.learn(boardToState(game.board), position, -1, None)
            break

    else:
        # Give an immediate penalty regard on -1 if the player wins
        position = playerPlay(game, 'O')
        if game.checkGameOver():
            print(f"Player wins! Agent's reward is: -1")
            agent.learn(boardToState(game.board), position, -1, None)
            break

        # Give an immediate reward on 1 if the agent wins
        position = agentPlay(game, agent, 'X')
        if game.checkGameOver():
            print(f"Agent wins! Agent's reward is: +1")
            agent.learn(boardToState(game.board), position, 1, None)
            break

    # If no one wins, give a reward of 0
    print(f"Nobody wins in this turn, play another one. Agent's reward is: 0")
    agent.step(boardToState(game.board), 0)

if agentIsO:
    print(f'Game over! Winner: {"Player" if game.winner == "X" else "Dragon"} ({game.winner})')
else:
    print(f'Game over! Winner: {"Player" if game.winner == "O" else "Dragon"} ({game.winner})')

agent.model.save('dragon.keras')
