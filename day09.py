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

    def compact_disk(self, verbose: bool = False):
        """
        Compacts the disk by moving blocks from the right to empty spaces on the left
        e.g.
        0..111....22222
        02.111....2222.
        022111....222..
        0221112...22...
        """
        if verbose:
            print("".join(map(str, self.block_map)))

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
                print("".join(map(str, self.block_map)))

    def defrag_disk(self, verbose: bool = False):
        """
        Compacts the disk without fragmenting by files by keeping files in contiguous blocks
        e.g.
        00...111...2...333.44.5555.6666.777.888899
        0099.111...2...333.44.5555.6666.777.8888..
        0099.1117772...333.44.5555.6666.....8888..
        0099.111777244.333....5555.6666.....8888..
        00992111777.44.333....5555.6666.....8888..
        """
        moved_files = set()
        if verbose:
            print("".join(map(str, self.block_map)))

        start, size = self.last_file(len(self.block_map) - 1)

        while start > 0:
            file_id = self.block_map[start]
            # If we've already moved this file, don't try to again
            if file_id in moved_files:
                start, size = self.last_file(start - 1)
                continue

            print("Moving file ID", file_id)
            try:
                avail_empty = self.find_empty(start, size)
            except IndexError:
                # If we didn't find an approriate empty block
                # set avail_empty to size, which skips the next block
                avail_empty = start

            # Only copy a file into an empty block if it appears before the file
            if avail_empty < start:
                # Copy the file into the empty block
                # Then set the original file location to empty
                self.block_map[avail_empty : avail_empty + size] = [file_id] * size
                self.block_map[start : start + size] = ["."] * size
                moved_files.add(file_id)

            # Find the next file before restarting the loop
            try:
                start, size = self.last_file(start - 1)
            except ValueError:
                # An error is raised if there are no files before start, meaning we've hit the start of the disk
                break

            if verbose:
                print("".join(map(str, self.block_map)))

    def next_empty(self, start: int) -> int:
        """
        Finds the position of the next empty block starting at start
        """
        for i, block in enumerate(self.block_map[start:], start=start):
            if block == ".":
                return i
        raise ValueError(f"No empty blocks found after {start}")

    def last_used(self, start: int) -> int:
        """
        Finds the position of the last used block starting at start and working backwards
        """
        for i in range(start, 0, -1):
            if isinstance(self.block_map[i], int):
                return i
        raise ValueError(f"No used blocks found before {start}")

    def last_file(self, start: int) -> tuple[int, int]:
        """
        Finds the position of the last file starting at start and working backwards
        returns the start position of the file and the size of the file
        """
        file_end = self.last_used(start)
        file_start = file_end
        file_size = 1
        file_id = self.block_map[file_end]

        for i in range(file_end - 1, 0, -1):
            if self.block_map[i] == file_id:
                file_start = i
                file_size += 1
            else:
                break

        return file_start, file_size

    def find_empty(self, end: int, size: int) -> int:
        """
        Finds the position of the first contiguous set of empty blocks of at least the given size
        returns the position of the start of the set of empty blocks
        If no block of the appropriate size is found, raises an IndexError
        """
        start = 0
        while start < end:
            # Find the first empty block
            start = self.next_empty(start)
            this_size = 0

            # Walk forward through the block map until hitting a non-empty block
            for i, block in enumerate(self.block_map[start:], start=start):
                if block == ".":
                    this_size += 1
                    if this_size >= size:
                        return start
                else:
                    start = i
                    break
            else:
                # If the loop terminated on it's own (i.e. without a break) increment start
                start += 1

        # If we've hit the end of the block map without finding what we need, raise an error
        raise IndexError()

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

    # Part 1
    # drive = HardDrive(disk)
    # drive.compact_disk()
    # print("After compaction, disk checksum is", drive.checksum)

    # Part 2
    # TODO: This is very slow, takes about 10 minutes to run on the full problem set,
    #       would be worthwhile to revisit this to speed it up. Maybe create a map
    #       of the first empty block of each size and update it when filling empty blocks
    drive = HardDrive(disk)
    drive.defrag_disk()
    print("After defragmentation, disk checksum is", drive.checksum)
