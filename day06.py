from concurrent.futures import ProcessPoolExecutor
from functools import partial

from utils import BoundedGrid, XYCoord

LOOP = object()


class LabMap(BoundedGrid):
    up = XYCoord(0, -1)
    right = XYCoord(1, 0)
    down = XYCoord(0, 1)
    left = XYCoord(-1, 0)

    def __init__(self, path: str):
        obstacles = []

        # The direction the guard is facing denoted as the change in position
        # when they move forward
        # Assume the guard is always facing up to start
        self.guard_facing = self.up

        with open(path, "r") as fp:
            for i, line in enumerate(fp.readlines()):  # i == y
                for j, char in enumerate(line):  # j == x
                    if char == "#":
                        obstacles.append(XYCoord(j, i))
                    elif char == "^":
                        self.guard = XYCoord(j, i)

        super().__init__(j, i)

        self.obstacles = obstacles

    def walk_guard(self) -> set[XYCoord] | object:
        """
        Have the guard patrol around the map until it exits the area
        - Will always walk in a straight line until it hits an obstacle
        - When hitting obstacle, will turn 90 degrees (clockwise) and then continue

        Returns the set of unique coordinates the guard visits on their patrol unless they
        encountered a loop, in which case returns a LOOP sentinal
        """
        # Visited will be all unique coordinates visited
        visited = set()
        # visited_window will be tuples of the previous three coords visited
        # when a duplicate shows up, that is an indication we're in a loop
        visited_window = set()
        looped = False

        def in_loop(current_window: tuple[XYCoord, XYCoord, XYCoord]) -> bool:
            # If the current last_three positions were previously visited
            # assume we're in a loop
            # print(last_three)
            return tuple(last_three) in visited_window

        last_three = []
        while self._within_bounds(self.guard):
            # print(self.guard, self.guard_facing)
            visited.add(self.guard)
            last_three.append(self.guard)

            if len(last_three) >= 3:
                last_three = last_three[-3:]

                if in_loop(tuple(last_three)):
                    looped = True
                    break

                visited_window.add(tuple(last_three))

            self._step_forward()

        return visited if not looped else LOOP

    def _step_forward(self) -> None:
        """
        Make the guard take a step forward, if it would step into an obstacle, turn 90 degrees clockwise instead
        """
        # Check if the position in front of us is an obstacle
        new_pos = self.guard + self.guard_facing

        if new_pos in self.obstacles:
            match self.guard_facing:
                case self.up:
                    self.guard_facing = self.right
                case self.right:
                    self.guard_facing = self.down
                case self.down:
                    self.guard_facing = self.left
                case self.left:
                    self.guard_facing = self.up
        else:
            self.guard = new_pos


def test_new_obstacle(pos, path):
    test_map = LabMap(path)
    test_map.obstacles.append(pos)
    return test_map.walk_guard()


def introduce_obstacles(path) -> int:
    """
    To a LabMap, add obstacles into the guard's path to determine if it forces the guard
    into a loop
    """
    map = LabMap(path)
    start = map.guard
    visited = map.walk_guard()
    assert isinstance(visited, set)
    visited.remove(start)

    partial_test = partial(test_new_obstacle, path=path)

    num_loops = 0
    with ProcessPoolExecutor() as executor:
        for res in executor.map(partial_test, visited):
            if not isinstance(res, set):
                num_loops += 1

    return num_loops


if __name__ == "__main__":
    path = "inputs/day06"

    map = LabMap(path)

    visited_tiles = map.walk_guard()
    assert isinstance(visited_tiles, set)
    print("Number of distinct positions visited:", len(visited_tiles))

    num_loops = introduce_obstacles(path)
    print("Number of positions we can place an obstacle:", num_loops)
