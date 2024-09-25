import collections
import heapq
import math
import sys
from collections import defaultdict as dd



def dijkstra(start):
    ret = dd(lambda: math.inf)
    heap = []
    ret[start] = 0
    heapq.heappush(heap, (0, start))

    while heap:
        w, x = heapq.heappop(heap)

        if ret[x] < w:
            continue

        for num, nw in graph[x]:
            if ret[num] > nw + w:
                ret[num] = nw + w
                heapq.heappush(heap, (ret[num], num))

    return ret


if __name__ == '__main__':
    Q = int(input())

    dist = dd(lambda: math.inf)
    possible, impossible = [], []
    possible_set, impossible_set = set(), set()
    ban = set()
    start = 0
    for _ in range(Q):
        query, *data = map(int, input().split())

        if query == 100:
            n, m, *data = data
            graph = dd(list)
            arr = dd(lambda: dd(lambda: math.inf))
            for i in range(m):
                v, u, w = data[i * 3:i * 3 + 3]
                arr[v][u] = min(arr[v][u], w)
                arr[u][v] = min(arr[u][v], w)
            graph = dd(list)
            for key in arr:
                graph[key].extend(arr[key].items())
            dist = dijkstra(start)
        elif query == 200:
            idx, revenue, dest = data
            profit = revenue - dist[dest]
            if profit >= 0:
                heapq.heappush(possible, (-profit, idx, revenue, dest))
                possible_set.add(idx)
            else:
                impossible.append((-profit, idx, revenue, dest))
                impossible_set.add(idx)
            ban.discard(idx)
        elif query == 300:
            idx = data[0]
            if idx in possible_set or idx in impossible_set:
                ban.add(idx)
            possible_set.discard(idx)
            impossible_set.discard(idx)
        elif query == 400:
            tmp = []
            while possible:
                profit, idx, revenue, dest = heapq.heappop(possible)
                if idx in ban:
                    continue
                if idx in possible_set:
                    print(idx)
                    ban.add(idx)
                    possible_set.discard(idx)
                    break
                else:
                    tmp.append((profit, idx, revenue, dest))
            else:
                print(-1)
            for t in tmp:
                heapq.heappush(possible, t)
        elif query == 500:
            s = data[0]
            dist = dijkstra(s)
            possible_tmp, impossible_tmp = [], []
            possible_set, impossible_set = set(), set()
            for ele in [possible, impossible]:
                for _, idx, revenue, dest in ele:
                    if idx in ban:
                        continue
                    profit = revenue - dist[dest]
                    if profit >= 0:
                        heapq.heappush(possible_tmp, (-profit, idx, revenue, dest))
                        possible_set.add(idx)
                    else:
                        impossible_tmp.append((-profit, idx, revenue, dest))
                        impossible_set.add(idx)
            possible, impossible = possible_tmp, impossible_tmp