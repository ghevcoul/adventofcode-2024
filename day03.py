import re


PATTERN = re.compile(r"mul\(\d+,\d+\)")


def main(path: str):
    muls = []
    with open(path, "r") as fp:
        for line in fp.readlines():
            muls.extend(re.findall(PATTERN, line))

    executed = []
    for mul in muls:
        val1, val2 = mul[4:-1].split(",")
        executed.append(int(val1) * int(val2))

    print("Total added results:", sum(executed))


if __name__ == "__main__":
    path = "inputs/day03"
    main(path)
