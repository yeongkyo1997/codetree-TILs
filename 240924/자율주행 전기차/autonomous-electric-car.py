import collections
import math
import sys

# sys.stdin = open('자율주행 전기차', 'r')


def find_start():
    global C, cx, cy
    q = collections.deque()
    q.append((cx, cy, 0))
    visited = [[False] * N for _ in range(N)]
    visited[cx][cy] = True
    candi = []

    while q:
        x, y, depth = q.popleft()
        if (x, y) in starts and (x, y) not in starts_set:
            candi.append((depth, x, y, (x, y, depth)))

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny] and board[nx][ny] == 0:
                visited[nx][ny] = True

                q.append((nx, ny, depth + 1))
    candi.sort()
    x, y, dist = candi[0][-1]
    idx = starts_lib[x, y]
    starts_set.add((x, y))
    cx, cy = x, y
    C -= dist
    if C < 0:
        return -1
    return idx


# 목적지 찾기
def find_end(idx):
    global C, cx, cy
    q = collections.deque()
    q.append((cx, cy, 0))
    visited = [[False] * N for _ in range(N)]
    visited[cx][cy] = True

    while q:
        x, y, depth = q.popleft()
        if (x, y) == ends[idx]:
            C -= depth
            if C < 0:
                return -1
            C += depth * 2
            cx, cy = x, y
            return depth
        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and board[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny, depth + 1))


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    N, M, C = map(int, input().split())

    board = [list(map(int, input().split())) for _ in range(N)]
    cx, cy = map(lambda x: int(x) - 1, input().split())
    starts = []
    starts_lib = {}
    starts_set = set()
    ends = []
    for idx in range(M):
        sx, sy, ex, ey = map(lambda x: int(x) - 1, input().split())
        starts.append((sx, sy))
        starts_lib[sx, sy] = idx
        ends.append((ex, ey))

    for _ in range(M):
        idx = find_start()
        if idx == -1:
            C = -1
            break
        if find_end(idx) == -1:
            C = -1
            break

    print(C)