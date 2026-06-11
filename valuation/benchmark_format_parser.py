from pathlib import Path

import numpy as np
import numpy.typing as npt

from structs import Agent


## map

# our evaluator only sees maps in terms of occupancy
def parse_map(grid: str) -> npt.NDArray[np.bool_]:
    lines = grid.splitlines()

    if len(lines) < 5:
        raise ValueError("map is missing header or grid data")

    if lines[0].strip() != "type octile":
        raise ValueError("expected first line: type octile")

    try:
        height = int(lines[1].split()[1])
        width = int(lines[2].split()[1])
    except (IndexError, ValueError) as e:
        raise ValueError("invalid height/width header") from e

    if lines[3].strip() != "map":
        raise ValueError("expected fourth line: map")

    map_lines = lines[4:]

    if len(map_lines) != height:
        raise ValueError(f"expected {height} map rows, got {len(map_lines)}")

    occupancy = np.zeros((height, width), dtype=np.bool_)

    passable = {".", "G", "S", "W"}
    blocked = {"@", "O", "T"}

    for y, row in enumerate(map_lines):
        if len(row) != width:
            raise ValueError(f"row {y} expected width {width}, got {len(row)}")

        for x, ch in enumerate(row):
            if ch in passable:
                occupancy[y, x] = False
            elif ch in blocked:
                occupancy[y, x] = True
            else:
                raise ValueError(f"invalid map character {ch!r} at ({x}, {y})")

    return occupancy


def parse_map_from(path: str | Path) -> npt.NDArray[np.bool_]:
    return parse_map(Path(path).read_text(encoding="utf-8"))


## scenario
def parse_scenario(scenario: str) -> list[Agent]:
    lines = scenario.splitlines()

    if not lines:
        raise ValueError("empty scenario")

    first = lines[0].split()
    if len(first) < 2 or first[0] != "version":
        raise ValueError("scenario must start with 'version x.x'")

    agents: list[Agent] = []

    for line_no, line in enumerate(lines[1:], start=2):
        parts = line.split()

        if len(parts) != 9:
            raise ValueError(f"line {line_no}: expected 9 fields, got {len(parts)}")

        agent = Agent(
            # bucket=int(parts[0]),
            # map_name=parts[1],
            # map_width=int(parts[2]),
            # map_height=int(parts[3]),
            start=(int(parts[4]), int(parts[5])),
            goal=(int(parts[6]), int(parts[7])),
            # optimal_length=float(parts[8]),
        )

        agents.append(agent)

    return agents


def parse_scenario_from(path: str | Path) -> list[Agent]:
    return parse_scenario(Path(path).read_text(encoding="utf-8"))
