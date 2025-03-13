from typing import Tuple

import numpy as np

def mask8(
        i_a: Tuple[int, int, int, int, int, int, int, int],
        i_value: int) -> Tuple[int, int, int, int, int, int, int, int]:
    """Convert 8 neighbors to binary mask (1 if matches value, 0 otherwise)"""
    return (
        i_a[0] == i_value,
        i_a[1] == i_value,
        i_a[2] == i_value,
        i_a[3] == i_value,
        i_a[4] == i_value,
        i_a[5] == i_value,
        i_a[6] == i_value,
        i_a[7] == i_value
    )


def combine8(
        i_a: Tuple[int, int, int, int, int, int, int, int],
        i_b: Tuple[int, int, int, int, int, int, int, int]) \
        -> Tuple[int, int, int, int, int, int, int, int]:
    """Combine two binary masks using logical OR operation"""
    return (
        i_a[0] or i_b[0],
        i_a[1] or i_b[1],
        i_a[2] or i_b[2],
        i_a[3] or i_b[3],
        i_a[4] or i_b[4],
        i_a[5] or i_b[5],
        i_a[6] or i_b[6],
        i_a[7] or i_b[7]
    )


def simplify8(i_a: Tuple[int, int, int, int, int, int, int, int]) \
        -> Tuple[int, int, int, int, int, int, int, int]:
    """Remove redundant corner tiles that don't affect border appearance"""
    return (
        0 if i_a[0] and (not i_a[1] or not i_a[3]) else i_a[0],
        i_a[1],
        0 if i_a[2] and (not i_a[1] or not i_a[4]) else i_a[2],
        i_a[3],
        i_a[4],
        0 if i_a[5] and (not i_a[6] or not i_a[3]) else i_a[5],
        i_a[6],
        0 if i_a[7] and (not i_a[6] or not i_a[4]) else i_a[7]
    )


def code8(i_a: Tuple[int, int, int, int, int, int, int, int]) -> int:
    """Convert 8-connected binary mask to numeric code"""
    return i_a[0] + 2 * i_a[1] + 4 * i_a[2] + 8 * i_a[3] \
           + 16 * i_a[4] + 32 * i_a[5] + 64 * i_a[6] + 128 * i_a[7]


def decode8(i_code: int) -> Tuple[int, int, int, int, int, int, int, int]:
    """Convert numeric code back to 8-connected binary mask"""
    return (
        i_code & 1,
        (i_code & 2) // 2,
        (i_code & 4) // 4,
        (i_code & 8) // 8,
        (i_code & 16) // 16,
        (i_code & 32) // 32,
        (i_code & 64) // 64,
        (i_code & 128) // 128
    )

weights8 = np.array((1, 2, 4, 8, 16, 32, 64, 128))


def code8np(a: np.ndarray) -> np.ndarray:
    return a.dot(weights8)