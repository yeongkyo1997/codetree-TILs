import collections
import heapq
import math
import sys

input = lambda: sys.stdin.readline().rstrip()


def dijkstra(start):
    dist[start] = 0
    heap = []
    heapq.heappush(heap, (dist[start], start))

    while heap:
        w, x = heapq.heappop(heap)

        if dist[x] < w:
            continue

        for v, nw in graph[x]:
            if dist[v] > w + nw:
                dist[v] = w + nw
                heapq.heappush(heap, (dist[v], v))


if __name__ == '__main__':
    Q = int(input())
    start = 0
    dist = collections.defaultdict(lambda: math.inf)
    items = collections.defaultdict(tuple)
    ban = set()
    for _ in range(Q):
        query, *data = list(map(int, input().split()))
        if query == 100:
            n, m, *data = data
            tmp = collections.defaultdict(lambda: collections.defaultdict(lambda: math.inf))
            for i in range(m):
                a, b, cost = data[i * 3:i * 3 + 3]
                tmp[a][b] = min(tmp[a][b], cost)
                tmp[b][a] = min(tmp[b][a], cost)
            graph = collections.defaultdict(list)
            for s in tmp:
                graph[s].extend(tmp[s].items())
            dijkstra(start)
        elif query == 200:
            idx, revenue, dest = data
            items[idx] = (revenue, dest)
            ban.discard(idx)
        elif query == 300:
            idx = data[0]
            if idx in items:
                ban.add(idx)
        elif query == 400:
            candi = []
            for idx, (revenue, dest) in items.items():
                if idx in ban:
                    continue
                if revenue - dist[dest] < 0:
                    continue
                candi.append((-(revenue - dist[dest]), idx, (revenue - dist[dest], idx)))
            if candi:
                candi.sort()
            else:
                print(-1)
                continue
            profit, idx = candi[0][-1]
            print(idx)
            ban.add(idx)
        else:
            s = data[0]
            start = s
            dist = collections.defaultdict(lambda: math.inf)
            dijkstra(start)