from dataclasses import dataclass
from functools import partial
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


def concatenate(a: int, b: int) -> int:
    """
    Takes two integers and concatenates their digits to create a new integer
    e.g. concatenate(5, 6) -> 56, concatenate(17, 45) -> 1745
    """
    return int(str(a) + str(b))


def is_valid_equation(equation: Equation, with_concat: bool = False) -> bool:
    """
    Determine if this equation can be made valid by inserting addition, multiplication,
    or concatenation operators between the values
    """
    operators = [add, mul]
    if with_concat:
        operators.append(concatenate)
    for operator_perm in product(operators, repeat=len(equation.values) - 1):
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

    valid_concat = partial(is_valid_equation, with_concat=True)
    valid_eqs = filter(valid_concat, equations)
    summed_results = sum(eq.result for eq in valid_eqs)
    print("Total calibration results with concatenation:", summed_results)


if __name__ == "__main__":
    path = "inputs/day07"
    main(path)
