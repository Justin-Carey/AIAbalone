"""
Copyright (C) BCIT AI/ML Option 2018 Team with Members Following - All Rights Reserved.
- Jake Jonghun Choi     jchoi179@my.bcit.ca
- Justin Carey          justinthomascarey@gmail.com
- Pashan Irani          pashanirani@gmail.com
- Tony Huang	        tonyhuang1996@hotmail.ca
- Chil Yuqing Qiu       yuqingqiu93@gmail.com
Unauthorized copying of this file, via any medium is strictly prohibited.
Written by Chil, Yuqing Qiu <yuqingqiu93@gmail.com>
"""

import os


# the total evaluation function
# PARAMS:
#     current_state: matching Chi-En's *.board file, one line only
#     piece_weight: how important are the number of piece on board, default 0.5 --> 50% of the decision is based on the piece number
# RETURN:
#     the evaluated position value, range [0, 1], 1 means winning state, 0 means losing state
def ai_evaluate_state(current_state, piece_weight=0.5):
    piece_heuristics = evaluate_pieces(current_state)
    position_heuristics = evaluate_position(current_state)
    # if any side has lost 6 pieces
    if (piece_heuristics == 1) or (piece_heuristics == 0):
        return 1
    # if no side has lost 6 pieces yet
    else:
        return piece_heuristics * piece_weight + position_heuristics * (1 - piece_weight)


# black_remain indicates how many losable pieces for black side(MAX player) remains, initial state value: 6, losing state value: 0
# white_remain indicates how many losable pieces for white side(MIN player) remains, initial state value: 6, losing state value: 0
def evaluate_pieces(current_state):
    black_remain = count_marbles(current_state, 'b') - 8
    white_remain = count_marbles(current_state, 'w') - 8
    return black_remain/(black_remain+white_remain)


def evaluate_position(current_state):
    return 0.5


def count_marbles(state, color):
    num_marble = 0
    for marble in state:
        if color in marble:
            num_marble += 1
    return num_marble


def one_state(one_line):
    state = one_line.split(",")
    return state


# manually debug mode: put the testing board under this directory and test with file name Test.board
if __name__ == "__main__":
    # for redirect file location
    this_dir = os.path.dirname(os.path.realpath('__file__'))
    # for change test files
    file_name = "Test.board"
    test_file = this_dir + '/' + file_name
    try:
        with open(test_file) as file:
            content = file.readlines()
        content = [x.strip() for x in content]
        for line in content:
            print(line)
            print(ai_evaluate_state(one_state(line)))

    except FileNotFoundError:
        print("test file not found")


