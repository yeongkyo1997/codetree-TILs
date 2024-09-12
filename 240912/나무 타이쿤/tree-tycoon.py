import sys


# 영양제 이동
def move_energy(d, p):
    tmp = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if not energy[i][j]:
                continue
            dx, dy = dir[d]
            nx, ny = (i + dx * p) % N, (j + dy * p) % N
            tmp[nx][ny] = 1

    return tmp


# 나무 성장
def grow():
    def get_cnt(x, y):
        dir = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        ret = 0
        for dx, dy in dir:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and board[nx][ny] > 0:
                ret += 1

        return ret

    for i in range(N):
        for j in range(N):
            if energy[i][j] == 1:
                board[i][j] += 1

    for i in range(N):
        for j in range(N):
            if energy[i][j] == 1:
                board[i][j] += get_cnt(i, j)


# 나무 자르고 영양제 추가하기
def cut():
    for i in range(N):
        for j in range(N):
            if board[i][j] >= 2 and not prev_energy[i][j]:
                board[i][j] -= 2
                energy[i][j] += 1


if __name__ == '__main__':
    dir = [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]

    N, M = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    energy = [[0] * N for _ in range(N)]
    energy[-1][0] = energy[-1][1] = energy[-2][0] = energy[-2][1] = 1

    for _ in range(M):
        d, p = map(int, input().split())
        d -= 1
        energy = move_energy(d, p)
        prev_energy = [e[:] for e in energy]
        grow()
        energy = [[0] * N for _ in range(N)]
        cut()

    result = sum(sum(b) for b in board)
    print(result)