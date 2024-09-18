import math
import sys

# sys.stdin = open('Main_13460', 'r')


# 움직이고 움직인 횟수 리턴
def move_cnt(x, y, d):
    dx, dy = dir[d]
    nx, ny = x, y
    cnt = 0

    while True:
        nx += dx
        ny += dy

        if board[nx][ny] == '#':
            return x, y, cnt
        if board[nx][ny] == 'O':
            return nx, ny, cnt
        x, y = nx, ny
        cnt += 1


# 10번 dfs
def dfs(rx, ry, bx, by, visited, depth):
    global result
    if depth == 10:
        return
    if (rx, ry, bx, by) in visited:
        return

    # 움직일 방향 선택하기
    for d in range(4):
        # 파란 구슬 움직이기
        nbx, nby, b_cnt = move_cnt(bx, by, d)

        # 파란 구슬이 나간 경우
        if (nbx, nby) == (ox, oy):
            continue

        # 빨간 구슬 움직이기
        nrx, nry, r_cnt = move_cnt(rx, ry, d)

        # 빨간 구슬이 나간 경우
        if (nrx, nry) == (ox, oy):
            result = min(depth + 1, result)
            return

        # 파란 구슬과 빨간 구슬이 위치가 같다면
        if (nrx, nry) == (nbx, nby):
            dx, dy = dir[d]
            # 파란 구슬이 더 많이 움직인 경우
            if b_cnt > r_cnt:
                nbx -= dx
                nby -= dy
            else:  # 빨간 구슬이 더 많이 움직인 경우
                nrx -= dx
                nry -= dy
        dfs(nrx, nry, nbx, nby, visited | {(rx, ry, bx, by)}, depth + 1)


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    N, M = map(int, input().split())

    board = [list(input()) for _ in range(N)]
    rx, ry = -1, -1
    bx, by = -1, -1
    # 출구
    ox, oy = -1, -1
    for i in range(N):
        for j in range(M):
            if board[i][j] == 'B':
                bx, by = i, j
            elif board[i][j] == 'R':
                rx, ry = i, j
            elif board[i][j] == 'O':
                ox, oy = i, j
    result = math.inf
    dfs(rx, ry, bx, by, set(), 0)
    if result == math.inf:
        result = -1
    print(result)