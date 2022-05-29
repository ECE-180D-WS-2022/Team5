WIN_HEIGHT = 480
WIN_WIDTH = 640 # old
MULT_WIN_HEIGHT = 608
MULT_WIN_WIDTH = 1024
TILE_SIZE = 32
FPS = 60

CHOP_TIMES = 3
STIR_TIMES = 3

PLAYER_SPEED = 2

BACKGROUD_LAYER = 1
DECORATION_LAYER = 4
COUNTER_BACK_LAYER = 7
COUNTER_BACK_ITEMS_LAYER = 10 # 11, 12, 13, 14, 15, 16
COUNTER_LAYER = 17 # 18, 19
CURSOR_LAYER = 17
COUNTER_ITEMS_LAYER = 20 # 21, 22, 23, 24, 25, 26, 27
PLAYER_LAYER = 28 # 29, 30
COUNTER_FRONT_LAYER = 31 # 32, 33
COUNTER_FRONT_ITEMS_LAYER = 34 # 35, 36, 37, 38, 39, 40

# CURSOR_LAYER = 4
# PLAYER_LAYER = 5
# COUNTERTOP_LAYER = 6
# COUNTER_FRONT_LAYER = 6
# COUNTER_LAYER = 4


# FOREGROUND_LAYER = 7

PLATE_LAYER = 1
BOTTOM_BUN_LAYER = 2
LETTUCE_LAYER = 3
MEAT_LAYER = 4
TOMATO_LAYER = 5
TOP_BUN_LAYER = 6

BLACK = (0,0,0)

cover_height = 20

IDLE_FRAMES = 6
RUN_FRAMES = 6
PICKUP_FRAMES = 12
PUTDOWN_FRAMES = 10
STIR_FRAMES = 6
CHOP_FRAMES = 6
SPEAK_FRAMES = 8

FRIDGE_OPEN_FRAMES = 6
FRIDGE_CLOSE_FRAMES = 4

INVENTORY_X = 32*7
INVENTORY_Y = 32*19
INVENTORY_LAYER = 17

mult_counter_tilemap_back = [
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '.....TTTT........TTTT...........',
    '....A!^()BB%B%BCA!^()BB%B%BC....',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
]

mult_counter_tilemap_back_items = [
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '...........XWXW........XWXW.....',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
]

mult_counter_tilemap = [
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '....GEEEEJJSJSJHGEEEEJJSJSJH....',
    '....G..........HG..........H....',
    '....G..........HG..........H....',
    '....G..........HG..........H....',
    '....M......JJJJHM......JJJJH....',
    '....G..........HG..........H....',
    '....G..........*G..........*....',
    '....G..........HG..........H....',
    '....G..........HG..........H....',
    '....G..........HG..........H....',
    '.V..D..........FD..........F..V.',
    '................................',
]

mult_counter_tilemap_2 = [
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '...........BBBB........BBBB.....',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '....DBBBBB$BB$BFDBBBBB$BB$BF....',
    '....IJJJJJJJJJJKIJJJJJJJJJJK....',
]

mult_counter_items_tilemap = [
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................0...........0...',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
]

mult_counter_front_items_tilemap = [
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '................................',
    '...............0...........0....',
    '................................',
    '................................',
    '..........ZY.ZY.......ZY.ZY.....',
    '................................',
]

# green_counter = {
#     "A": (128,32),
#     "B": (192,32),
#     "C": (64,0),
#     "D": (0,32),
#     "E": (32,32),
#     "F": (64,32),
#     "G": (0,64),
#     "H": (64,64),
#     "I": (0,96),
#     "J": (32,96),
#     "K": (64,96),
#     "L": (32,0),
# }

white_counter = {
    "A": (0,32),
    "B": (160,32),
    "C": (32,32),
    "D": (0,96),
    "F": (32,96),
    "G": (0,64),
    "M": (0,64),
    "H": (32,64),
    "I": (64,320),
    "J": (96,320),
    "K": (128,320),
    "!": (288,768),
    "E": (288,800),
    "*": (64,192),
    "%": (256,416),
    "S": (256,448),
    "T": (288,736),
}

front_items = {
   "Z": (352,1120), # cutting board
   "Y": (384,1152),  # knife
}

back_items = {
    "X": (448,1120),  # pan
    "W": (480,1120),  # pan handle
}