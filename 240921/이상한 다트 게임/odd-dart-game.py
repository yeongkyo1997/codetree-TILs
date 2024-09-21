import collections
import copy
import sys

# sys.stdin = open('이상한 다트 게임', 'r')


# 원판 회전 시키기
def rotate(x, d, k):
    # 회전 시킬 원반 탐색
    for i in range(N):
        # 배수라면 회전
        if (i + 1) % x == 0:
            # 시계 방향
            if d == 0:
                board[i].rotate(k)
            else:
                board[i].rotate(-k)


# 인접한 숫자 지우기
def remove():
    dir = [(-1, 0,), (0, 1), (1, 0), (0, -1)]

    # 인접한 숫자 있는지 확인
    def check(board, x, y, num):
        for dx, dy in dir:
            nx, ny = x + dx, (y + dy) % M
            if 0 <= nx < N and board[nx][ny] == num:
                return True
        return False

    tmp = copy.deepcopy(board)
    flag = False
    for i in range(N):
        for j in range(M):
            if board[i][j] == -1:
                continue
            if check(board, i, j, board[i][j]):
                flag = True
                tmp[i][j] = -1

    return tmp, flag


# 정규화
def normalization():
    total = 0
    cnt = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] != -1:
                cnt += 1
                total += board[i][j]

    mean = total // cnt

    for i in range(N):
        for j in range(M):
            if board[i][j] == -1:
                continue

            if board[i][j] > mean:
                board[i][j] -= 1
            elif board[i][j] < mean:
                board[i][j] += 1


if __name__ == '__main__':
    N, M, Q = map(int, input().split())

    board = [collections.deque(map(int, input().split())) for _ in range(N)]

    for _ in range(Q):
        x, d, k = map(int, input().split())
        rotate(x, d, k)
        board, flag = remove()
        if not flag:
            normalization()

    result = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] == -1:
                continue
            result += board[i][j]

    print(result)