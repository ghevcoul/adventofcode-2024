
def main(input_data: str):
    list1 = []
    list2 = []
    with open(input_data, 'r') as fp:
        for line in fp.readlines():
            val1, val2 = line.split()
            list1.append(int(val1))
            list2.append(int(val2))

    list1.sort()
    list2.sort()

    total_dist = sum(abs(v1 - v2) for v1, v2 in zip(list1, list2))
    print(total_dist)


if __name__ == "__main__":
    input_path = "inputs/day01"
    main(input_path)
    