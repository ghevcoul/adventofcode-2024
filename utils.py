from dataclasses import dataclass


@dataclass(frozen=True)
class XYCoord:
    x: int
    y: int

    def __add__(self, other: "XYCoord") -> "XYCoord":
        new_x = self.x + other.x
        new_y = self.y + other.y
        return XYCoord(new_x, new_y)

    def __sub__(self, other: "XYCoord") -> "XYCoord":
        new_x = self.x - other.x
        new_y = self.y - other.y
        return XYCoord(new_x, new_y)


class BoundedGrid:
    def __init__(self, max_x: int, max_y: int):
        self.max_x = max_x
        self.max_y = max_y

    def _within_bounds(self, pos: XYCoord) -> bool:
        """
        Checks whether the provided XYCoord is within the bounds of the grid
        """
        x_in = 0 <= pos.x <= self.max_x
        y_in = 0 <= pos.y <= self.max_y
        return x_in and y_in
