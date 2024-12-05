from collections import Counter

def calculate_distance(list1: list[int], list2: list[int]) -> None:
    """
    Takes two lists and calculates the pairwise distance between them
    after sorting
    """
    total_dist = sum(abs(v1 - v2) for v1, v2 in zip(sorted(list1), sorted(list2)))
    print("Total distance between lists:", total_dist)


def calculate_similarity(list1: list[int], list2: list[int]) -> None:
    """
    Takes two lists and calculates the similarity between them
    Similarity is defined as:
    For each element in list1, find the number of times it appears in list2
    and multiply its value by the number of appearances
    e.g. if 4 appears 3 times in list2, it's similarity score is 12
    Sum the similarity score for each element
    """
    list2_count = Counter(list2)

    total_similarity = sum(v * list2_count[v] for v in list1)
    print("Total similarity between lists:", total_similarity)


def main(input_data: str):
    list1 = []
    list2 = []
    with open(input_data, 'r') as fp:
        for line in fp.readlines():
            val1, val2 = line.split()
            list1.append(int(val1))
            list2.append(int(val2))

    calculate_distance(list1, list2)
    calculate_similarity(list1, list2)


if __name__ == "__main__":
    input_path = "inputs/day01"
    main(input_path)
