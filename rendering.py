from __future__ import division, print_function

import numpy as np

from matplotlib import pyplot as plt
from time import time

from game import Board, BlackStone, WhiteStone, Coords
import pygame

WHITE = (255, 255, 255)  # TRIPLICATION
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

def OnClick(event, board, stone):
    i = int(event.xdata)
    j = int(event.ydata)
    board.add_stone(stone, Coords(i, j))
    print(board.board)
    plt.clf()
    plt.close(plt.gcf())


def plot_board(screen, board):
    if board.boardsize == 19:
        background_path = 'background.jpg'
        border_width = 45
        jump = 23.5
        stone_size = 10
    elif board.boardsize == 9:
        background_path = '9x9board.png'
        border_width = 14
        jump = 23
        stone_size = 10
        
    background_image = pygame.image.load(background_path).convert()
    screen.blit(background_image, [0, 0])

    for (x, y), thing in np.ndenumerate(board.board):
        if thing.color != GREY:
            pygame.draw.circle(
                screen,
                thing.color,
                [
                    int(border_width + x*jump),
                    int(border_width + y*jump),
                ],
                stone_size
            )

    pygame.display.flip()