"""
    Michael Nguyen
    Ian Nguyen

    December 17, 2021
    CPSC 481 - TicTacToe
"""

import math
import random
import time
from os import system
import platform

game_Board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

# Assigned Moves
assigned_moves = {
    1: [0, 0], 2: [0, 1], 3: [0, 2],
    4: [1, 0], 5: [1, 1], 6: [1, 2],
    7: [2, 0], 8: [2, 1], 9: [2, 2],
}

# All possible outcomes to win
def winning_Outcomes(state, pos):
    win_state = [
        # Case 1: Horizontal Wins
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        #Case 2: Vertical Wins
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        #Case 3: Diagonal Wins
        [state[0][0], state[1][1], state[2][2]],
        [state[0][2], state[1][1], state[2][0]],
    ]
    if [pos, pos, pos] in win_state:
        return True
    else:
        return False

# Assigning player a value for minimax algorithm
Human = -1
AI = +1

# Returns who wins
def game_over(state):
    return winning_Outcomes(state, Human) or winning_Outcomes(state, AI)


def check_available(state):
    pos = []

    for r, row in enumerate(state):
        for c, col in enumerate(row):
            if col == 0:
                pos.append([r, c])

    return pos


# Check to see if move is available
def valid_move(r, c):
    if [r, c] in check_available(game_Board):
        return True
    else:
        return False


# Place the move
def set_move(r, c, player):
    if valid_move(r, c):
        game_Board[r][c] = player
        return True
    else:
        return False


# Finding the best solution
def minimax(state, depth, player):
    if player == Human:
        optimized_score = [+1, +1, +math.inf]
    else:
        optimized_score = [-1, -1, -math.inf]

    if depth == 0 or game_over(state):
        score = Heuristic(state)
        return [-1, -1, score]

    for cell in check_available(state):
        r, c = cell[0], cell[1]
        state[r][c] = player
        score = minimax(state, depth - 1, -player)
        state[r][c] = 0
        score[0], score[1] = r, c

        # AI tries to maximize their score
        # User tries to minimize
        if player == AI:
            if score[2] > optimized_score[2]:
                optimized_score = score
        else:
            if score[2] < optimized_score[2]:
                optimized_score = score

    return optimized_score


def Heuristic(state):
    if winning_Outcomes(state, AI):
        score = +1
    elif winning_Outcomes(state, Human):
        score = -1
    else:
        score = 0

    return score


def print_Board(state, bot, user):
    optimal_score = {
        -1: user,
        +1: bot,
        0: ' '
    }
    str_line = '----  ----  ----'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            current = optimal_score[cell]
            print(f'| {current} |', end='')
        print('\n' + str_line)


def human_turn(bot, user):
    depth = len(check_available(game_Board))
    if depth == 0 or game_over(game_Board):
        return

    # Keeps track of movement
    move = -1

    print(f'Human turn [{user}]')
    print_Board(game_Board, bot, user)

    while move < 1 or move > 9:
        try:
            move = int(input('Enter in a num from 1 - 9 for next movement: '))
            position = assigned_moves[move]
            valid = set_move(position[0], position[1], Human)

            if not valid:
                print('Move taken.')
                move = -1
        except (KeyError, ValueError):
            print('Bad choice')


def ai_turn(bot, user):
    depth = len(check_available(game_Board))
    if depth == 0 or game_over(game_Board):
        return

    print(f'Computer turn [{bot}]')
    print_Board(game_Board, bot, user)

    if depth == 9:
        r = random.choice([0, 1, 2])
        c = random.choice([0, 1, 2])
    else:
        move = minimax(game_Board, depth, AI)
        r, c = move[0], move[1]
    print("Using Minimax algorithm to find best move...")
    set_move(r, c, AI)
    time.sleep(0.5)

def main():
    user = ''
    bot = ''

    # User select which piece they would like to play as
    print('Welcome to the unbeatable tictactoe battle! Choose your unit! (X or O)')
    user = input('You have chosen: ').upper()

    # Assigning the AI's piece
    if user == 'X':
        bot = 'O'
    else:
        bot = 'X'

    # Run the game until board is filled
    while len(check_available(game_Board)) > 0 and not game_over(game_Board):
        human_turn(bot, user)
        ai_turn(bot, user)

    # Game over message
    if winning_Outcomes(game_Board, Human):
        print(f'User turn [{user}]')
        print_Board(game_Board, bot, user)
        print('Thats a win for the humans!')
    elif winning_Outcomes(game_Board, AI):
        print(f'AIs turn [{bot}]')
        print_Board(game_Board, bot, user)
        print('The winner is.... AI!')
    else:
        print_Board(game_Board, bot, user)
        print('This match turned into a Draw!')

    # THE REFRESH DOESN'T WORK, NOT SURE HOW TO FIX IT
    """
    user_choice = input('play again?(y/n): ').upper()
    print("\n")
    if user_choice == 'Y':
        main()
    else:
    """
    exit()


if __name__ == '__main__':
    main()