'''
Copyright (C) BCIT AI/ML Option 2018 Team with Members Following - All Rights Reserved.
- Jake Jonghun Choi     jchoi179@my.bcit.ca
- Justin Carey          justinthomascarey@gmail.com
- Pashan Irani          pashanirani@gmail.com
- Tony Huang	        tonyhuang1996@hotmail.ca
- Chil Yuqing Qiu       yuqingqiu93@gmail.com
Unauthorized copying of this file, via any medium is strictly prohibited.
Written by Jake Jonghun Choi <jchoi179@my.bcit.ca>
'''

import ai_rules

# Move one piece.
cpdef inline move_one_piece(state, int old_x, int old_y, int new_x, int new_y):

    cdef int piece

    # Memorize the old piece.
    piece = state[old_x][old_y]

    # Remove the old piece.
    state[old_x][old_y] = 0

    # Place the piece to new location.
    state[new_x][new_y] = piece

    return state

# Move two pieces.
cpdef inline move_two_pieces(state, int old_x1, int old_y1, int new_x1, int new_y1,
                           int old_x2, int old_y2, int new_x2, int new_y2):

    cdef int piece1, piece2

    # Memorize the old pieces.
    piece1 = state[old_x1][old_y1]
    piece2 = state[old_x2][old_y2]

    # Remove the old pieces.
    state[old_x1][old_y1] = 0
    state[old_x2][old_y2] = 0

    # Place the pieces to new location.
    state[new_x1][new_y1] = piece1
    state[new_x2][new_y2] = piece2

    return state

# Move three pieces.
cpdef inline move_three_pieces(state, int old_x1, int old_y1, int new_x1, int new_y1,
                             int old_x2, int old_y2, int new_x2, int new_y2,
                             int old_x3, int old_y3, int new_x3, int new_y3):

    cdef piece1, piece2, piece3

    # Memorize the old pieces.
    piece1 = state[old_x1][old_y1]
    piece2 = state[old_x2][old_y2]
    piece3 = state[old_x3][old_y3]

    # Remove the old pieces.
    state[old_x1][old_y1] = 0
    state[old_x2][old_y2] = 0
    state[old_x3][old_y3] = 0

    # Place the pieces to new location.
    state[new_x1][new_y1] = piece1
    state[new_x2][new_y2] = piece2
    state[new_x3][new_y3] = piece3

    return state


# Move 2 to 1 sumito.
cpdef inline move_2_to_1_sumito(state, int old_x1, int old_y1, int new_x1, int new_y1,
                              int old_x2, int old_y2, int new_x2, int new_y2):

    cdef piece1, piece2, clicked_x, clicked_y, removed_x, removed_y, piece_opponent

    # Get the clicked position.
    clicked_position = get_the_differences_from_sets_for_sumitos({(new_x1, new_y1), (new_x2, new_y2)},
                                                                 {(old_x1, old_y1), (old_x2, old_y2)})
    clicked_x = clicked_position[0]
    clicked_y = clicked_position[1]

    # Get the moved position.
    moved_position = get_the_differences_from_sets_for_sumitos({(old_x1, old_y1), (old_x2, old_y2)},
                                                               {(new_x1, new_y1), (new_x2, new_y2)})
    removed_x = moved_position[0]
    removed_y = moved_position[1]

    # Store 2 advanced coordinates for piece advancement.
    advanced_coordinates = []

    # Find out the directions and populate advanced_coordinates.
    if removed_y == clicked_y:

        if clicked_x > removed_x:
            advanced_coordinates.append((clicked_x + 1, clicked_y))
            advanced_coordinates.append((clicked_x + 2, clicked_y))
        elif clicked_x < removed_x:
            advanced_coordinates.append((clicked_x - 1, clicked_y))
            advanced_coordinates.append((clicked_x - 2, clicked_y))

    elif removed_x == clicked_x:

        if clicked_y > removed_y:
            advanced_coordinates.append((clicked_x, clicked_y + 1))
            advanced_coordinates.append((clicked_x, clicked_y + 2))
        elif clicked_y < removed_y:
            advanced_coordinates.append((clicked_x, clicked_y - 1))
            advanced_coordinates.append((clicked_x, clicked_y - 2))
    else:

        if clicked_x > removed_x:
            advanced_coordinates.append((clicked_x + 1, clicked_y - 1))
            advanced_coordinates.append((clicked_x + 2, clicked_y - 2))
        elif clicked_x < removed_x:
            advanced_coordinates.append((clicked_x - 1, clicked_y + 1))
            advanced_coordinates.append((clicked_x - 2, clicked_y + 2))

    # Memorize the opponent piece.
    piece_opponent = state[clicked_x][clicked_y]

    # Memorize the old pieces.
    piece1 = state[old_x1][old_y1]
    piece2 = state[old_x2][old_y2]

    # Remove the old pieces.
    state[old_x1][old_y1] = 0
    state[old_x2][old_y2] = 0

    # Place the pieces to new location.
    state[new_x1][new_y1] = piece1
    state[new_x2][new_y2] = piece2

    # Place the opponent piece to the advanced position.
    if (ai_rules.is_the_position_inside_of_the_board(state, [advanced_coordinates[0]])):
        adv_x = advanced_coordinates[0][0]
        adv_y = advanced_coordinates[0][1]
        state[adv_x][adv_y] = piece_opponent

    return state

