import collections
import sys


# 공격자 선정
def find():
    candi = []
    for i in range(N):
        for j in range(M):
            if board[i][j] != 0:
                candi.append((board[i][j], -attack_time[i][j], -(i + j), j, (i, j)))

    candi.sort()
    sx, sy = candi[0][-1]
    ex, ey = candi[-1][-1]



    return sx, sy, ex, ey


def attack(sx, sy, ex, ey, path):
    # 가장 강한 포탑 공격
    board[ex][ey] -= board[sx][sy]

    if board[ex][ey] < 0:
        board[ex][ey] = 0
    for px, py in path:
        attacked[px][py] = True
        if (sx, sy) == (px, py) or (ex, ey) == (px, py):
            continue
        board[px][py] -= board[sx][sy] // 2

        if board[px][py] < 0:
            board[px][py] = 0


# 레이저 공격
def lazer(sx, sy, ex, ey):
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    prev = [[None for _ in range(M)] for _ in range(N)]
    q = collections.deque()
    q.append((sx, sy))
    visited = [[False] * M for _ in range(N)]
    visited[sx][sy] = True

    while q:
        x, y = q.popleft()
        if (x, y) == (ex, ey):
            path = []

            while (x, y) != (sx, sy):
                path.append((x, y))
                x, y = prev[x][y]
            attack(sx, sy, ex, ey, path)
            return True

        for dx, dy in dir:
            nx, ny = (x + dx) % N, (y + dy) % M

            if not visited[nx][ny] and board[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
                prev[nx][ny] = (x, y)
    return False


# 폭탄공격
def bomb(sx, sy, ex, ey):
    dir = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    candi = []
    attacked[sx][sy] = True
    attacked[ex][ey] = True
    for dx, dy in dir:
        nx, ny = (ex + dx) % N, (ey + dy) % M

        if board[nx][ny]:
            attacked[nx][ny] = True
            candi.append((nx, ny))
    attack(sx, sy, ex, ey, candi)


# 고치기
def fix(sx, sy, ex, ey):
    for i in range(N):
        for j in range(M):
            if (sx, sy) == (i, j) or (ex, ey) == (i, j):
                continue
            if not attacked[i][j] and board[i][j]:
                board[i][j] += 1


if __name__ == '__main__':
    N, M, K = map(int, input().split())

    board = [list(map(int, input().split())) for _ in range(N)]
    attack_time = [[0] * M for _ in range(N)]
    for i in range(1, K + 1):
        attacked = [[False] * M for _ in range(N)]
        sx, sy, ex, ey = find()
        if (sx, sy) == (ex, ey):
            break
        # 공격자 공격력 올리기
        board[sx][sy] += N + M
        # 공격자 공격시간
        attack_time[sx][sy] = i
        if not lazer(sx, sy, ex, ey):
            bomb(sx, sy, ex, ey)
        fix(sx, sy, ex, ey)

    result = max(max(b) for b in board)
    print(result)