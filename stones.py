from __future__ import division, print_function


WHITE = (255, 255, 255)  # DUPLICATION
GREY = (100, 100, 100)  # DUPLICATION
BLACK = (0, 0, 0)

class Stone(object):
    def __repr__(self):
        return self.short
    def __str__(self):
        return self.short
    def __content__(self):
        return self.short
    def __eq__(self, other):
        return self.color == other.color

class NoStone(Stone):
    short = '0'
    color = GREY

class PlayerStone(Stone):
    pass

class WhiteStone(PlayerStone):
    short = 'W'
    color = WHITE
    enemy_color = BLACK

class BlackStone(PlayerStone):
    short = 'B'
    color = BLACK
    enemy_color = WHITE
