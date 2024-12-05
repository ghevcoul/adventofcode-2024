from typing import Generator


def read_data(input_path: str) -> Generator[tuple[int, ...]]:
    """
    Load a data file expected to be lines containing one or more ints
    Yield each line as a tuple of ints
    """
    with open(input_path, "r") as fp:
        for line in fp.readlines():
            yield tuple(int(v) for v in line.split())


def is_pos(val: int) -> bool:
    return val > 0


def is_neg(val: int) -> bool:
    return val < 0


def in_range(val: int) -> bool:
    return abs(val) in (1, 2, 3)


def is_safe(report: tuple[int, ...]) -> bool:
    """
    Takes a tuple of integers representing a generator report and determine if it's safe
    Safety is defined as:
    - The levels are either all increasing or all decreasing
    - All changes are 1, 2, or 3
    """
    changes = []
    for i in range(len(report) - 1):
        changes.append(report[i + 1] - report[i])

    # If all the changes are positive or negative, check the change range
    if all(map(is_pos, changes)) or all(map(is_neg, changes)):
        return all(map(in_range, changes))

    return False


def main(input_path: str):
    num_safe = 0
    for report in read_data(input_path):
        if is_safe(report):
            num_safe += 1

    print("Number of safe reports:", num_safe)


if __name__ == "__main__":
    input_path = "inputs/day02"
    main(input_path)
