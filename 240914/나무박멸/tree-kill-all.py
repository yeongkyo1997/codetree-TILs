import sys

# sys.stdin = open('나무박멸', 'r')


# 나무 성장
def grow():
    def grow(x, y):
        ret = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and board[nx][ny] > 0:
                ret += 1
        return ret

    for i in range(N):
        for j in range(N):
            if board[i][j] > 0:
                board[i][j] += grow(i, j)
    return board


# 나무 번식
def spread():
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    tmp = [row[:] for row in board]
    for i in range(N):
        for j in range(N):
            if board[i][j] <= 0:
                continue
            candi = []
            for dx, dy in dir:
                nx, ny = i + dx, j + dy
                if 0 <= nx < N and 0 <= ny < N and board[nx][ny] == 0 and death[nx][ny] == 0:
                    candi.append((nx, ny))
            for cx, cy in candi:
                tmp[cx][cy] += board[i][j] // len(candi)

    return tmp


# 제초제 뿌리기
def remove():
    # 제거되는 나무 수
    def calc(x, y):
        ret = board[x][y]
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for size in range(1, K + 1):
                nx, ny = x + dx * size, y + dy * size
                if 0 <= nx < N and 0 <= ny < N and board[nx][ny] > 0:
                    ret += board[nx][ny]
                else:
                    break
        return ret

    candi = []
    for i in range(N):
        for j in range(N):
            if board[i][j] > 0:
                candi.append((-calc(i, j), i, j, (i, j)))
    if not candi:
        return -1
    candi.sort()
    x, y = candi[0][-1]
    ret = board[x][y]
    board[x][y] = 0
    death[x][y] = C + 1
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        for size in range(1, K + 1):
            nx, ny = x + dx * size, y + dy * size
            if 0 <= nx < N and 0 <= ny < N:
                if board[nx][ny] <= 0:
                    death[nx][ny] = C + 1
                    break
                ret += board[nx][ny]
                board[nx][ny] = 0
                death[nx][ny] = C + 1

    return ret


# 제초제 줄이기
def reduce():
    for i in range(N):
        for j in range(N):
            death[i][j] = max(0, death[i][j] - 1)


if __name__ == '__main__':
    N, M, K, C = map(int, input().split())

    board = [list(map(int, input().split())) for _ in range(N)]
    # 제초제
    death = [[0] * N for _ in range(N)]

    result = 0
    # 로직 시작
    for _ in range(M):
        board = grow()
        board = spread()
        val = remove()
        if val < 0:
            break
        result += val
        reduce()

    print(result)