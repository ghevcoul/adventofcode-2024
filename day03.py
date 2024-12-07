import re
import sys


MUL_PATTERN = re.compile(r"mul\(\d+,\d+\)")
DO_PATTERN = re.compile(r"do\(\)")
DONT_PATTERN = re.compile(r"don't\(\)")


def compute_muls(muls: list[str]) -> int:
    """
    Parse each "mul(x,y)" command into integers and perform the multiplication
    sum the result of all the mul commands and return it
    """
    executed = []
    for mul in muls:
        val1, val2 = mul[4:-1].split(",")
        executed.append(int(val1) * int(val2))

    return sum(executed)


def part1(path: str):
    muls = []
    with open(path, "r") as fp:
        for line in fp.readlines():
            muls.extend(re.findall(MUL_PATTERN, line))

    print("Total added results:", compute_muls(muls))


def parse_line(line: str, enabled: bool) -> tuple[list[str], bool]:
    """
    Parse a line of the program, returning all enabled mul(x,y) strings and the current enabled state
    A "don't()" in the program disables all mul()s until the next "do()" re-enables them
    """
    muls = []
    index = 0
    while index < len(line):
        if enabled:
            # search for either the next mul or dont
            mul_loc = MUL_PATTERN.search(line, pos=index)
            dont_loc = DONT_PATTERN.search(line, pos=index)

            # if neither were found, we're at the end of the string
            if not mul_loc and not dont_loc:
                index = len(line)
                break

            # extract the start positions of both Matches
            # if one match wasn't found, set to big value for comparison purposes
            mul_start = mul_loc.start() if mul_loc else sys.maxsize
            dont_start = dont_loc.start() if dont_loc else sys.maxsize
            if mul_start < dont_start:
                muls.append(mul_loc.group())
                index = mul_loc.end()
            else:
                enabled = False
                index = dont_loc.end()
        else:
            # search only for the next do
            do_loc = DO_PATTERN.search(line, pos=index)

            # if it wasn't found, we're at the end of the string
            if not do_loc:
                break

            enabled = True
            index = do_loc.end()

    return muls, enabled


def part2(path: str):
    muls = []

    enabled = True
    with open(path, "r") as fp:
        for line in fp.readlines():
            found_muls, enabled = parse_line(line, enabled)
            muls.extend(found_muls)

    print("Sum of all enabled muls:", compute_muls(muls))


def main(path: str):
    part1(path)
    part2(path)


if __name__ == "__main__":
    path = "inputs/day03"
    main(path)
