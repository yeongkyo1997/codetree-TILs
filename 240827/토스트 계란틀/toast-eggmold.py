import collections
import math


def merge_egg(board, path):
    total = 0
    for x, y in path:
        total += board[x][y]

    total = math.floor(total / len(path))

    for x, y in path:
        board[x][y] = total


def bfs(board, x, y):
    q = collections.deque()
    path = set()
    q.append((x, y))
    path.add((x, y))
    visited[x][y] = True
    flag = False

    while q:
        x, y = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                if L <= abs(board[x][y] - board[nx][ny]) <= R:
                    flag = True
                    path.add((nx, ny))
                    visited[nx][ny] = True
                    q.append((nx, ny))
    merge_egg(board, path)

    return flag


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    n, L, R = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]

    result = 0
    while True:
        visited = [[False] * n for _ in range(n)]
        flag = False
        for i in range(n):
            for j in range(n):
                if not visited[i][j]:
                    if bfs(board, i, j):
                        flag = True
        if not flag:
            break
        result += 1

    print(result)