import collections
import sys


# 공격자 및 공격받을 포탑 선정
def find():
    turrets = []
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                continue
            turrets.append((board[i][j], -time[i][j], -(i + j), -j, (i, j)))
    turrets.sort()
    return turrets


# 레이저 공격
def lazer(sx, sy, ex, ey):
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    q = collections.deque()
    prev = [[None for _ in range(N)] for _ in range(N)]
    visited = [[False] * N for _ in range(N)]
    q.append((sx, sy))
    visited[sx][sy] = True

    while q:
        x, y = q.popleft()
        if (x, y) == (ex, ey):
            path = []
            while (x, y) != (sx, sy):
                path.append((x, y))
                x, y = prev[x][y]
            path.reverse()
            return path

        for dx, dy in dir:
            nx, ny = (x + dx) % N, (y + dy) % N
            if board[nx][ny] != 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                prev[nx][ny] = (x, y)
                q.append((nx, ny))
    return None


# 폭탄 공격
def bomb(sx, sy, ex, ey):
    dir = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    for dx, dy in dir:
        nx, ny = (ex + dx) % N, (ey + dy) % N
        if board[nx][ny] != 0 and (sx, sy) != (nx, ny):
            attacked[nx][ny] = True
            board[nx][ny] -= board[sx][sy] // 2
            board[nx][ny] = max(0, board[nx][ny])


# 포탑 정비
def fix():
    for i in range(N):
        for j in range(N):
            if not attacked[i][j] and board[i][j] != 0:
                board[i][j] += 1


if __name__ == '__main__':
    N, M, K = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    time = [[-1] * N for _ in range(N)]

    for i in range(K):
        turrets = find()
        sx, sy = turrets[0][-1]
        ex, ey = turrets[-1][-1]
        time[sx][sy] = i
        board[sx][sy] += N * 2
        board[ex][ey] -= board[sx][sy]
        path = lazer(sx, sy, ex, ey)
        attacked = [[False] * N for _ in range(N)]
        attacked[sx][sy] = True
        attacked[ex][ey] = True
        if path:
            for px, py in path:
                if (px, py) != (ex, ey) and (px, py) != (sx, sy):
                    board[px][py] -= board[sx][sy] // 2
                    board[px][py] = max(0, board[px][py])
                    attacked[px][py] = True
        else:
            bomb(sx, sy, ex, ey)
        fix()
    result = max(max(b) for b in board)

    print(result)