# Move 3 to 1 sumito.
cpdef inline move_3_to_1_sumito(state, int old_x1, int old_y1, int new_x1, int new_y1,
                              int old_x2, int old_y2, int new_x2, int new_y2,
                              int old_x3, int old_y3, int new_x3, int new_y3):

    cdef piece1, piece2, piece3, clicked_x, clicked_y, removed_x, removed_y, piece_opponent

    # Get the clicked position.
    clicked_position = get_the_differences_from_sets_for_sumitos({(new_x1, new_y1), (new_x2, new_y2), (new_x3, new_y3)},
                                                                 {(old_x1, old_y1), (old_x2, old_y2), (old_x3, old_y3)})
    clicked_x = clicked_position[0]
    clicked_y = clicked_position[1]

    # Get the moved position.
    moved_position = get_the_differences_from_sets_for_sumitos({(old_x1, old_y1), (old_x2, old_y2), (old_x3, old_y3)},
                                                               {(new_x1, new_y1), (new_x2, new_y2), (new_x3, new_y3)})
    removed_x = moved_position[0]
    removed_y = moved_position[1]

    # Store 3 advanced coordinates for piece advancement.
    advanced_coordinates = []

    # Find out the directions and populate advanced_coordinates.
    if removed_y == clicked_y:

        if clicked_x > removed_x:
            advanced_coordinates.append((clicked_x + 1, clicked_y))
            advanced_coordinates.append((clicked_x + 2, clicked_y))
            advanced_coordinates.append((clicked_x + 3, clicked_y))
        elif clicked_x < removed_x:
            advanced_coordinates.append((clicked_x - 1, clicked_y))
            advanced_coordinates.append((clicked_x - 2, clicked_y))
            advanced_coordinates.append((clicked_x - 3, clicked_y))

    elif removed_x == clicked_x:

        if clicked_y > removed_y:
            advanced_coordinates.append((clicked_x, clicked_y + 1))
            advanced_coordinates.append((clicked_x, clicked_y + 2))
            advanced_coordinates.append((clicked_x, clicked_y + 3))
        elif clicked_y < removed_y:
            advanced_coordinates.append((clicked_x, clicked_y - 1))
            advanced_coordinates.append((clicked_x, clicked_y - 2))
            advanced_coordinates.append((clicked_x, clicked_y - 3))
    else:

        if clicked_x > removed_x:
            advanced_coordinates.append((clicked_x + 1, clicked_y - 1))
            advanced_coordinates.append((clicked_x + 2, clicked_y - 2))
            advanced_coordinates.append((clicked_x + 3, clicked_y - 3))
        elif clicked_x < removed_x:
            advanced_coordinates.append((clicked_x - 1, clicked_y + 1))
            advanced_coordinates.append((clicked_x - 2, clicked_y + 2))
            advanced_coordinates.append((clicked_x - 3, clicked_y + 3))

    # Memorize the opponent piece.
    piece_opponent = state[clicked_x][clicked_y]

    # Memorize the old pieces.
    piece1 = state[old_x1][old_y1]
    piece2 = state[old_x2][old_y2]
    piece3 = state[old_x3][old_y3]

    # Remove the old pieces.
    state[old_x1][old_y1] = 0
    state[old_x2][old_y2] = 0
    state[old_x3][old_y3] = 0

    # Place the pieces to new location.
    state[new_x1][new_y1] = piece1
    state[new_x2][new_y2] = piece2
    state[new_x3][new_y3] = piece3

    # Place the opponent piece to the advanced position.
    if (ai_rules.is_the_position_inside_of_the_board(state, [advanced_coordinates[0]])):
        adv_x = advanced_coordinates[0][0]
        adv_y = advanced_coordinates[0][1]
        state[adv_x][adv_y] = piece_opponent

    return state

