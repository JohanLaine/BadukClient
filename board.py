from __future__ import division, print_function

import numpy as np

from copy import copy
from itertools import product

from stones import (
    NoStone,
    PlayerStone,
    WHITE,
    BLACK,
)


class InvalidMoveError(Exception):
    pass

class NotEncapsulatedException(Exception):
    pass

class NotAnEyeError(Exception):
    pass

class Coords(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return self.__class__(new_x, new_y)

    def __str__(self):
        return 'Coords({},{})'.format(self.x, self.y)
    def __repr__(self):
        return 'Coords({},{})'.format(self.x, self.y)
    def __content__(self):
        return 'Coords({},{})'.format(self.x, self.y)

    def __eq__(self, other):
        value = (self.x == other.x) and (self.y == other.y)
        return value

NWES = [
    Coords(-1, 0),
    Coords(0, -1),
    Coords(0, 1),
    Coords(1, 0),
]

def alphanumerical_coordinate(coordinate):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    i, j = coordinate.x, coordinate.y
    alphanumerical = alphabet[j] + str(i+1)
    return alphanumerical

class Board(object):
    def __init__(self, boardsize=2):
        self.boardsize = boardsize
        self.board = np.zeros(
            (self.boardsize, self.boardsize), dtype=object
        )
        self.board.fill(
            NoStone()
        )
        self.history = []
        self.explicit_history = []
        self.pockets = {BLACK: [], WHITE: []}

    def print_history(self):
        for (stone, coordinate) in self.history:
            print(stone, alphanumerical_coordinate(coordinate))

    def calculate_scores(self):
        scores = {
            BLACK: len(self.pockets[BLACK]),
            WHITE: len(self.pockets[WHITE]),
        }
        counted_coords = []
        for (x, y) in product(range(self.boardsize), range(self.boardsize)):
            try:
                if Coords(x, y) not in counted_coords:
                    eye, color = self.points_in_eye(Coords(x, y))
                    counted_coords.extend(eye)
                    scores[color] += len(eye)
            except NotAnEyeError:
                pass
        return scores

    def add_stone(self, stone, xy):
        print('add_stone', stone, xy)
        saved_board = copy(self.board)  # if something illegal occurs
        if isinstance(self.board[xy.x, xy.y], PlayerStone):
            print('Square occupied!')
            raise InvalidMoveError
        else:
            for direction in NWES:
                neighbour = xy + direction
                if (-1 < neighbour.x < self.boardsize) and \
                    (-1 < neighbour.y < self.boardsize):
                    if isinstance(self.board[neighbour.x, neighbour.y], PlayerStone):
                        self.maybe_remove(
                            stone,
                            neighbour
                        )

            group, libertypoints = self.liberties(xy, future_color=stone.color)
            if not self.check_history(stone, xy):
                print('Illegal Ko! Returning')
                self.board = saved_board
                raise InvalidMoveError

            elif len(libertypoints) > 0:
                self.board[xy.x, xy.y] = stone
                self.history.append((stone, xy))
                self.explicit_history.append(copy(self.board))
            else:
                print('Illegal move!')  # Again, maybe return to
                                        # self.board = saved_board ??
                print(group)
                print(libertypoints)
                print(stone)
                print(xy)
                print(self.board)
                raise InvalidMoveError

    def check_history(self, stone, xy):
        proxy_board = copy(self.board)
        proxy_board[xy.x, xy.y] = stone
        for historic_board in self.explicit_history:
            if (historic_board == proxy_board).all().all():
                print('Ko fight yo')
                return False
        return True

    def maybe_remove(self, stone, neighbour):
        pot_stone = self.board[neighbour.x, neighbour.y]
        if pot_stone.color == stone.enemy_color:
            group, libertypoints = self.liberties(neighbour)
            if len(libertypoints) == 1:  # GIVEN THAT WE ARE PUTTING IN A STONE
                self.remove(
                    color=stone.color,
                    group=group
                )

    def remove(self, color, group):
        for xy in group:
            self.pockets[color].append(self.board[xy.x, xy.y])
            self.board[xy.x, xy.y] = NoStone()

    def points_in_eye(self, xy):
        """
        xy: Coords

        Returns
        -------
        points : int
        surrounding_color : Player
        """
        if not isinstance(self.board[xy.x, xy.y], NoStone):
            raise NotAnEyeError
        def check_space(ij):
            for direction in NWES:
                new_ij = ij + direction
                if new_ij in eye + surrounding:
                    pass
                elif (not -1 < new_ij.x < self.boardsize) or \
                    (not -1 < new_ij.y < self.boardsize):
                    pass
                else:
                    if isinstance(self.board[new_ij.x, new_ij.y], PlayerStone):
                        surrounding.append(new_ij)
                        surrounding_colors.add(self.board[new_ij.x, new_ij.y].color)  # FIXME
                    elif isinstance(self.board[new_ij.x, new_ij.y], NoStone):
                        eye.append(new_ij)
                        check_space(new_ij)
                    else:
                        raise Exception('what is going on here?')

        eye = [xy, ]
        surrounding = []
        surrounding_colors = set()
        check_space(xy)
        if len(surrounding_colors) == 0:
            print('wtf')
            raise Exception
        elif len(surrounding_colors) == 2:
            raise NotEncapsulatedException
        else:
            surrounding_color = surrounding_colors.pop()

        return eye, surrounding_color

    def liberties(self, xy, future_color=None):
        def check_liberties(ij):
            for direction in NWES:
                new_ij = ij + direction
                if new_ij in group + libertypoints:
                    pass
                elif (not -1 < new_ij.x < self.boardsize) or \
                    (not -1 < new_ij.y < self.boardsize):
                    pass
                else:
                    if isinstance(self.board[new_ij.x, new_ij.y], NoStone):
                        libertypoints.append(new_ij)
                    elif self.board[new_ij.x, new_ij.y].color == color:
                        group.append(new_ij)
                        check_liberties(new_ij)

        color = self.board[xy.x, xy.y].color if future_color is None else future_color
        group = [xy, ]
        libertypoints = []
        check_liberties(xy)

        return group, libertypoints
                    

