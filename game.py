from __future__ import division, print_function

import numpy as np

from PodSixNet.Connection import connection, ConnectionListener

from bisect import bisect_left
from functools import partial
from matplotlib import pyplot as plt
import traceback
import re
import time
import sys

import pygame
from pygame.locals import *  # Bad idea

from ttt_core import EngineV4

from rendering import plot_board, OnClick
from board import (
    Board,
    Coords,
    InvalidMoveError,
    NotEncapsulatedException,
)
from stones import (
    WHITE,
    BLACK
)


class Player(object):
    def __init__(self, name='rudolph', color=BLACK):
        self.name = name
        self.color = color


class BadukEngine(EngineV4):
    @property
    def screen_size(self):
        if self.board.boardsize == 19:
            size = (512, 512)  # Could be calculated from board size
        # image is 512 x 512
        else:
            size = (211, 211)
            # image is 211 x 211
        return size

    def Network_go_to_scoring(self, data):
        self.running = False

    def start(
        self,
    ):
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        self.running = True # unnecessary?
        try:
            self.startup()
            while self.running:
                for event in pygame.event.get():
                    if event.type == ACTIVEEVENT:       self.current_screen._handle_active(event)
                    if event.type == KEYDOWN:           self.current_screen._handle_keydown(event)
                    if event.type == KEYUP:             self.current_screen._handle_keyup(event)
                    if event.type == MOUSEBUTTONUP:     self.current_screen._handle_mouseup(event)
                    if event.type == MOUSEBUTTONDOWN:   self.current_screen._handle_mousedown(event)
                    if event.type == MOUSEMOTION:       self.current_screen._handle_mousemotion(event)
                    if event.type == QUIT:              self.current_screen.quit(event)
                
                # Check to see if a key has been held down
                self.current_screen._handle_keyhold()
                
                connection.Pump()
                self.Pump()

                self.current_screen.update()
                self.current_screen.redraw()
        except Exception as e:
            print("")
            traceback.print_exc(file=sys.stdout)
            connection.Send({'action': 'quit'})
            
            if self.current_screen != None:
                self.current_screen.quit()
            raise

        print('HEJHEJHEJ')
        print('HEJHEJHEJ')
        print('HEJHEJHEJ')
        
#        self.play()
#        self.settle_score()

        pygame.quit()

#    def settle_score(self):
#        print('TIME TO SETTLE SCORE')
#        if self.board.boardsize == 19:
#            size = (512, 512)  # Could be calculated from board size
#        # image is 512 x 512
#        else:
#            size = (211, 211)
#            # image is 211 x 211
#        screen = pygame.display.set_mode(size)
#        pygame.display.set_caption('BadukClient')
#        clock = pygame.time.Clock()
#
#        while True:
#            if not self.settle_score_controllertick():
#                return
#
#            plot_board(screen=screen, board=self.board)
#            clock.tick(60)

#    def settle_score_controllertick(self):
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                return False
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_q:
#                    try:
#                        scores = self.board.calculate_scores()
#                        print(scores)
#                        return False
#                    except NotEncapsulatedException:
#                        print('Not encapsulated!')
#            if event.type == pygame.MOUSEBUTTONUP:
#                x, y = pygame.mouse.get_pos()
#                try:
#                    idx, idy = self._calc_position(x, y)
#                    stone = self.board.board[idx, idy]
#                    if isinstance(stone, PlayerStone):
#                        group, libertypoints = self.board.liberties(
#                            Coords(idx, idy),
#                        )
#                        self.board.remove(stone.enemy_color, group)
#                    print(self.board.pockets)
#                except InvalidMoveError:
#                    print('invalid move!')
#
#        return True

#    def play_controllertick(self):
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                return False
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_p:
#                    print('That is a pass!')
#                    self.next_player = 1 - self.next_player
#                    if self.last_move_was_a_pass:
#                        return False
#                    else:
#                        self.last_move_was_a_pass = True
#                if event.key == pygame.K_q:
#                    return False
#            if event.type == pygame.MOUSEBUTTONUP:
#                x, y = pygame.mouse.get_pos()
#                try:
#                    idx, idy = self._calc_position(x, y)
#                    stone = self.players[self.next_player].pick_up_stone()
#                    self.board.add_stone(
#                        stone,
#                        Coords(idx, idy)
#                    )
#                    self.next_player = 1 - self.next_player
#                    self.last_move_was_a_pass = False
#                except InvalidMoveError:
#                    print('invalid move!')
#
#        return True

#    def play(self):
#        print('TIME TO PLAY')
#        if self.board.boardsize == 19:
#            size = (512, 512)  # Could be calculated from board size
#        # image is 512 x 512
#        else:
#            size = (211, 211)
#            # image is 211 x 211
#
#        surface = pygame.display.set_mode(size)
#        pygame.display.set_caption('BadukClient')
#        self.next_player = 0
#
#        clock = pygame.time.Clock()
#        self.last_move_was_a_pass = False
#        while True:
#            if not self.play_controllertick():
#                return
#
#            # What HAPPENS HERE??
#            1/0
#            plot_board(surface=surface, board=self.board)
#            clock.tick(60)

#    def _calc_position(self, x, y):
#        if self.board.boardsize == 19:
#            border_width = 45
#            jump = 23.5
#        elif self.board.boardsize == 9:
#            border_width = 14
#            jump = 23
#        borders = [border_width-jump/2+i*jump for i in range(self.board.boardsize + 1)]
#        id_x = bisect_left(borders, x) - 1
#        id_y = bisect_left(borders, y) - 1
#        if (id_x not in range(self.board.boardsize)) or (id_y not in range(self.board.boardsize)):
#            raise InvalidMoveError
#        return id_x, id_y


from ttt_screen import Screen
class BadukScreen(Screen):
    def redraw(self):
        if time.time() < self._next_redraw:
            return

        surf = self.engine.display
        plot_board(surf, board=self.state)
        self._next_redraw = time.time() + self._redraw_delay

    def handle_mouseup(self, event, drag=False):
        x, y = event.pos
        try:
            idx, idy = self._calc_position(x, y)
        except InvalidMoveError:
            print('invalid move!')
            return

        self.make_move(idx, idy)

    def handle_keydown(self, event):
        if event.key == pygame.K_p:
            self.make_pass_move()
    
    def _calc_position(self, x, y):
        boardsize = len(self.state)
        if boardsize == 19:
            border_width = 45
            jump = 23.5
        elif boardsize == 9:
            border_width = 14
            jump = 23
        borders = [border_width-jump/2+i*jump for i in range(boardsize + 1)]
        id_x = bisect_left(borders, x) - 1
        id_y = bisect_left(borders, y) - 1
        if (id_x not in range(boardsize)) or (id_y not in range(self.board.boardsize)):
            raise InvalidMoveError
        return id_x, id_y
