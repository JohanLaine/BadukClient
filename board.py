from __future__ import division, print_function

import numpy as np

from copy import copy
from itertools import product

from stones import (
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
        self.board = np.ones(
            (self.boardsize, self.boardsize)
        ).astype(int) * -1  # Would maybe be better with [[str]]
        self.history = []
        self.explicit_history = []
        self.pockets = [[], []]

    def print_history(self):
        for (stone, coordinate) in self.history:
            print(stone, alphanumerical_coordinate(coordinate))

    def calculate_scores(self):
        scores = map(len, self.pockets)
        counted_coords = []
        for (x, y) in product(range(self.boardsize), range(self.boardsize)):
            try:
                if Coords(x, y) not in counted_coords:
                    eye, eye_player = self.points_in_eye(Coords(x, y))
                    counted_coords.extend(eye)
                    scores[eye_player] += len(eye)
            except NotAnEyeError:
                pass
        return scores

    def add_stone(self, current_player, xy):
        saved_board = copy(self.board)  # if something illegal occurs
        if self.board[xy.x, xy.y] != -1:
            print('Square occupied!')
            raise InvalidMoveError
        else:
            for direction in NWES:
                neighbour = xy + direction
                if (-1 < neighbour.x < self.boardsize) and \
                    (-1 < neighbour.y < self.boardsize):
                    if self.board[neighbour.x, neighbour.y] != -1:
                        self.maybe_remove(
                            current_player=current_player,
                            neighbour=neighbour
                        )

            group, libertypoints = self.liberties(xy, current_player=current_player)
            if not self.check_history(current_player, xy):
                print('Illegal Ko! Returning')
                self.board = saved_board
                raise InvalidMoveError

            elif len(libertypoints) > 0:
                self.board[xy.x, xy.y] = current_player
                self.history.append((current_player, xy))
                self.explicit_history.append(copy(self.board))
            else:
                print('Illegal move!')  # Again, maybe return to
                                        # self.board = saved_board ??
                print(group)
                print(libertypoints)
                print(current_player)
                print(xy)
                print(self.board)
                raise InvalidMoveError

    def check_history(self, current_player, xy):
        proxy_board = copy(self.board)
        proxy_board[xy.x, xy.y] = current_player
        for historic_board in self.explicit_history:
            if (historic_board == proxy_board).all().all():
                print('Ko fight yo')
                return False
        return True

    def maybe_remove(self, current_player, neighbour):
        pot_stone_number = self.board[neighbour.x, neighbour.y]
        if pot_stone_number != current_player:
            group, libertypoints = self.liberties(neighbour)
            if len(libertypoints) == 1:  # GIVEN THAT WE ARE PUTTING IN A STONE
                self.remove(
                    current_player=current_player,
                    group=group
                )

    def remove(self, current_player, group):
        for xy in group:
            self.pockets[current_player].append(self.board[xy.x, xy.y])
            self.board[xy.x, xy.y] = -1

    def points_in_eye(self, xy):
        """
        xy: Coords

        Returns
        -------
        points : int
        surrounding_color : Player
        """
        if self.board[xy.x, xy.y] != -1:
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
                    if self.board[new_ij.x, new_ij.y] != -1:
                        surrounding.append(new_ij)
                        surrounding_colors.add(self.board[new_ij.x, new_ij.y])  # FIXME
                    elif self.board[new_ij.x, new_ij.y] == -1:
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

    def liberties(self, xy, current_player=None):
        def check_liberties(ij):
            for direction in NWES:
                new_ij = ij + direction
                if new_ij in group + libertypoints:
                    pass
                elif (not -1 < new_ij.x < self.boardsize) or \
                    (not -1 < new_ij.y < self.boardsize):
                    pass
                else:
                    if self.board[new_ij.x, new_ij.y] == -1:
                        libertypoints.append(new_ij)
                    elif self.board[new_ij.x, new_ij.y] == color_number:
                        group.append(new_ij)
                        check_liberties(new_ij)

        color_number = self.board[xy.x, xy.y] if current_player is None else current_player
        group = [xy, ]
        libertypoints = []
        check_liberties(xy)

        return group, libertypoints
                    

