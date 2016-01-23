from __future__ import print_function, division

import numpy as np

from bisect import bisect_left
from functools import partial
from matplotlib import pyplot as plt

from rendering import plot_board, OnClick
from game import (
    Board,
    WhiteStone,
    BlackStone,
    PlayerStone,
    Coords,
    InvalidMoveError,
    NotEncapsulatedException,
    WHITE,
    BLACK,
)


class Player(object):
    def __init__(self, name='rudolph', color=BLACK):
        self.name = name
        self.color = color

    def pick_up_stone(self):
        stone = BlackStone() if self.color==BLACK else WhiteStone()
        return stone

class Game(object):
    def __init__(
        self,
        boardsize=19,
        player1=Player('Bertil', BLACK),
        player2=Player('Whitney', WHITE),
    ):
        self.players = [player1, player2]
        self.board = Board(boardsize=boardsize)

    def __call__(  # WHAT TO CALL IT?
        self,
    ):
        self.play()
        self.settle_score()

        pygame.quit()

    def settle_score(self):
        print('TIME TO SETTLE SCORE')
        if self.board.boardsize == 19:
            size = (512, 512)  # Could be calculated from board size
        # image is 512 x 512
        else:
            size = (211, 211)
            # image is 211 x 211
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('BadukClient')
        clock = pygame.time.Clock()

        loopnotover = True
        while loopnotover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loopnotover = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        try:
                            scores = self.board.calculate_scores()
                            print(scores)
                            loopnotover = False
                        except NotEncapsulatedException:
                            print('Not encapsulated!')
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    try:
                        idx, idy = self._calc_position(x, y)
                        stone = self.board.board[idx, idy]
                        if isinstance(stone, PlayerStone):
                            group, libertypoints = self.board.liberties(
                                Coords(idx, idy),
                            )
                            self.board.remove(stone.enemy_color, group)
                        print(self.board.pockets)
                    except InvalidMoveError:
                        print('invalid move!')

            plot_board(screen=screen, board=self.board)
            clock.tick(60)

    def play(self):
        print('TIME TO PLAY')
        if self.board.boardsize == 19:
            size = (512, 512)  # Could be calculated from board size
        # image is 512 x 512
        else:
            size = (211, 211)
            # image is 211 x 211

        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('BadukClient')
        next_player = 0

        clock = pygame.time.Clock()
        gamenotover = True
        last_move_was_a_pass = False
        while gamenotover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gamenotover = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        print('That is a pass!')
                        next_player = 1 - next_player
                        if last_move_was_a_pass:
                            gamenotover = False
                        else:
                            last_move_was_a_pass = True
                    if event.key == pygame.K_q:
                        gamenotover = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    try:
                        idx, idy = self._calc_position(x, y)
                        stone = self.players[next_player].pick_up_stone()
                        self.board.add_stone(
                            stone,
                            Coords(idx, idy)
                        )
                        next_player = 0 if next_player else 1
                        last_move_was_a_pass = False
                    except InvalidMoveError:
                        print('invalid move!')

            plot_board(screen=screen, board=self.board)
            clock.tick(60)

    def _calc_position(self, x, y):
        if self.board.boardsize == 19:
            border_width = 45
            jump = 23.5
        elif self.board.boardsize == 9:
            border_width = 14
            jump = 23
        borders = [border_width-jump/2+i*jump for i in range(self.board.boardsize + 1)]
        id_x = bisect_left(borders, x) - 1
        id_y = bisect_left(borders, y) - 1
        if (id_x not in range(self.board.boardsize)) or (id_y not in range(self.board.boardsize)):
            raise InvalidMoveError
        return id_x, id_y

def main():
    game = Game(9)
    game()

if __name__ == '__main__':
    import pygame
    pygame.init()
    main()
