# a3.py

# my friend helped me with ideas of how to implement this game

import time
from random import *
from math import inf as infinity
import platform
from os import system

"""
An implementation of Tic-Tac-Toe where a human can play against the computer,
where the computer makes all of its moves using random playouts using Python.

"""
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
HUMAN = -1
COMPUTER = +1


def judge(state):
    # return +1 if the computer wins; -1 if the human wins; 0 draw
    if wins(state, COMPUTER):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def game_over(state):
    # return: True if the human or computer wins; end of game
    return wins(state, HUMAN) or wins(state, COMPUTER)


def wins(state, player):
    # return True if the player wins; False if the player loses
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def empty_cells(state):
    # returns a list of emply cells; needed to continue playing
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells


def legal_move(x, y):
    # return True if the board[x][y] is empty; False otherwise
    cell_list = empty_cells(board)
    if [x, y] in cell_list:
        return True
    else:
        return False


def set_move(x, y, player):
    # returns True if move played by current player is legal;
    # return False otherwise
    if legal_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

def clear_screen():
    # clears the console
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def random_playouts(state, depth, player):
    """
    AI function that chooses the best move for the Computer
    Parameters-
                state: current state of the board
                depth: node index in the tree (between 0 and 9)
                player: human or computer
    returns a list with the best choice of row, col and the score
    """
    if player == COMPUTER:
        best = [-1, -1, -infinity]
    elif player == HUMAN:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = judge(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = random_playouts(state, depth-1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMPUTER:
            if score[2] > best[2]:
                best = score  
        else:
            if score[2] < best[2]:
                best = score  

    return best


def print_state(state, computer_choice, human_choice):
    # prints current state 
    chars = {
        -1: human_choice,
        +1: computer_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)
    print("")


def human_turn(computer_choice, human_choice):
    """
    The Human plays choosing a valid move.
    Parameters-
              computer_choice: computer's choice of X or O
              human_choice: human's choice of X or O
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # list of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clear_screen()
    
    print(f'Human turn [{human_choice}]')
    print_state(board, computer_choice, human_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Please Use Number Pad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('\nIllegal Move\n')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('\nBye\n')
            exit()
        except (KeyError, ValueError):
            print('\nIllegal Choice\n')
            

def ai_turn(computer_choice, human_choice):
    """
    It calls the minimax function if the depth < 9,
    otherwise chooses a random coordinate.
    Parameters-
              computer_choice: computer's choice of X or O
              human_choice: human's choice of X or O
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clear_screen()
    
    print(f'Computer turn [{computer_choice}]')
    print_state(board, computer_choice, human_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = random_playouts(board, depth, COMPUTER)
        x, y = move[0], move[1]

    set_move(x, y, COMPUTER)
    time.sleep(1)


def play_a_new_game(): ################################################
    
    clear_screen()
    
    human_choice = ''  # X or O
    computer_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while human_choice != 'O' and human_choice != 'X':
        try:
            print('')
            human_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Illegal choice')

    # Setting computer's choice
    if human_choice == 'X':
        computer_choice = 'O'
    else:
        computer_choice = 'X'

    # Who is starting the game?
    clear_screen()
    while first != 'Y' and first != 'N':
        try:
            first = input('Would you like to start? [Y/N]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Illegal choice')

    # Loop through moves while playing game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(computer_choice, human_choice)
            first = ''

        human_turn(computer_choice, human_choice)
        ai_turn(computer_choice, human_choice)

    # Game over message
    if wins(board, HUMAN):
        clear_screen()
        print(f'Your turn [{human_choice}]')
        print_state(board, computer_choice, human_choice)
        print('YOU WIN!')
    elif wins(board, COMPUTER):
        clear_screen()
        print(f'Computer turn [{computer_choice}]')
        print_state(board, computer_choice, human_choice)
        print('YOU LOSE!')
    else:
        clear_screen()
        print_state(board, computer_choice, human_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    play_a_new_game()
