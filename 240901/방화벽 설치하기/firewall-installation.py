import collections
import copy
import sys

input = lambda: sys.stdin.readline().rstrip()


def bfs(board, wall, zero_cnt):
    q = collections.deque(fire)
    visited = [[False] * m for _ in range(n)]

    for fx, fy in fire:
        visited[fx][fy] = True

    while q:
        x, y = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < m and board[nx][ny] == 0 and not visited[nx][ny] and (nx, ny) not in wall:
                visited[nx][ny] = True
                q.append((nx, ny))
                zero_cnt -= 1

    return zero_cnt - 3


def dfs(wall, depth, start):
    global result
    if depth == 3:
        result = max(result, bfs(board, wall, len(zero)))
        return

    for i in range(start, len(zero)):
        dfs(wall | {(zero[i])}, depth + 1, i + 1)


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    n, m = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    fire = []
    zero = []

    for i in range(n):
        for j in range(m):
            if board[i][j] == 2:
                fire.append((i, j))
            if board[i][j] == 0:
                zero.append((i, j))

    result = 0
    dfs(set(), 0, 0)
    print(result)