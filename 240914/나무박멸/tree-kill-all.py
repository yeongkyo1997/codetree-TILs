import collections
import math
import sys

# sys.stdin = open('나무박멸', 'r')


# 나무 성장
def grow():
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for x in range(N):
        for y in range(N):
            if board[x][y] <= 0:
                continue
            cnt = 0
            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < N and 0 <= ny < N and board[nx][ny] > 0 and death[nx, ny] == 0:
                    cnt += 1
            board[x][y] += cnt


# 나무 번식
def spread():
    global board
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    tmp = [b[:] for b in board]
    for x in range(N):
        for y in range(N):
            if board[x][y] <= 0:
                continue
            cnt = 0
            candi = []
            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < N and 0 <= ny < N and board[nx][ny] == 0 and death[nx, ny] == 0:
                    cnt += 1
                    candi.append((nx, ny))
            for cx, cy in candi:
                tmp[cx][cy] += board[x][y] // cnt

    board = tmp


# 제초제 뿌리기
def remove():
    global board, death, result

    dir = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def do(x, y):
        ret = board[x][y]
        for dx, dy in dir:
            for i in range(1, K + 1):
                nx, ny = x + dx * i, y + dy * i

                if 0 <= nx < N and 0 <= ny < N:
                    if board[nx][ny] <= 0:
                        break
                    ret += board[nx][ny]
        return ret

    max_val = -math.inf
    rx, ry = -1, -1
    for x in range(N):
        for y in range(N):
            if board[x][y] > 0:
                val = do(x, y)
                if max_val < val:
                    max_val = val
                    rx, ry = x, y
    if (rx, ry) == (-1, -1):
        return
    result += board[rx][ry]
    board[rx][ry] = 0
    death[rx, ry] = C + 1
    for dx, dy in dir:
        for i in range(1, K + 1):
            nx, ny = rx + dx * i, ry + dy * i
            if 0 <= nx < N and 0 <= ny < N and board[nx][ny] != -1:
                if board[nx][ny] == 0:
                    death[nx, ny] = C + 1
                    break
                death[nx, ny] = C + 1
                result += board[nx][ny]
                board[nx][ny] = 0
            else:
                break


# 제초제 줄이기
def reduce():
    for i in range(N):
        for j in range(N):
            if death[i, j] != 0:
                death[i, j] -= 1


if __name__ == '__main__':
    N, M, K, C = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    death = collections.defaultdict(int)

    result = 0
    for i in range(M):
        reduce()
        grow()
        spread()
        remove()

    print(result)