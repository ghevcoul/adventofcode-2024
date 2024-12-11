from dataclasses import dataclass
from itertools import product
from operator import add, mul


@dataclass
class Equation:
    result: int
    values: tuple[int, ...]


def load_data(path: str) -> list[Equation]:
    equations = []
    with open(path, "r") as fp:
        for line in fp.readlines():
            result, values_str = line.strip().split(":")
            values = values_str.strip().split(" ")
            values_int = tuple(int(val) for val in values)
            equations.append(Equation(result=int(result), values=values_int))
    return equations


def is_valid_equation(equation: Equation) -> bool:
    """
    Determine if this equation can be made valid by inserting either "+" or "*" between
    the values
    """
    for operator_perm in product([add, mul], repeat=len(equation.values) - 1):
        running_total = equation.values[0]
        for val, operator in zip(equation.values[1:], operator_perm):
            running_total = operator(running_total, val)
        if running_total == equation.result:
            return True
    return False


def main(path: str):
    equations = load_data(path)

    valid_eqs = filter(is_valid_equation, equations)
    summed_results = sum(eq.result for eq in valid_eqs)
    print("Total calibration results:", summed_results)


if __name__ == "__main__":
    path = "inputs/day07"
    main(path)
