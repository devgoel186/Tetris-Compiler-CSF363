from typing import NamedTuple

Color = NamedTuple("Color", [("r", int), ("g", int), ("b", int)])
'''A tuple of R G B values.'''

BGCOLOR = Color(35, 35, 35)

BLACK = Color(0, 0, 0)
'''(0, 0, 0)'''
WHITE = Color(255, 255, 255)
'''(255, 255, 255)'''

BOARD_WIDTH = 0
BOARD_HEIGHT = 0

SHAPES = {

}

GLOBAL_COLORS = {

}

SEQUENCES = {

}

GAME = {

}

COLORS: list[Color] = [
    (0,   0,   0),  # BLACK
    (255, 85,  85),  # ORANGE
    (100, 200, 115),  # GREEN
    (120, 108, 245),  # MEDIUM BLUE
    (255, 140, 50),  # SAFFRON
    (50,  120, 52),  # DARK GREEN
    (146, 202, 73),  # YELLOW GREEN
    (150, 161, 218),  # PURPLE
    (120, 180, 160),  # GREYISH GREEN
    (228, 12, 15),  # RED
    (11, 11, 96),  # DARK BLUE
    (252, 214, 59),  # YELLOW
    (35,  35,  35),  # Helper color for background grid
]


LINE_SCORES: list[int] = []

LVL_SPEED_MOD: dict[int, int] = {}

FPS = 60


def set_parameters(levelmap):
    for i, key in enumerate(levelmap):
        levelname = key
        level = levelmap[key]

        global SHAPES
        SHAPES[levelname] = level.pieces_list

        global GLOBAL_COLORS
        GLOBAL_COLORS[levelname] = level.colors_list

        global SEQUENCES
        SEQUENCES[levelname] = level.sequences_list

        global GAME
        GAME[levelname] = level.startgame_list
        print(GAME)

        global BOARD_HEIGHT, BOARD_WIDTH
        BOARD_HEIGHT, BOARD_WIDTH = level.board[0], level.board[1]

        global LINE_SCORES
        LINE_SCORES = level.scoring

        global LVL_SPEED_MOD
        LVL_SPEED_MOD[i] = level.levelspeed * 50

    from game import playgamenow
    playgamenow()
