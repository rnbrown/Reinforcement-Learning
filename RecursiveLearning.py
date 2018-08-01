import numpy as np
from itertools import product
from TicTacToeGame import TTTBoard, getkey

class Recursivelearning:
    #This will explore all game states recursively
    def __init__(self, Q=None):
        self.Q = Q or self.newQ()
    
    def newQ(self):
        newQ = {}
        for s in product(['a','b','c'], repeat=9):
            key = ''.join(list(s))
            newQ[key] = np.zeros(9)
        return newQ
    
    def recursive_train(self, game, move):
        next_board = game.update(move)
        if next_board.done:
            val = next_board.score()
        else:
            func = {0:max, 1:min}[game.turn]
            val = func([self.recursive_train(next_board, xy) for xy in next_board.allpossible()])      
        self.Q[getkey(game.state)][move[0]*3 + move[1]] = val
        return val   
            
    def train(self):
        game = TTTBoard()
        for move in game.allpossible():
            self.Q[getkey(game.state)][move[0]*3 + move[1]] = self.recursive_train(game, move)
