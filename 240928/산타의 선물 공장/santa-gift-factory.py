import sys




def main():
    class Node:
        def __init__(self, gift_id, weight):
            self.id = gift_id
            self.weight = weight
            self.prev = None
            self.next = None
            self.belt = None

    class Belt:
        def __init__(self):
            self.head = None
            self.tail = None
            self.broken = False

    q = int(sys.stdin.readline())
    commands = []

    for _ in range(q):
        line = sys.stdin.readline().strip()
        commands.append(line)

    id_to_node = {}
    belts = []
    m = 0  # Number of belts

    for idx, command in enumerate(commands):
        tokens = command.strip().split()
        cmd = int(tokens[0])

        if cmd == 100:
            # Factory establishment
            n = int(tokens[1])
            m = int(tokens[2])
            IDs = list(map(int, tokens[3:3 + n]))
            Ws = list(map(int, tokens[3 + n:]))
            belts = [Belt() for _ in range(m)]
            per_belt = n // m
            idx_id = 0

            for i in range(m):
                belt = belts[i]
                for _ in range(per_belt):
                    gift_id = IDs[idx_id]
                    weight = Ws[idx_id]
                    node = Node(gift_id, weight)
                    node.belt = i
                    id_to_node[gift_id] = node

                    if belt.head is None:
                        belt.head = belt.tail = node
                    else:
                        belt.tail.next = node
                        node.prev = belt.tail
                        belt.tail = node
                    idx_id += 1
            # No output for this command

        elif cmd == 200:
            # Unload gifts
            w_max = int(tokens[1])
            total_weight = 0
            for i in range(m):
                belt = belts[i]
                if belt.broken or belt.head is None:
                    continue
                node = belt.head
                if node.weight <= w_max:
                    # Unload the gift
                    total_weight += node.weight
                    belt.head = node.next
                    if belt.head:
                        belt.head.prev = None
                    else:
                        belt.tail = None  # Belt is now empty
                    del id_to_node[node.id]
                else:
                    # Move the gift to the back
                    if belt.head == belt.tail:
                        continue  # Only one gift
                    belt.head = node.next
                    belt.head.prev = None
                    belt.tail.next = node
                    node.prev = belt.tail
                    node.next = None
                    belt.tail = node
            print(total_weight)

        elif cmd == 300:
            # Remove gift
            r_id = int(tokens[1])
            node = id_to_node.get(r_id)
            if node:
                belt = belts[node.belt]
                if node.prev:
                    node.prev.next = node.next
                else:
                    belt.head = node.next
                if node.next:
                    node.next.prev = node.prev
                else:
                    belt.tail = node.prev
                del id_to_node[r_id]
                print(r_id)
            else:
                print(-1)

        elif cmd == 400:
            # Check gift
            f_id = int(tokens[1])
            node = id_to_node.get(f_id)
            if node:
                belt_num = node.belt + 1  # 1-based indexing
                print(belt_num)
                belt = belts[node.belt]
                if node == belt.head:
                    continue  # Already at front
                # Detach segment from node to tail
                if node.prev:
                    node.prev.next = None
                    belt.tail = node.prev
                    node.prev = None
                # Attach to front
                node_tail = node
                while node_tail.next:
                    node_tail = node_tail.next
                node_tail.next = belt.head
                if belt.head:
                    belt.head.prev = node_tail
                belt.head = node
            else:
                print(-1)

        elif cmd == 500:
            # Belt failure
            b_num = int(tokens[1]) - 1  # 0-based indexing
            belt = belts[b_num]
            if belt.broken:
                print(-1)
            else:
                belt.broken = True
                print(b_num + 1)
                # Find next available belt
                target_belt = None
                for i in range(1, m + 1):
                    idx = (b_num + i) % m
                    if not belts[idx].broken:
                        target_belt = belts[idx]
                        break
                if belt.head is None:
                    continue  # No gifts to move
                # Move gifts from belt to target_belt from tail to head
                # Reverse the belt
                current = belt.head
                prev = None
                while current:
                    next_node = current.next
                    current.next = prev
                    current.prev = next_node
                    prev = current
                    current = next_node
                belt.head, belt.tail = belt.tail, belt.head
                if target_belt.head is None:
                    target_belt.head = belt.head
                    target_belt.tail = belt.tail
                else:
                    target_belt.tail.next = belt.head
                    belt.head.prev = target_belt.tail
                    target_belt.tail = belt.tail
                current = belt.head
                while current:
                    current.belt = target_belt.broken and b_num or idx
                    current = current.next
                belt.head = belt.tail = None


if __name__ == '__main__':
    main()