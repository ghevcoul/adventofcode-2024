from collections import defaultdict
from functools import cmp_to_key
from typing import Iterable


class Rules:
    def __init__(self, rules: Iterable[tuple[int, int]]):
        # Store the rules as a dict, keyed on first page num
        # Value will be set of all page nums that must appear after it
        self.rules = defaultdict(set)
        for before, after in rules:
            self.rules[before].add(after)

    def check_update(self, update: Iterable[int]) -> bool:
        """
        Check if this update violates any rules, returns False if it does
        - Iterates through the list of updates
        - Fetches rules for that page number
        - Checks if any of the prior looked at page numbers are in the list of "after" pages
        """
        prior = set()
        for page in update:
            after = self.rules[page]
            # If the intersection of after and prior has any elements in it
            # This is a rule violation
            if after & prior:
                return False
            prior.add(page)

        return True

    def fix_update(self, update: Iterable[int]) -> list[int]:
        """
        Takes an update that is incorrectly ordered and sorts it into the correct order
        If given a correctly ordered update, should return the same list unchanged
        """
        return sorted(update, key=cmp_to_key(self.compare_pages))

    def compare_pages(self, left: int, right: int) -> bool:
        """
        Compares two page numbers returning True if left should come before right (i.e. left < right)
        left < right if right exists in left's rules

        If they share no rules, will also return True, to ensure a stable sort
        """
        if right in self.rules[left]:
            return -1
        elif left in self.rules[right]:
            return 1
        else:
            return 0


def parse_input(path: str):
    rules = []
    updates = []
    with open(path, "r") as fp:
        in_rules = True
        for line in fp.readlines():
            # The rules and updates are separated by a blank line
            if line == "\n":
                in_rules = False
                continue

            if in_rules:
                left, right = line.strip().split("|")
                rules.append((int(left), int(right)))
            else:
                int_update = [int(x) for x in line.strip().split(",")]
                updates.append(int_update)

    return updates, Rules(rules)


def main(path: str):
    updates, rules = parse_input(path)

    correct_updates = []
    incorrect_updates = []
    for update in updates:
        if rules.check_update(update):
            correct_updates.append(update)
        else:
            incorrect_updates.append(update)

    middles = sum(update[len(update) // 2] for update in correct_updates)
    print("Sum of the middle value of all correct updates:", middles)

    fixed_updates = [rules.fix_update(update) for update in incorrect_updates]
    middles = sum(update[len(update) // 2] for update in fixed_updates)
    print("Sum of the middle value of all fixed updates:", middles)


if __name__ == "__main__":
    path = "inputs/day05"
    main(path)
