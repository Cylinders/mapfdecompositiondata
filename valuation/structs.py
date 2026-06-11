import numpy as np
import numpy.typing as npt
from typing import NamedTuple, Tuple

type Grid = npt.NDArray[np.bool_]

type GridPath = list[tuple[int, int]]


class Agent(NamedTuple):
    start: Tuple[int, int]
    goal: Tuple[int, int]
