from collections import deque


def bfs(n, board, robot_pos, robot_level):
    q = deque([(robot_pos[0], robot_pos[1], 0)])
    visited = [[False] * n for _ in range(n)]
    visited[robot_pos[0]][robot_pos[1]] = True

    while q:
        x, y, dist = q.popleft()

        if 0 < board[x][y] < robot_level:
            return (x, y, dist)

        for dx, dy in dir:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and board[nx][ny] <= robot_level:
                visited[nx][ny] = True
                q.append((nx, ny, dist + 1))

    return None


def solve(n, board):
    pos = None
    for i in range(n):
        for j in range(n):
            if board[i][j] == 9:
                pos = (i, j)
                board[i][j] = 0
                break
        if pos:
            break

    level = 2
    exp = 0
    time = 0

    while True:
        target = bfs(n, board, pos, level)
        if not target:
            break

        x, y, dist = target
        time += dist
        exp += 1
        board[x][y] = 0
        pos = (x, y)

        if exp == level:
            level += 1
            exp = 0

    return time


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(n)]

    print(solve(n, board))