from dataclasses import dataclass


@dataclass(frozen=True)
class XYCoord:
    x: int
    y: int

    def __add__(self, other: "XYCoord") -> "XYCoord":
        new_x = self.x + other.x
        new_y = self.y + other.y
        return XYCoord(new_x, new_y)

    def __repr__(self) -> str:
        return f"XYCoord({self.x},{self.y})"


class LabMap:
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
        self.max_x = j
        self.max_y = i

        self.obstacles = obstacles

    def walk_guard(self) -> int:
        """
        Have the guard patrol around the map until it exits the area
        - Will always walk in a straight line until it hits an obstacle
        - When hitting obstacle, will turn 90 degrees (clockwise) and then continue

        Returns the number of unique coordinates the guard visits on their patrol
        """
        visited = set()

        while self._within_bounds():
            # print(self.guard, self.guard_facing)
            visited.add(self.guard)
            self._step_forward()

        return len(visited)

    def _within_bounds(self) -> bool:
        """
        Checks whether the guard is currently within the bounds of the map
        """
        x_in = 0 <= self.guard.x <= self.max_x
        y_in = 0 <= self.guard.y <= self.max_y
        return x_in and y_in

    def _step_forward(self):
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


if __name__ == "__main__":
    path = "inputs/day06"

    map = LabMap(path)

    print("Number of distinct positions visited:", map.walk_guard())
