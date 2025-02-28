from typing import Tuple

def vectorAddI(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    """Add two integer vectors component-wise."""
    return v1[0] + v2[0], v1[1] + v2[1]

def vectorSubI(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    """Subtract two integer vectors component-wise."""
    return v1[0] - v2[0], v1[1] - v2[1]

def vectorMulI(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    """Multiply two integer vectors component-wise."""
    return v1[0] * v2[0], v1[1] * v2[1]

def vectorDivI(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    """Divide two integer vectors component-wise using integer division."""
    return v1[0] // v2[0], v1[1] // v2[1]

def vectorAddF(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    """Add two float vectors component-wise."""
    return v1[0] + v2[0], v1[1] + v2[1]

def vectorSubF(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    """Subtract two float vectors component-wise."""
    return v1[0] - v2[0], v1[1] - v2[1]

def vectorMulF(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    """Multiply two float vectors component-wise."""
    return v1[0] * v2[0], v1[1] * v2[1]

def vectorDivF(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    """Divide two float vectors component-wise."""
    return v1[0] / v2[0], v1[1] / v2[1]