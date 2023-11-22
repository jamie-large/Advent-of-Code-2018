import os

class Node:
    def __init__(self, val: int):
        self.val = val
        self.prev: Node | None = None
        self.next: Node | None = None

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        head = Node(ord(f.read(1)))
        last_node = head
        length = 1
        while True:
            c = f.read(1)
            if not c:
                break
            current = Node(ord(c))
            last_node.next = current
            current.prev = last_node
            last_node = current
            length += 1
        if last_node.prev:
            last_node.prev.next = None
            length -= 1

        current = head

        DIFFERENCE = abs(ord('A') - ord('a'))

        current = head
        while current is not None and current.next is not None:
            if abs(current.val - current.next.val) == DIFFERENCE:
                if current == head:
                    head = current.next.next
                    current = head
                elif current.prev:
                    current.prev.next = current.next.next
                    if current.next.next:
                        current.next.next.prev = current.prev
                    current = current.prev
                length -= 2
            else:
                current = current.next
        return length



def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    with open(fname, "r") as f:
        input_string = f.readline()[:-1]
        DIFFERENCE = abs(ord('A') - ord('a'))

        min_length = len(input_string)

        for skipped_char_ord in range(ord('A'), ord('A') + 26):
            skipped_chars = [chr(skipped_char_ord), chr(skipped_char_ord + DIFFERENCE)]

            i = 0
            while input_string[i] in skipped_chars:
                i += 1
            head = Node(ord(input_string[i]))

            last_node = head
            length = 1
            while i < len(input_string):
                c = input_string[i]
                if c in skipped_chars:
                    i += 1
                    continue
                current = Node(ord(c))
                last_node.next = current
                current.prev = last_node
                last_node = current
                length += 1
                i += 1

            length -= 1

            current = head
            while current is not None and current.next is not None:
                if abs(current.val - current.next.val) == DIFFERENCE:
                    if current == head:
                        head = current.next.next
                        current = head
                    elif current.prev:
                        current.prev.next = current.next.next
                        if current.next.next:
                            current.next.next.prev = current.prev
                        current = current.prev
                    length -= 2
                else:
                    current = current.next
            if length < min_length:
                min_length = length

        return min_length

print(solution_part1())
print(solution_part2())
