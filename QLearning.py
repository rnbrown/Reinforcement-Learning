import numpy as np
from itertools import product
from TicTacToeGame import TTTBoard, getkey
    
class Qlearning:
    def __init__(self, random_rate=None, decay_rate=None, learning_rate=None, Q=None):
        self.random_rate = random_rate or .2
        self.decay_rate = decay_rate or .95
        self.learning_rate = learning_rate or .8
        self.Q = Q or self.newQ()
    
    def newQ(self):
        newQ = {}
        for s in product(['a','b','c'], repeat=9):
            key = ''.join(list(s))
            newQ[key] = (np.random.rand(9) -.5) * .3
        return newQ 

    def action(self, board):
        if np.random.rand() <= self.random_rate:
            xy = board.allpossible()[np.random.randint(len(board.allpossible()))]
        else:
            start = getkey(board.state)
            if board.turn == 1:
                i = np.argmax(self.Q[start])
            else:
                i = np.argmin(self.Q[start])
            xy = (i//3, i%3)
        return xy
        
    def simulate_game(self):
        #create new board, play 1 full game and update Q with each step
        board = TTTBoard()
        while not board.done:
            xy = self.action(board)
            if not board.possible(xy):
                self.Q[getkey(board.state)][3*xy[0]+xy[1]] = .5 - board.turn
            else:
                board = board.update(xy)
                self.updateQ(board)
    
    def updateQ(self, game):
        #unpack
        #player turn made move, taking the board from state s_prev to s
        hist = game.history[-1]
        s_prev, move, s, score = getkey(hist['s_prev']), hist['move'], getkey(hist['s']), hist['score']
        move = 3*move[0] + move[1]
        #update Q table
        if game.done:
            self.Q[s_prev][move] = score 
        else:
            func = {0:min, 1:max}[game.turn]
            expected = self.decay_rate * func(self.Q[s])
            self.Q[s_prev][move] *= (1 - self.learning_rate)
            self.Q[s_prev][move] += self.learning_rate * expected
        