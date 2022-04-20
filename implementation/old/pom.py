from typing import Tuple


def p1((x, y): Tuple[int, int]) -> int:
    return x[0]


def p2(x: Tuple[int, int]) -> int:
    return x[1]
