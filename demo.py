"""Short examples for the demo menu option."""

from random import choice


CASES = (
    ("bananabananabandana", "banana"),
    ("ababababababa", "ababa"),
    ("mississippiriver", "issip"),
    ("hellomatchingworld", "planet"),
    ("kitten", "kittens"),
)


def choose_demo():
    return choice(CASES)
