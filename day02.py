from typing import Generator, Iterable


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


def is_safe(report: Iterable[int]) -> bool:
    """
    Takes an iterable of integers representing a generator report and determine if it's safe
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


def run_part1(input_path: str):
    num_safe = 0
    for report in read_data(input_path):
        if is_safe(report):
            num_safe += 1

    print("Number of safe reports:", num_safe)


def run_part2(input_path: str):
    num_safe = 0
    for report in read_data(input_path):
        if is_safe(report):
            num_safe += 1
            continue

        # Remove one element at a time from report
        # and check if the remainder is safe
        for i in range(len(report)):
            tmp_report = list(report)
            tmp_report.pop(i)
            if is_safe(tmp_report):
                num_safe += 1
                break

    print("Number of safe reports with Problem Dampener:", num_safe)


def main(input_path: str):
    run_part1(input_path)
    run_part2(input_path)


if __name__ == "__main__":
    input_path = "inputs/day02"
    main(input_path)
