import chess
import random as rng

# CONSTANTS

DEFAULT_FEN = "ppppkppp/pppppppp/8/8/8/8/PPPPPPPP/PPPPKPPP w - - 0 1"
WEIGHTED_PROBABILITY = [
    (chess.KNIGHT, 18),
    (chess.BISHOP, 18),
    (chess.ROOK, 8),
    (chess.QUEEN, 4)
]
SUM_WEIGHTED_PROB = sum(x for _, x in WEIGHTED_PROBABILITY)
GACHA_LIST = ['n', 'b', 'r', 'q']
PIECE_POINTS = {
    'p': 1,
    'n': 3,
    'b': 3,
    'r': 5,
    'q': 9
}


# FUNCTIONS

def rand(l: int, r: int) -> int:
    return rng.randint(l, r)