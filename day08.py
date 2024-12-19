from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

from utils import BoundedGrid, XYCoord


@dataclass(frozen=True)
class Antenna(XYCoord):
    def antinode(self, other: "Antenna") -> XYCoord:
        """
        Finds the antinode position for this Antenna relative to other
        The antinode will be exactly opposite other on the grid
        """
        return self + (self - other)

    def as_xycoord(self) -> XYCoord:
        return XYCoord(self.x, self.y)


class AntennaMap(BoundedGrid):
    def __init__(self, path: str):
        self.antennae: dict[str, list[Antenna]] = defaultdict(list)

        with open(path, "r") as fp:
            for i, line in enumerate(fp.readlines()):  # i == y
                for j, char in enumerate(line.strip()):  # j == x
                    if char != ".":
                        self.antennae[char].append(Antenna(j, i))

        super().__init__(j, i)

    def find_antinodes(self) -> int:
        """
        Find all antinodes on the map
        Return the number of unique antinode positions
        """
        all_antis = set()
        for freq, antennae in self.antennae.items():
            for a, b in combinations(antennae, 2):
                a_anti = a.antinode(b)
                b_anti = b.antinode(a)
                if self._within_bounds(a_anti):
                    all_antis.add(a_anti)
                if self._within_bounds(b_anti):
                    all_antis.add(b_anti)

        return len(all_antis)

    def find_resonant_antinodes(self) -> int:
        """
        Find all antinodes on the map, taking into account resonant harmonics
        Resonant harmonics means that there are antinodes at every position along the
        line created by two antennae, evenly spaced by the distance between the two antennae

        Return the number of unique antinode positions
        """
        all_antis = set()

        for freq, antennae in self.antennae.items():
            for a, b in combinations(antennae, 2):
                # The positions of the two antennae are themselves antinodes
                all_antis.update([a.as_xycoord(), b.as_xycoord()])

                # Find all antinodes starting from a and working away from b
                dist = a - b
                antinode = a + dist
                while self._within_bounds(antinode):
                    all_antis.add(antinode)
                    antinode = antinode + dist

                # Find all antinodes starting from b and working away from a
                dist = b - a
                antinode = b + dist
                while self._within_bounds(antinode):
                    all_antis.add(antinode)
                    antinode = antinode + dist

        return len(all_antis)


if __name__ == "__main__":
    path = "inputs/day08"
    map = AntennaMap(path)

    all_found = map.find_antinodes()
    print("Number of identified antinodes:", all_found)

    found = map.find_resonant_antinodes()
    print("Number of resonant antinodes identified:", found)
