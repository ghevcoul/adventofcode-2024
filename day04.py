class WordSearch:
    def __init__(self, path: str):
        grid = []
        with open(path, "r") as fp:
            for line in fp.readlines():
                grid.append([char for char in line.strip()])

        self.grid = grid

    def find_xmas(self) -> int:
        """
        Find all occurances of XMAS in the grid
        """
        xmas = 0

        # Start from each position in the grid and search
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                xmas += self._match_xmas(i, j)

        return xmas

    def find_x_mas(self) -> int:
        """
        Find all occurances of X-MAS in the grid
        That is, two MAS in the shape of an X
        """
        xmas = 0

        # Start from each position in the grid and search
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                xmas += self._match_x_mas(i, j)

        return xmas

    def _match_xmas(self, xpos: int, ypos: int) -> int:
        """
        From the given starting point, extract itself and the next three letters
        in all 8 possible directions and check if it matches XMAS
        Returns the number of matches starting from this position
        """
        # Fail early if this position isn't an X
        if self.grid[xpos][ypos] != "X":
            return 0

        directions = [
            (0, 1),  # down
            (0, -1),  # up
            (1, 0),  # right
            (-1, 0),  # left
            (1, 1),  # down right
            (1, -1),  # up right
            (-1, 1),  # down left
            (-1, -1),  # up left
        ]

        candidates = [self._extract_4(xpos, ypos, *direc) for direc in directions]
        return candidates.count("XMAS")

    def _match_x_mas(self, xpos: int, ypos: int) -> int:
        """
        From the given starting point, extract the x-shapes and check
        if they're an X-MAS
        """
        # Sort the letters in MAS, makes it easier to check forward and reverse of each arm
        match_string = sorted("MAS")
        # Fail early if this position isn't an A
        if self.grid[xpos][ypos] != "A":
            return 0

        arm1, arm2 = self._extract_x(xpos, ypos)
        if sorted(arm1) == match_string and sorted(arm2) == match_string:
            return 1
        else:
            return 0

    def _extract_x(self, xpos: int, ypos: int) -> tuple[str, str]:
        """
        Extracts the letters in an X around the given position
        e.g. The given letter and the next one at all diagonals around it
        Returns a two-tuple of strings of the extracted letters making up each
        arm of the X
        If the input position is on an edge, return a tuple of empty strings
        """
        arm1 = [(xpos - 1, ypos - 1), (xpos, ypos), (xpos + 1, ypos + 1)]
        arm2 = [(xpos + 1, ypos - 1), (xpos, ypos), (xpos - 1, ypos + 1)]
        if self._out_of_bounds(arm1 + arm2):
            return ("", "")

        return "".join(self.grid[x][y] for x, y in arm1), "".join(
            self.grid[x][y] for x, y in arm2
        )

    def _extract_4(self, xpos: int, ypos: int, xshift: int, yshift: int) -> str:
        """
        Extracts the letter at this position of the grid and the next three letters
        returning them as string
        xshift and yshift should be one of [-1, 0, 1] and define the direction to extract in
        If there are not three letters up (i.e. we hit an edge), return an empty string
        """
        # Determine the indices we need to extract
        indexes = [(xpos + (idx * xshift), ypos + (idx * yshift)) for idx in range(4)]
        # Check if they take us out of bounds
        if self._out_of_bounds(indexes):
            return ""
        return "".join(self.grid[x][y] for x, y in indexes)

    def _out_of_bounds(self, coords: list[tuple[int, int]]) -> bool:
        """
        Checks if the given set of coordinates are all within the grid
        """
        xbound = [0 <= xpos < len(self.grid) for xpos, _ in coords]
        ybound = [0 <= ypos < len(self.grid[0]) for _, ypos in coords]
        return not all(xbound + ybound)


if __name__ == "__main__":
    path = "inputs/day04"

    wordsearch = WordSearch(path)

    print("Occurances of XMAS:", wordsearch.find_xmas())
    print("Occurances of X-MAS:", wordsearch.find_x_mas())
