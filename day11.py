import math
from functools import cache


BLINKS = 75


@cache
def blink_stone(stone: int, iteration: int) -> int:
    """
    Recursive function that stops when iteration == BLINKS

    At each call, updates the stone and then calls itself with the new value
    - stone == 0 -> 1
    - num_digits(stone) is event -> split digits in half, truncate leading 0
    - otherwise -> stone * 2024
    """
    if iteration == BLINKS:
        return 1

    if stone == 0:
        return blink_stone(1, iteration + 1)

    # Order of magnitude will be one less than the number of digits
    # such that (10 ** oom) has the same number of digits as the input number
    num_digits = math.floor(math.log10(stone)) + 1
    if num_digits % 2 == 0:
        midpoint_magnitude = 10 ** (num_digits // 2)
        a = stone // midpoint_magnitude
        b = stone % midpoint_magnitude
        return blink_stone(a, iteration + 1) + blink_stone(b, iteration + 1)

    return blink_stone(stone * 2024, iteration + 1)


def main(stones: list[int]):
    num_stones = 0

    for stone in stones:
        num_stones += blink_stone(stone, 0)

    print(num_stones)


if __name__ == "__main__":
    example = [125, 17]
    puzzle_input = [965842, 9159, 3372473, 311, 0, 6, 86213, 48]

    main(puzzle_input)
