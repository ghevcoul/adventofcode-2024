from utils import BoundedGrid, XYCoord


class TopoMap(BoundedGrid):
    def __init__(self, path: str):
        grid = []

        with open(path, "r") as fp:
            for line in fp.readlines():
                grid.append(list(int(char) for char in list(line.strip())))

        max_x = len(grid[0]) - 1
        max_y = len(grid) - 1
        super().__init__(max_x, max_y)

        self.grid = grid

    def find_trailheads(self) -> list[XYCoord]:
        """
        Searches the topo map for the positions of all the trailheads
        """
        trailheads = []

        for y, row in enumerate(self.grid):
            for x, elev in enumerate(row):
                if elev == 0:
                    trailheads.append(XYCoord(x, y))

        return trailheads

    def valid_paths(self, pos: XYCoord) -> list[XYCoord]:
        """
        For the given position, return all adjacent positions that are an
        increase of 1 in elevation
        """
        paths = []

        curr_elev = self.grid[pos.y][pos.x]

        changes = [XYCoord(0, -1), XYCoord(0, 1), XYCoord(-1, 0), XYCoord(1, 0)]

        for change in changes:
            new_pos = pos + change
            if (
                self._within_bounds(new_pos)
                and self.grid[new_pos.y][new_pos.x] == curr_elev + 1
            ):
                paths.append(new_pos)

        return paths

    def compute_trailhead_score(self, trailhead: XYCoord) -> int:
        """
        The trailhead score is the number of peaks you can reach walking from this tailhead
        To reach a peak, you must follow numbers up sequentially either up, down, left, or right
        from the current position

        Uses an iterative depth-first search approach to walk to the paths to a peak
        """
        peaks = set()
        visited = set()
        stack = [trailhead]

        while len(stack) > 0:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                if self.grid[curr.y][curr.x] == 9:
                    peaks.add(curr)
                else:
                    stack.extend(self.valid_paths(curr))

        return len(peaks)

    def compute_trailhead_rating(self, trailhead: XYCoord) -> int:
        """
        The trailhead rating is the number of unique paths you can take following 0 to 9

        This is basically the same algorithm as the trailhead score, but we don't skip visited nodes
        and accumulate reached peaks in a list rather than a set
        """
        peaks = list()
        stack = [trailhead]

        while len(stack) > 0:
            curr = stack.pop()
            if self.grid[curr.y][curr.x] == 9:
                peaks.append(curr)
            else:
                stack.extend(self.valid_paths(curr))

        return len(peaks)

    def part1(self):
        """
        Find all trailheads on the map and calculate the score for each, print the sum off all the scores
        """
        total_score = sum(
            self.compute_trailhead_score(th) for th in self.find_trailheads()
        )

        print("The total score for this map:", total_score)

    def part2(self):
        """
        Find all trailheads on the map and calculate the rating for each
        Print the sum of all the ratings
        """
        total_rating = sum(
            self.compute_trailhead_rating(th) for th in self.find_trailheads()
        )

        print("The total score for this map:", total_rating)


if __name__ == "__main__":
    input_path = "inputs/day10"

    topo = TopoMap(input_path)
    topo.part1()
    topo.part2()