# Move 3 to 2 sumito.
cpdef inline move_3_to_2_sumito(state, int old_x1, int old_y1, int new_x1, int new_y1,
                              int old_x2, int old_y2, int new_x2, int new_y2,
                              int old_x3, int old_y3, int new_x3, int new_y3):

    cdef piece1, piece2, piece3, clicked_x, clicked_y, removed_x, removed_y, piece_opponent_1, piece_opponent_2

    # Get the clicked position.
    clicked_position = get_the_differences_from_sets_for_sumitos({(new_x1, new_y1), (new_x2, new_y2), (new_x3, new_y3)},
                                                                 {(old_x1, old_y1), (old_x2, old_y2), (old_x3, old_y3)})
    clicked_x = clicked_position[0]
    clicked_y = clicked_position[1]

    # Get the moved position.
    moved_position = get_the_differences_from_sets_for_sumitos({(old_x1, old_y1), (old_x2, old_y2), (old_x3, old_y3)},
                                                               {(new_x1, new_y1), (new_x2, new_y2), (new_x3, new_y3)})
    removed_x = moved_position[0]
    removed_y = moved_position[1]

    # Store 3 advanced coordinates for piece advancement.
    advanced_coordinates = []

    # Find out the directions and populate advanced_coordinates.
    if removed_y == clicked_y:

        if clicked_x > removed_x:
            advanced_coordinates.append((clicked_x + 1, clicked_y))
            advanced_coordinates.append((clicked_x + 2, clicked_y))
            advanced_coordinates.append((clicked_x + 3, clicked_y))
        elif clicked_x < removed_x:
            advanced_coordinates.append((clicked_x - 1, clicked_y))
            advanced_coordinates.append((clicked_x - 2, clicked_y))
            advanced_coordinates.append((clicked_x - 3, clicked_y))

    elif removed_x == clicked_x:

        if clicked_y > removed_y:
            advanced_coordinates.append((clicked_x, clicked_y + 1))
            advanced_coordinates.append((clicked_x, clicked_y + 2))
            advanced_coordinates.append((clicked_x, clicked_y + 3))
        elif clicked_y < removed_y:
            advanced_coordinates.append((clicked_x, clicked_y - 1))
            advanced_coordinates.append((clicked_x, clicked_y - 2))
            advanced_coordinates.append((clicked_x, clicked_y - 3))
    else:

        if clicked_x > removed_x:
            advanced_coordinates.append((clicked_x + 1, clicked_y - 1))
            advanced_coordinates.append((clicked_x + 2, clicked_y - 2))
            advanced_coordinates.append((clicked_x + 3, clicked_y - 3))
        elif clicked_x < removed_x:
            advanced_coordinates.append((clicked_x - 1, clicked_y + 1))
            advanced_coordinates.append((clicked_x - 2, clicked_y + 2))
            advanced_coordinates.append((clicked_x - 3, clicked_y + 3))

    # Memorize the opponent pieces.
    piece_opponent_1 = state[clicked_x][clicked_y]
    piece_opponent_2 = state[advanced_coordinates[0][0]][advanced_coordinates[0][1]]

    # Memorize the old pieces.
    piece1 = state[old_x1][old_y1]
    piece2 = state[old_x2][old_y2]
    piece3 = state[old_x3][old_y3]

    # Remove the old pieces.
    state[old_x1][old_y1] = 0
    state[old_x2][old_y2] = 0
    state[old_x3][old_y3] = 0

    # Place the pieces to new location.
    state[new_x1][new_y1] = piece1
    state[new_x2][new_y2] = piece2
    state[new_x3][new_y3] = piece3

    # Place the opponent piece 1 to the advanced position.
    if (ai_rules.is_the_position_inside_of_the_board(state, [advanced_coordinates[0]])):
        adv_x_1 = advanced_coordinates[0][0]
        adv_y_1 = advanced_coordinates[0][1]
        state[adv_x_1][adv_y_1] = piece_opponent_1

    # Place the opponent piece 2 to the advanced position.
    if (ai_rules.is_the_position_inside_of_the_board(state, [advanced_coordinates[1]])):
        adv_x_2 = advanced_coordinates[1][0]
        adv_y_2 = advanced_coordinates[1][1]
        state[adv_x_2][adv_y_2] = piece_opponent_2

    return state


# ================ ================ Utility Functions ================ ================


# Get the differences from sets for sumitos to get rid of clicked input from gui.
cpdef inline get_the_differences_from_sets_for_sumitos(positions_1, positions_2):

    new_set = positions_1.difference(positions_2)
    return new_set.pop()











