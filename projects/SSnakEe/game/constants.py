"""Visi spēles skaitļi vienuviet."""

# Režģis
DEFAULT_GRID_SIZE = 25
GRID_OPTIONS = [15, 20, 25, 30]

# Ātrums (bāzes intervāls sekundēs starp soļiem)
SPEED_OPTIONS = [
    ("Slow",   0.18),
    ("Normal", 0.13),
    ("Fast",   0.09),
    ("Insane", 0.06),
]
DEFAULT_SPEED_INDEX = 1

# Automātiskā grūtība (augoša)
DIFFICULTY_INTERVAL = 20.0
DIFFICULTY_FACTOR = 0.9
MIN_MOVE_INTERVAL = 0.04

# Ēdiens
FOOD_POINTS = 5
SECOND_POINTS = 1
MULTI_FOOD_COUNT = 5

# Magnēts
MAGNET_CHECK_EVERY = 4.0
MAGNET_MIN_ELAPSED = 8.0
MAGNET_SPAWN_CHANCE = 0.35
MAGNET_MAX_PER_GAME = 2
MAGNET_LIFETIME = 12.0

# Spēlētāja kontrole
INVERT_P1_AD = False

# Krāsas
BG_COLOR = (45, 52, 68)
GRID_COLOR = (60, 68, 88)
FOOD_COLOR = (230, 90, 90)
FOOD_BORDER = (180, 50, 50)

P1_BODY = (245, 245, 250)
P1_HEAD = (230, 190, 60)

P2_BODY = (100, 180, 255)
P2_HEAD = (60, 130, 220)

MAGNET_COLOR = (255, 100, 200)
MAGNET_BORDER = (200, 40, 140)