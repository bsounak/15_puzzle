"""
15 Puzzle - Sounak Bhattacharya
How to play?
--> run this file. The main game window will appear. Click on a numbered button to see if it moves. If you start from
the initial position, move buttons around, and can return to the original position, you will win the game. For a tougher
challenge, press the scramble button. It will generate a random board position. Remember: It might be possible that
there is no solution for an initial random board setting. Good Luck!
"""

from tkinter import *
import math
import random

BUTTON_COLOR = '#AF7AC5'
BACKGROUND_COLOR = '#d9d9d9'


class Application(object):
    def __init__(self):

        # Main window
        self.window = Tk()
        self.window.geometry('{}x{}'.format(400, 400))
        self.window.title('15 puzzle')

        # Here I will save the buttons as values and grid co-ordinates as keys
        self.board_position = {}

        # To make the window stretch when resized
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=3)
        self.window.grid_columnconfigure(0, weight=1)

        # This frame will contain buttons like scramble and restart and a status text
        self.frame0 = Frame(self.window)
        self.frame0.grid(row=0, column=0, sticky="nsew")
        Button(self.frame0, text='scramble', background='pink', command=self.scramble, height=2, width=8). \
            grid(row=0, column=1, sticky="nse")
        Button(self.frame0, text='restart', background='pink', command=self.restart, height=2, width=8). \
            grid(row=1, column=1, sticky="nse")

        # Welcome text
        self.message = Label(self.frame0, text='Welcome! Click on a button to see if it moves.')
        self.message.grid(row=0, column=0, columnspan=2)

        self.frame0.grid_rowconfigure(0, weight=1)
        self.frame0.grid_columnconfigure(1, weight=1)
        self.frame0.grid_rowconfigure(1, weight=1)
        self.frame0.grid_columnconfigure(1, weight=1)

        # This frame will contain 15 numbered buttons and a blank one
        self.frame = Frame(self.window)
        self.frame.grid(row=1, column=0, sticky="nsew")

        self.swapped_once = False
        self.scrambled = False

        # Some stuff I need to understand better
        for row in range(4):
            self.frame.grid_rowconfigure(row, weight=1)
        for column in range(4):
            self.frame.grid_columnconfigure(column, weight=1)

        # Draw initial board position
        self.initiate_board()

        self.window.mainloop()

    def restart(self):
        """ Reset the board to the original arrangement. """
        self.message.configure(text='Ok. You have started fresh.')
        self.swapped_once = False
        self.scrambled = False
        self.initiate_board()

    def initiate_board(self):
        """ Put the numbered buttons in the right place and store them in a dictionary. """
        # Add buttons
        for i in range(4):
            for j in range(4):
                if 4*i + j + 1 == 16:  # blank piece
                    button = Button(self.frame, command=lambda coord=(i, j): self.update(coord),
                                    background=BACKGROUND_COLOR)
                    button.grid(row=i, column=j, sticky='nsew')
                else:
                    button = Button(self.frame, text=str(4*i + j + 1), background=BUTTON_COLOR,
                                    command=lambda coord=(i, j): self.update(coord))
                    button.grid(row=i, column=j, sticky='nsew')

                self.board_position[(i, j)] = button  # store the buttons

    def get_location_of_blank_tile(self):
        """ Get the grid coordinate of the blank tile """

        for key in self.board_position.keys():
            if self.board_position[key]['text'] == '':
                return key

    def legal_move(self, clicked_button_coord, blank_tile_coord):
        """
        Check whether the clicked_button can be swapped with the blank space. Return True if Yes, False if no.
        :param clicked_button_coord: tuple
        :param blank_tile_coord: tuple
        :return: bool

        Example:
        >>> legal_move((0,0), (3,3))
        >>> False
        """
        return any([x == y for (x, y) in zip(clicked_button_coord, blank_tile_coord)])

    def swap(self, button1, button2):
        """ Swap the properties between button1 and button 2
        :param button1: tuple
        :param button2: tuple
        """
        self.swapped_once = True
        if not self.scrambled:
            self.message.configure(text='Great!.\n Now jumble the board a bit more \n '
                                        'and try to get back to the original position.')
        text = self.board_position[button1]['text']
        color = self.board_position[button1]['background']

        self.board_position[button1]['text'] = self.board_position[button2]['text']
        self.board_position[button1]['background'] = self.board_position[button2]['background']

        self.board_position[button2]['text'] = text
        self.board_position[button2]['background'] = color

    def get_distance(self, button1, button2):
        """ Calculate eucledian distance between two button coordinates
        :param button1: tuple
        :param button2: tuple

        Example:
        >>> get_distance((0,0), (3,0))
        >>> 3
        """
        return int(math.sqrt(sum([(i - j)*(i - j) for i, j in zip(button1, button2)])))

    def win(self):
        """ Check if the current board position is a winning position or not. """
        for key in self.board_position.keys():
            try:
                if (4*key[0] + key[1] + 1) == int(self.board_position[key]['text']):
                    pass
                else:
                    return False
            except ValueError:
                if (4 * key[0] + key[1] + 1) == 16:
                    pass
                else:
                    return False

        return True

    def update(self, clicked_button_coord):
        """ This method is called when a numbered button is clicked.
         :param clicked_button_coord: tuple
        """
        blank_tile_coord = self.get_location_of_blank_tile()
        if self.legal_move(clicked_button_coord, blank_tile_coord):
            distance = self.get_distance(clicked_button_coord, blank_tile_coord)
            if distance == 1:
                self.swap(clicked_button_coord, blank_tile_coord)

        if self.win():
            if self.swapped_once:
                self.message.configure(text='Congratulations! You Won.\n Try scrambling for a real challenge.')

    def scramble(self):
        """ Random shuffle the board. """
        self.scrambled = True
        self.swapped_once = False
        self.message.configure(text='This is a random board arrangement. \n There might not be a solution.')
        order = random.sample(range(1, 17), 16)
        i = 0
        for key in self.board_position.keys():
            if order[i] == 16:
                self.board_position[key]['text'] = ''
                self.board_position[key]['background'] = BACKGROUND_COLOR

            else:
                self.board_position[key]['text'] = order[i]
                self.board_position[key]['background'] = BUTTON_COLOR

            i += 1
            

def main():
    app = Application()

main()