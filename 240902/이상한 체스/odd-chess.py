import copy
import math
import sys

input = lambda: sys.stdin.readline().rstrip()

N, M = map(int, input().rstrip().split())

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
cctv_dir = [
    [],
    [[0], [1], [2], [3]],
    [[0, 1], [2, 3]],
    [[0, 2], [0, 3], [1, 2], [1, 3]],
    [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]],
    [[0, 1, 2, 3]]
]

board = [list(map(int, input().rstrip().split())) for _ in range(N)]
cctv = []
result = math.inf

for i in range(N):
    for j in range(M):
        if 1 <= board[i][j] <= 5:
            cctv.append((i, j, board[i][j]))


# 탐색
def dfs(board, depth):
    global result

    if depth == len(cctv):
        result = min(result, cnt_zero(board))
        return

    x, y, cctv_type = cctv[depth]
    for directions in cctv_dir[cctv_type]:
        tmp = [b[:] for b in board]
        tracking(x, y, directions, tmp)
        dfs(tmp, depth + 1)


def tracking(x, y, directions, board):
    for direction in directions:
        nx, ny = x, y
        while True:
            nx += dx[direction]
            ny += dy[direction]
            if nx < 0 or ny < 0 or nx >= N or ny >= M:
                break
            if board[nx][ny] == 6:
                break
            if board[nx][ny] == 0:
                board[nx][ny] = -1


def cnt_zero(board):
    cnt = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] == 0:
                cnt += 1
    return cnt


dfs(board, 0)
print(result)