import os
from dataclasses import dataclass
@dataclass
class Coordinate:
    x: int
    y: int
@dataclass
class Path:
    coordinates: list[Coordinate]
    identifier: int
    def length(self):
        return len(self.coordinates)
@dataclass
class Solution:
    paths: list[Path]
    time: float
    def makespan(self):
        if not self.paths:
            return 0
        return max(path.length() for path in self.paths)
    def sumOfCosts(self):
        return sum(path.length() for path in self.paths)
    def verifyCollisions(self):
        max_length = self.makespan()
        for i in range(max_length):
            occupied_locations = set()
            for path in self.paths:
                coord_index = min(i, path.length() - 1)
                current_loc = (path.coordinates[coord_index].x, path.coordinates[coord_index].y)
                if current_loc in occupied_locations:
                    return False
                occupied_locations.add(current_loc)
        return True
def parse(filepath):
    """Parses a solution file and returns a Solution object."""
    paths = []
    time_val = 0.0
    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            if i == 0:
                time_val = float(line[5:])
            else:
                parts = line.split("\t")
                identifier = int(parts[0])
                coords = []
                for j in range(1, len(parts), 2):
                    if j + 1 < len(parts):
                        x = int(parts[j])
                        y = int(parts[j+1])
                        coords.append(Coordinate(x, y))
                paths.append(Path(coordinates=coords, identifier=identifier))

    return Solution(paths=paths, time=time_val)

if __name__ == "__main__":
	print("Solution Verification")
	x = parse("./solutionexample.sol")
	print(x.verifyCollisions())
	print(x.makespan())
	print(x.sumOfCosts())
