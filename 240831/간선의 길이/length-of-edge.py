import sys
import collections
import heapq
import math


def dijkstra(graph, start, N):
    dist = [math.inf] * (N + 1)
    dist[start] = 0
    heap = []
    heapq.heappush(heap, (0, start))

    while heap:
        depth, x = heapq.heappop(heap)

        if dist[x] < depth:
            continue

        for e, d in graph[x]:
            w = dist[x] + d

            if dist[e] > w:
                dist[e] = w
                heapq.heappush(heap, (dist[e], e))

    return dist


def dijkstra_with_modified_edge(graph, start, N, mod_edge):
    dist = [math.inf] * (N + 1)
    dist[start] = 0
    heap = []
    heapq.heappush(heap, (0, start))

    while heap:
        depth, x = heapq.heappop(heap)

        if dist[x] < depth:
            continue

        for e, d in graph[x]:
            if (x, e) == mod_edge or (e, x) == mod_edge:
                d *= 2  # 선택된 간선의 길이를 2배로 늘림

            w = dist[x] + d

            if dist[e] > w:
                dist[e] = w
                heapq.heappush(heap, (dist[e], e))

    return dist


def find_max_difference():
    original_dist = dijkstra(graph, 1, N)
    shortest_length = original_dist[N]

    max_dist = -math.inf
    for u, v, d in edges:
        modified_dist = dijkstra_with_modified_edge(graph, 1, N, (u, v))
        new_length = modified_dist[N]
        max_dist = max(max_dist, new_length)

    ret = max_dist - shortest_length
    return ret


if __name__ == '__main__':
    N, M = map(int, input().split())
    graph = collections.defaultdict(list)
    edges = []
    for i in range(1, M + 1):
        u, v, d = map(int, input().split())
        graph[u].append((v, d))
        graph[v].append((u, d))
        edges.append((u, v, d))
    result = find_max_difference()
    print(result)