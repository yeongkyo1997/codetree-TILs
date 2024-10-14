import bisect
import sys

input = lambda: sys.stdin.readline().rstrip()


if __name__ == "__main__":
    Q = int(input())
    queries = []
    insert_values = set()
    for _ in range(Q):
        parts = input().split()
        queries.append(parts)
        if parts[0] == 'insert':
            value = int(parts[2])
            insert_values.add(value)

    sorted_values = sorted(insert_values)
    value_to_idx = {v: i + 1 for i, v in enumerate(sorted_values)}
    idx_to_value = sorted_values
    n = len(sorted_values)


    class FenwickTree:
        __slots__ = ['n', 'tree']

        def __init__(self, size):
            self.n = size
            self.tree = [0] * (self.n + 2)

        def add(self, idx, delta):
            while idx <= self.n:
                self.tree[idx] += delta
                idx += idx & -idx

        def sum(self, idx):
            res = 0
            while idx > 0:
                res += self.tree[idx]
                idx -= idx & -idx
            return res

        def reset(self):
            self.tree = [0] * (self.n + 2)

        def find_kth(self, k):
            left = 1
            right = self.n
            res = -1
            while left <= right:
                mid = (left + right) // 2
                s = self.sum(mid)
                if s >= k:
                    res = mid
                    right = mid - 1
                else:
                    left = mid + 1
            return res


    BIT_count = FenwickTree(n)
    BIT_sum = FenwickTree(n)

    name_to_value = {}
    value_to_name = {}
    outputs = []

    for parts in queries:
        if not parts:
            continue
        cmd = parts[0]
        if cmd == 'init':
            name_to_value.clear()
            value_to_name.clear()
            BIT_count.reset()
            BIT_sum.reset()
        elif cmd == 'insert':
            name = parts[1]
            value = int(parts[2])
            if name in name_to_value or value in value_to_name:
                outputs.append('0')
            else:
                name_to_value[name] = value
                value_to_name[value] = name
                idx = value_to_idx[value]
                BIT_count.add(idx, 1)
                BIT_sum.add(idx, value)
                outputs.append('1')
        elif cmd == 'delete':
            name = parts[1]
            if name in name_to_value:
                value = name_to_value.pop(name)
                value_to_name.pop(value)
                idx = value_to_idx[value]
                BIT_count.add(idx, -1)
                BIT_sum.add(idx, -value)
                outputs.append(str(value))
            else:
                outputs.append('0')
        elif cmd == 'rank':
            k = int(parts[1])
            total = BIT_count.sum(n)
            if total < k:
                outputs.append('None')
            else:
                idx = BIT_count.find_kth(k)
                if idx == -1:
                    outputs.append('None')
                else:
                    value = idx_to_value[idx - 1]
                    name = value_to_name[value]
                    outputs.append(name)
        elif cmd == 'sum':
            k = int(parts[1])
            # Find the rightmost index where value <=k
            # bisect_right returns the insertion point, so subtract 1
            pos = bisect.bisect_right(sorted_values, k)
            if pos == 0:
                outputs.append('0')
            else:
                total_sum = BIT_sum.sum(pos)
                outputs.append(str(total_sum))
    print('\n'.join(outputs))