import collections
import sys

input = lambda: sys.stdin.readline().rstrip()


def bfs(board, zero_cnt):
    q = collections.deque(fire)
    visited = [[False] * m for _ in range(n)]

    for fx, fy in fire:
        visited[fx][fy] = True

    while q:
        x, y = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < m and board[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
                zero_cnt -= 1

    return zero_cnt


def dfs(path, depth, row, col):
    global result
    if depth == 3:
        tmp = [b[:] for b in board]
        for px, py in path:
            tmp[px][py] = 1
        result = max(result, bfs(tmp, zero_cnt))

        return

    for r in range(row, n):
        for c in range(col, m):
            path.append((r, c))
            if c == m - 1:
                dfs(path, depth + 1, row + 1, 0)
            else:
                dfs(path, depth + 1, row, col + 1)
            path.pop()
        col = 0


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    n, m = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    fire = []
    zero_cnt = -3

    for i in range(n):
        for j in range(m):
            if board[i][j] == 2:
                fire.append((i, j))
            if board[i][j] == 0:
                zero_cnt += 1

    result = 0
    dfs([], 0, 0, 0)
    print(result)