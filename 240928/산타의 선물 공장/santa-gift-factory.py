import sys



def main():

    input = sys.stdin.read().split()
    idx = 0

    q = int(input[idx])
    idx += 1

    class Node:
        def __init__(self, ID, W):
            self.ID = ID
            self.W = W
            self.prev = None
            self.next = None

    class Belt:
        def __init__(self):
            self.head = None
            self.tail = None

        def append(self, node):
            if self.tail is None:
                self.head = self.tail = node
                node.prev = node.next = None
            else:
                self.tail.next = node
                node.prev = self.tail
                node.next = None
                self.tail = node

        def remove_head(self):
            if self.head is None:
                return None
            node = self.head
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None
            node.next = node.prev = None
            return node

        def move_head_to_tail(self):
            if self.head is None or self.head == self.tail:
                return
            node = self.head
            self.head = node.next
            self.head.prev = None
            self.tail.next = node
            node.prev = self.tail
            node.next = None
            self.tail = node

        def remove_node(self, node):
            if node.prev is None:
                # node is head
                self.head = node.next
            else:
                node.prev.next = node.next
            if node.next is None:
                # node is tail
                self.tail = node.prev
            else:
                node.next.prev = node.prev
            node.prev = node.next = None

        def insert_front_sublist(self, sub_head, sub_tail):
            if self.head is None:
                self.head = sub_head
                self.tail = sub_tail
                sub_head.prev = None
                sub_tail.next = None
            else:
                sub_tail.next = self.head
                self.head.prev = sub_tail
                self.head = sub_head
                sub_head.prev = None

    belts = []
    mapping = dict()
    broken_belts = set()
    m = 0

    result = []

    for _ in range(q):
        if idx >= len(input):
            break
        cmd = int(input[idx])
        idx += 1
        if cmd == 100:
            n = int(input[idx])
            m = int(input[idx + 1])
            idx += 2
            ids = list(map(int, input[idx:idx + n]))
            idx += n
            weights = list(map(int, input[idx:idx + n]))
            idx += n
            belts = [Belt() for _ in range(m + 1)]  # 1-based indexing
            items_per_belt = n // m
            for i in range(n):
                belt_num = (i // items_per_belt) + 1
                node = Node(ids[i], weights[i])
                belts[belt_num].append(node)
                mapping[ids[i]] = (belt_num, node)
            initialized = True
        elif cmd == 200:
            # Unload
            if idx >= len(input):
                w_max = 0
            else:
                w_max = int(input[idx])
                idx += 1
            total = 0
            for belt_num in range(1, m + 1):
                if belt_num in broken_belts:
                    continue
                belt = belts[belt_num]
                if belt.head is None:
                    continue
                node = belt.head
                if node.W <= w_max:
                    total += node.W
                    belt.remove_head()
                    del mapping[node.ID]
                else:
                    belt.move_head_to_tail()
            result.append(str(total))
        elif cmd == 300:
            # Remove
            if idx >= len(input):
                r_id = -1
            else:
                r_id = int(input[idx])
                idx += 1
            if r_id in mapping:
                belt_num, node = mapping[r_id]
                if belt_num in broken_belts:
                    result.append("-1")
                else:
                    belts[belt_num].remove_node(node)
                    del mapping[r_id]
                    result.append(str(r_id))
            else:
                result.append("-1")
        elif cmd == 400:
            # Find and rearrange
            if idx >= len(input):
                f_id = -1
            else:
                f_id = int(input[idx])
                idx += 1
            if f_id in mapping:
                belt_num, node = mapping[f_id]
                if belt_num in broken_belts:
                    result.append("-1")
                    continue
                result.append(str(belt_num))
                belt = belts[belt_num]
                if node.next is not None:
                    sub_head = node.next
                    sub_tail = belt.tail
                    belt.tail = node
                    node.next = None
                    sub_head.prev = None
                    sub_tail.next = belt.head
                    if belt.head is not None:
                        belt.head.prev = sub_tail
                    belt.head = sub_head
            else:
                result.append("-1")
        elif cmd == 500:
            if idx >= len(input):
                b_num = -1
            else:
                b_num = int(input[idx])
                idx += 1
            if b_num in broken_belts:
                result.append("-1")
            else:
                broken_belts.add(b_num)
                belt = belts[b_num]
                target_belt_num = -1
                for i in range(1, m + 1):
                    j = (b_num + i) if (b_num + i) <= m else (b_num + i - m)
                    if j not in broken_belts:
                        target_belt_num = j
                        break
                if belt.head is not None:
                    target_belt = belts[target_belt_num]
                    cur = belt.head
                    while cur is not None:
                        next_node = cur.next
                        target_belt.append(cur)
                        mapping[cur.ID] = (target_belt_num, cur)
                        cur = next_node
                    belt.head = belt.tail = None
                result.append(str(b_num))
        else:
            pass

    print('\n'.join(result))


if __name__ == "__main__":
    main()