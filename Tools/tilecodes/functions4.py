from typing import Tuple

import numpy as np

def mask4(i_a: Tuple[int, int, int, int],
          i_value: int) -> Tuple[int, int, int, int]:
    """Convert neighbors to binary mask (1 if matches value, 0 otherwise)"""
    return (i_a[0] == i_value, i_a[1] == i_value,
            i_a[2] == i_value, i_a[3] == i_value)


def combine4(
        i_a: Tuple[int, int, int, int],
        i_b: Tuple[int, int, int, int]) \
        -> Tuple[int, int, int, int]:
    """Combine two binary masks using logical OR operation"""
    return (
        i_a[0] or i_b[0],
        i_a[1] or i_b[1],
        i_a[2] or i_b[2],
        i_a[3] or i_b[3]
    )


def code4(i_a: Tuple[int, int, int, int]) -> int:
    """Convert binary mask to numeric code using powers of 2"""
    return i_a[0] + 2 * i_a[1] + 4 * i_a[2] + 8 * i_a[3]

weights4 = np.array((1, 2, 4, 8))


def code4np(a: np.ndarray) -> np.ndarray:
    return a.dot(weights4)