import collections
import math
import sys

# sys.stdin = open('바이러스 백신', 'r')


def bfs(path):
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    visited = set(path)
    q = collections.deque(map(lambda x: (x[0], x[1], 0), path))
    cnt = 0

    while q:
        x, y, depth = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and board[nx][ny] != -1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                q.append((nx, ny, depth + 1))
                if board[nx][ny] == 0:
                    cnt += 1
                    if cnt == zero_cnt:
                        return depth + 1

    return -1


# 병원 고르기
def dfs(path, depth, start):
    if depth == M:
        return bfs(path)
    ret = math.inf
    for i in range(start, len(hospitals)):
        ret = min(ret, dfs(path + [hospitals[i]], depth + 1, i + 1))
    return ret


if __name__ == '__main__':
    N, M = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    hospitals = []
    zero_cnt = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] == 2:
                hospitals.append((i, j))
            elif board[i][j] == 0:
                zero_cnt += 1
    result = dfs([], 0, 0)
    print(result if result != math.inf else -1)