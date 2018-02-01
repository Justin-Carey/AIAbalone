import pygame, sys, math
import view_button
import controller
import colors
import thorpy
import _thread
from pygame.locals import *

class GUI:

    # Coordinates constants.
    # The first two are the coordinates, and the last number is an indicator that
    # represents whether there is a piece or not (1 for the PLAYER BLACK and 2 for the PLAYER WHITE).
    # [x_coordinate, y_coordinate, piece, x_screen, y_screen, selected (0 or 1)]
    COORDINATES_CARTESIAN = [
        [0, -4, 0, 0, 0, 0], [1, -4, 0, 0, 0, 0], [2, -4, 0, 0, 0, 0], [3, -4, 0, 0, 0, 0], [4, -4, 0, 0, 0, 0],
        [-1, -3, 0, 0, 0, 0], [0, -3, 0, 0, 0, 0], [1, -3, 0, 0, 0, 0], [2, -3, 0, 0, 0, 0], [3, -3, 0, 0, 0, 0], [4, -3, 0, 0, 0, 0],
        [-2, -2, 0, 0, 0, 0], [-1, -2, 0, 0, 0, 0], [0, -2, 0, 0, 0, 0], [1, -2, 0, 0, 0, 0], [2, -2, 0, 0, 0, 0], [3, -2, 0, 0, 0, 0], [4, -2, 0, 0, 0, 0],
        [-3, -1, 0, 0, 0, 0], [-2, -1, 0, 0, 0, 0], [-1, -1, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0], [1, -1, 0, 0, 0, 0], [2, -1, 0, 0, 0, 0], [3, -1, 0, 0, 0, 0], [4, -1, 0, 0, 0, 0],
        [-4, 0, 0, 0, 0, 0], [-3, 0, 0, 0, 0, 0], [-2, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0],
        [-4, 1, 0, 0, 0, 0], [-3, 1, 0, 0, 0, 0], [-2, 1, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [2, 1, 0, 0, 0, 0], [3, 1, 0, 0, 0, 0],
        [-4, 2, 0, 0, 0, 0], [-3, 2, 0, 0, 0, 0], [-2, 2, 0, 0, 0, 0], [-1, 2, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0], [1, 2, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0],
        [-4, 3, 0, 0, 0, 0], [-3, 3, 0, 0, 0, 0], [-2, 3, 0, 0, 0, 0], [-1, 3, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0], [1, 3, 0, 0, 0, 0],
        [-4, 4, 0, 0, 0, 0], [-3, 4, 0, 0, 0, 0], [-2, 4, 0, 0, 0, 0], [-1, 4, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0]
    ]

    # Negative adjustment for coordinates constants.
    for coordinate in COORDINATES_CARTESIAN:
        coordinate[0] += 4
        coordinate[1] += 4

    # Stored pieces.
    # [index, piece]
    stored_pieces = []

    # Windows size setup.
    master_window_width = 1000
    master_window_height = 1000

    # Constructor.
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.font_coordinates = pygame.font.SysFont('Comic Sans MS', 30)

        self.main_display_surface = pygame.display.set_mode(
            (self.master_window_width,
             self.master_window_height)
        )

        pygame.display.set_caption('AIAbalone - Sandwich')

        # Set up the background.
        self.main_display_surface.fill(colors.WHITE)

        self.create_pieces_standard()
        self.populate_gui_coordinates()

        self.update_canvas()
        self.create_log_console()
        self.create_buttons()

    # Start the GUI main loop.
    def start_gui(self):

        # Event loop to be examined for an user action.
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mouse_button_down()

            pygame.display.update()

            # Thorpy reaction.
            self.thorpy_menu.react(event)

    # Mouse button listener.
    def mouse_button_down(self):
        pos = pygame.mouse.get_pos()

        # Process mouse input to get an index of clicked circle.
        index = 0
        for coordinate in self.COORDINATES_CARTESIAN:
            if self.calculate_distance(pos[0], pos[1], coordinate[3], coordinate[4]) < 30:
                # If there is a piece,
                if coordinate[2] != 0:
                    # If this hasn't been selected,
                    if coordinate[5] == 0:
                        # If the user clicked the piece, then highlight it.
                        self.select_position(index)
                        # Memorize the piece.
                        self.stored_pieces.append([index, coordinate[2]])
                        # Log messages.
                        messages = []
                        messages.append("Selected at (" + str(coordinate[0]) + "," + str(coordinate[1]) + ")")
                        messages.append("Stored_pieces: " + str(len(self.stored_pieces)))
                        self.log(messages)
                    # Or if this has been selected,
                    elif coordinate[5] == 1:
                        # Cancel the selection.
                        self.select_position(index)
                        # Throw away the piece in the list.
                        self.stored_pieces.remove([index, coordinate[2]])
                        # Log messages.
                        messages = []
                        messages.append("Unselected at (" + str(coordinate[0]) + "," + str(coordinate[1]) + ")")
                        messages.append("Stored_pieces: " + str(len(self.stored_pieces)))
                        self.log(messages)
                # If there is NOT a piece,
                elif coordinate[2] == 0:
                    # Move the piece according to the number of pieces in the stored_pieces.
                    if len(self.stored_pieces) == 1:
                        piece = self.stored_pieces.pop()
                        self.move_one_piece(piece[0], index, piece[1])
                        self.clear_all_selection()
                    elif len(self.stored_pieces) == 2:
                        pass
                        #TODO
                        self.clear_all_selection()
                    elif len(self.stored_pieces) == 3:
                        pass
                        #TODO
                        self.clear_all_selection()

            index += 1

        # Process mouse input for buttons.
        # for button in self.buttons:
        #     if button.rect.collidepoint(pos):
        #         button.call_back()

    # Move one piece.
    def move_one_piece(self, location_from, location_to, piece):
        self.COORDINATES_CARTESIAN[location_from][2] = 0
        self.COORDINATES_CARTESIAN[location_to][2] = piece
        self.update_canvas()

    # Move two pieces.
    def move_two_pieces(self):
        pass
        self.update_canvas()

    # Move three pieces.
    def move_three_pieces(self):
        pass
        self.update_canvas()

    # Select the position to indicate the position is selected.
    def select_position(self, position):
        if self.COORDINATES_CARTESIAN[position][5] == 0:
            self.COORDINATES_CARTESIAN[position][5] = 1
        elif self.COORDINATES_CARTESIAN[position][5] == 1:
            self.COORDINATES_CARTESIAN[position][5] = 0
        self.update_canvas()

    # Clear all coordinates' selection.
    def clear_all_selection(self):
        for coordinate in self.COORDINATES_CARTESIAN:
            coordinate[5] = 0
        self.update_canvas()

    # Clear all pieces in the stored_pieces.
    def clear_stored_pieces(self):
        self.stored_pieces.clear()

    # Initialize canvas with basic drawings.
    def update_canvas(self):

        # Draw the fundamental game setup.
        x_beginning = 240
        radius = 30
        radius_piece = 25
        x_decrement_increment = 40
        distance_between_elements = 80

        x_decrement_for_font = -30
        y_decrement_for_font = 30

        column_increment = 1
        coordinates_increment = 0
        for column in [5, 6, 7, 8, 9, 8, 7, 6, 5]:
            for row in range(0, column):
                # Draw background.
                if self.COORDINATES_CARTESIAN[coordinates_increment][5] == 0:
                    pygame.draw.circle(self.main_display_surface,
                                       colors.GREY,
                                       (row * distance_between_elements + x_beginning,
                                        column_increment * distance_between_elements),
                                       radius, 0)
                else:
                    pygame.draw.circle(self.main_display_surface,
                                       colors.CYAN,
                                       (row * distance_between_elements + x_beginning,
                                        column_increment * distance_between_elements),
                                       radius, 0)

                # Draw pieces.
                if self.COORDINATES_CARTESIAN[coordinates_increment][2] == 1:
                    pygame.draw.circle(self.main_display_surface,
                                       colors.BLACK,
                                       (row * distance_between_elements + x_beginning,
                                        column_increment * distance_between_elements),
                                       radius_piece, 0)
                elif self.COORDINATES_CARTESIAN[coordinates_increment][2] == 2:
                    pygame.draw.circle(self.main_display_surface,
                                       colors.WHITE,
                                       (row * distance_between_elements + x_beginning,
                                        column_increment * distance_between_elements),
                                       radius_piece, 0)

                # Draw coordinates.
                self.display_coordinates("(" + str(self.COORDINATES_CARTESIAN[coordinates_increment][0]) +
                                            "," + str(self.COORDINATES_CARTESIAN[coordinates_increment][1])+ ")",
                                        row * distance_between_elements
                                            + x_beginning + x_decrement_for_font,
                                        column_increment * distance_between_elements
                                            + y_decrement_for_font)
                coordinates_increment += 1

            column_increment += 1
            if column_increment <= 5:
                x_beginning -= x_decrement_increment
            else:
                x_beginning += x_decrement_increment

    # Initialize a log console.
    def create_log_console(self):
        # Draw console background.
        pygame.draw.rect(self.main_display_surface,
                         colors.BLACK, (0, 800, 1000, 200))

    # Print text to the log console.
    def log(self, message):
        # Draw console background to erase the previous messages.
        pygame.draw.rect(self.main_display_surface,
                         colors.BLACK, (0, 800, 1000, 200))
        x_log = 20
        y_log = 820

        font = pygame.font.SysFont('Consolas', 20)

        # Display messages in the message list.
        for m in message:
            text = str(m)
            text = font.render(text, True, colors.GREEN)
            self.main_display_surface.blit(text, (x_log, y_log))
            y_log += 20

    # Print text to the log console.
    def log_clear(self):
        # Draw console background to erase the previous messages.
        pygame.draw.rect(self.main_display_surface,
                         colors.BLACK, (0, 800, 1000, 200))

    # Display coordinates for the locations of Abalone.
    def display_coordinates(self, text, x, y, size = 20, color = (0, 0, 0)):
        text = str(text)
        font = pygame.font.SysFont('Consolas', 20)
        text = font.render(text, True, color)
        self.main_display_surface.blit(text, (x, y))

    # Create the initial pieces arranged (Standard).
    def create_pieces_standard(self):
        for index in [45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]:
            self.COORDINATES_CARTESIAN[index][2] = 1
        for index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15]:
            self.COORDINATES_CARTESIAN[index][2] = 2

    # Create the initial pieces arranged (German Daisy).
    def create_pieces_german_daisy(self):
        pass

    # Create the initial pieces arranged (Belgian Daisy).
    def create_pieces_belgian_daisy(self):
        pass

    # Populate gui coordinates for handling mouse events.
    def populate_gui_coordinates(self):
        x_beginning = 240
        x_decrement_increment = 40
        distance_between_elements = 80

        column_increment = 1
        coordinates_increment = 0
        for column in [5, 6, 7, 8, 9, 8, 7, 6, 5]:
            for row in range(0, column):
                self.COORDINATES_CARTESIAN[coordinates_increment][3] = row * distance_between_elements + x_beginning
                self.COORDINATES_CARTESIAN[coordinates_increment][4] = column_increment * distance_between_elements

                coordinates_increment += 1

            column_increment += 1
            if column_increment <= 5:
                x_beginning -= x_decrement_increment
            else:
                x_beginning += x_decrement_increment

    def calculate_distance(self, x1, y1, x2, y2):
        return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

    # Initialize buttons.
    def create_buttons(self):
        # Draw buttons background.
        pygame.draw.rect(self.main_display_surface,
                         colors.BLACK, (800, 0, 100, 800))
        pygame.draw.rect(self.main_display_surface,
                         colors.WHITE, (900, 0, 100, 800))

        # Draw texts for teams.
        font = pygame.font.SysFont('Consolas', 20)
        text_for_black_team = font.render("<Black>", True, colors.GREY)
        self.main_display_surface.blit(text_for_black_team, (805, 30))
        text_for_white_team = font.render("<White>", True, colors.GREY)
        self.main_display_surface.blit(text_for_white_team, (900, 30))

        # ================ Widgets (Thorpy) ================

        # ThorPy elements for black.
        button00 = thorpy.make_button("Button00", func=lambda: controller.button_01_callback(self))
        button00.set_size((90, 40))

        checker_radio = thorpy.Checker.make("Radio", type_="radio")
        checker_check = thorpy.Checker.make("Checker")

        label = thorpy.make_text("Label", 22, (255, 255, 0))
        inserter = thorpy.Inserter.make(name="", value="")

        slider = thorpy.SliderX.make(40, (0, 100), "", type_=int, initial_value=0)

        # ThorPy elements for white.
        button01 = thorpy.make_button("Button00", func=lambda: controller.button_02_callback(self))
        button01.set_size((90, 40))

        # ThorPy elements for all.
        button_start = thorpy.make_button("Start", func=lambda: controller.button_02_callback(self))
        button_start.set_size((190, 40))

        button_pause = thorpy.make_button("Pause", func=lambda: controller.button_02_callback(self))
        button_pause.set_size((190, 40))

        button_stop = thorpy.make_button("Stop", func=lambda: controller.button_02_callback(self))
        button_stop.set_size((190, 40))

        button_reset = thorpy.make_button("Reset", func=lambda: controller.button_02_callback(self))
        button_reset.set_size((190, 40))

        # Pack the buttons to each box.
        box_black = thorpy.Box.make(elements=[button00, checker_radio, checker_check, label, inserter, slider])
        box_white = thorpy.Box.make(elements=[button01])
        box_all = thorpy.Box.make(elements=[button_start, button_pause, button_stop, button_reset])

        # Place the elements.
        box_black.set_topleft((800, 80))
        box_black.blit()
        box_black.update()

        box_white.set_topleft((900, 80))
        box_white.blit()
        box_white.update()

        box_all.set_topleft((800, 615))
        box_all.blit()
        box_all.update()

        # Regroup all elements on a menu, even if the program does NOT launch the menu.
        self.thorpy_menu = thorpy.Menu([box_black, box_white, box_all])

        # IMPORTANT: Set the screen as surface for all elements.
        for element in self.thorpy_menu.get_population():
            element.surface = self.main_display_surface










