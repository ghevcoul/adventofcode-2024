import string


class HardDrive:
    def __init__(self, disk_map: str):
        self.disk_map = disk_map
        self._disk_map_to_block_map()

    def _disk_map_to_block_map(self):
        """
        Reads a disk map dense format and converts it into a block map format
        In the block map a number indicates a file ID and a period indicates an empty block
        disk map 12345 -> block map 0..111....22222
        """
        block_map = []
        current_id = 0

        for i, digit in enumerate(self.disk_map):
            digit = int(digit)

            # If odd, this represents free space
            if i % 2:
                block_map.extend(["."] * digit)
            else:
                # Even represents a file
                block_map.extend([current_id] * digit)
                current_id += 1

        self.block_map = block_map

    def defrag_disk(self, verbose: bool = False):
        """
        Defragments the disk by moving blocks from the right to empty spaces on the left
        e.g.
        0..111....22222
        02.111....2222.
        022111....222..
        0221112...22...
        """
        if verbose:
            print(self.block_map)

        # Initialize two pointers at the left and right ends of the map
        left = self.next_empty(0)
        right = self.last_used(len(self.block_map) - 1)
        while left < right:
            # Copy the value of right into left
            # Then set right to empty
            self.block_map[left] = self.block_map[right]
            self.block_map[right] = "."

            # Update the pointers before the next iteration
            left = self.next_empty(left)
            right = self.last_used(right)

            if verbose:
                print(self.block_map)

    def next_empty(self, start: int):
        for i, block in enumerate(self.block_map[start:], start=start):
            if block == ".":
                return i
        raise ValueError(f"No empty blocks found after {start}")

    def last_used(self, start: int):
        for i in range(start, 0, -1):
            if isinstance(self.block_map[i], int):
                return i
        raise ValueError(f"No used blocks found before {start}")

    def _is_compacted(self) -> bool:
        prev_block = self.block_map[0]
        for curr_block in self.block_map[1:]:
            # If previous block is empty and the current block is a file
            # the disk is not currently compacted
            if prev_block == "." and isinstance(curr_block, int):
                return False
            prev_block = curr_block

        # If we've made it to the end without exiting, must be compacted
        return True

    @property
    def checksum(self) -> int:
        """
        Compute the checksum of the disk by summing the product of each blocks position and file ID
        """
        checksum = 0

        for pos, block in enumerate(self.block_map):
            try:
                checksum += pos * int(block)
            except ValueError:
                continue

        return checksum


if __name__ == "__main__":
    # disk = "2333133121414131402"

    with open("inputs/day09", "r") as fp:
        disk = fp.readline().strip()

    drive = HardDrive(disk)
    drive.defrag_disk()
    print("After compaction, disk checksum is", drive.checksum)
