import numpy as np
import copy

def getkey(state):
        convert = {-1:'a', 0:'b', 1:'c'}
        char_list = [convert[_] for _ in state.flatten()]
        return ''.join(char_list)
    
class TTTBoard:
    
    def __init__(self, state=None, turn=None, done=None, history=None):
        self.state = state or np.zeros([3,3])
        self.turn = turn or 0
        self.done = done or 0
        self.history = history or []
    
    def reset(self):
        self.__init__()
        
    def score(self):
        #check rows
        for row in self.state:
            sum_i = sum(row)
            if abs(sum_i)==3:
                return np.sign(sum_i)
        #check cols
        for col in self.state.T:
            sum_i = sum(col)
            if abs(sum_i)==3:
                return np.sign(sum_i)
        #check diags
        for d in [0, 1]:
            sum_i = sum([self.state[n, n+d*(2-2*n)] for n in range(3)])
            if abs(sum_i)==3:
                return np.sign(sum_i)
        #no winner
        return 0    
        
    def possible(self, xy):
        #xy is a tuple with coords
        return self.state[xy]==0
    
    def allpossible(self):
        xy = np.where(self.state==0)
        return list(zip(xy[0], xy[1]))
        
    def update(self, xy):
        if self.possible(xy):
            next_board = copy.deepcopy(self)
            s_prev = self.state.copy()
            turn = self.turn
            #turn:0 corresponds with -1, turn:1 corr. w/ 1
            next_board.state[xy] = -1 + 2*self.turn
            next_board.turn = 1 - self.turn
            #update history
            hist = {'s_prev':s_prev,
                   'move':xy,
                   'turn':turn,
                   'score':next_board.score(),
                   's':next_board.state.copy()}
            next_board.history.append(hist)
            #done condition
            if next_board.score()!=0 or (0 not in next_board.state):
                next_board.done=1
            return next_board
        else:
            print('invalid')
