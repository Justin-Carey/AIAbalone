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

import view
import model

def update_gui_coordinates_from_global_game_state_representation(context):

    for gui_coordinate in context.COORDINATES_CARTESIAN:

        temp = model.global_game_board_state[gui_coordinate[0]][gui_coordinate[1]]
        gui_coordinate[2] = temp



