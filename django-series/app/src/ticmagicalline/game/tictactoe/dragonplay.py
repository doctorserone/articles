import random
import numpy as np
from tensorflow.keras.models import load_model
import os

from game.tictactoe.dragonagent import DragonAgent

class DragonPlay:
    def __init__(self, board, type="ai"):
        self.board = board
        self.type = type

    def chooseMovement(self):
        if self.type == "simple":
            return self.simpleMovement()
        else:
            return self.aiMovement()
        
    def getEmptyPositions(self):
        emptyPositions = []

        for i in range(0, 9):
            if self.board[i] == "E":
                emptyPositions.append(i)

        return emptyPositions
      
    def simpleMovement(self):
        emptyPositions = self.getEmptyPositions()
        if len(emptyPositions) == 0:
            print("No empty position to play!")
            return -1
        
        if random.choice([True, False]):
            # Choose the fist empty position and play there
            return emptyPositions[0]
     
        else:
            # Choose a random empty position and play there
            return random.choice(emptyPositions)

    def aiMovement(self):
        emptyPositions = self.getEmptyPositions()
        if len(emptyPositions) == 0:
            print("No empty position to play!")
            return -1
        
        agent = DragonAgent()
        if os.path.exists('/game/tictactoe/model/dragon.keras'):
            agent.model = load_model('/game/tictactoe/model/dragon.keras')

        validMove = False
        position = -1

        while not validMove:
            position = agent.start(self.boardToState(self.board))
            if self.board[position] == "E":
                validMove = True

        return position

    def boardToState(self, board):
        state = []

        for cell in board:
            if cell == 'E':
                state.append(0)
            elif cell == 'X':
                state.append(1)
            elif cell == 'O':
                state.append(-1)

        return state
