import numpy as np
from TicTacToeGame import TTTBoard, getkey

def player_move(game):
    xy = int(input('x: ')), int(input('y: '))
    return xy

def random_move(game):
    poss = game.allpossible()
    xy = poss[np.random.randint(len(poss))]
    return xy

def learned_move(game, training):
    poss = game.allpossible()
    poss = [xy[0]*3+xy[1] for xy in poss]  
    move_list = [_ for _ in enumerate(training.Q[getkey(game.state)]) if (_[0] in poss)]
    func = {0:min, 1:max}[game.turn]
    best_move = func(move_list,key=lambda x:x[1])[0]
    return (best_move//3, best_move%3)

def ai_vs_random(training, ai_first=False):
    game = TTTBoard()
    if ai_first==True:
        move = learned_move(game, training)
        game = game.update(move)
    while not game.done:
        move = random_move(game)
        game = game.update(move)
        if game.done:
            break
        move = learned_move(game, training)
        game = game.update(move)
    return game.score()

def ai_vs_ai(training):
    game = TTTBoard()
    while not game.done:
        move = learned_move(game, training)
        game = game.update(move)
    return game.score()

def print_board(game):
    readable = [['_'] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            if game.state[i][j] == 1:
                readable[i][j] = 'O'
            elif game.state[i][j] == -1:
                readable[i][j] = 'X'
    for row in readable:
        print(row)
    
#PLAY AGAINST AI
def play_game(training):
    game = TTTBoard()
    while not game.done:
            
        print_board(game)
        print()
        print('Your Move')
        your_move = player_move(game)
        print()
        
        game = game.update(your_move)
        print()
        print_board(game)
        print()
        if game.done: break

        ai_move = learned_move(game, training)
        print('ai_move')
        print(ai_move)
        print()
        
        game = game.update(ai_move)
            
    print_board(game)
    print('Game Score: ' + str(game.score()))
