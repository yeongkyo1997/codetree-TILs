import collections
import sys




# 탐사 진행
def find():
    global board

    # 90도 회전
    def rotate_90(board, row, col):
        tmp = [[0] * 3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                tmp[j][3 - i - 1] = board[i + row][j + col]

        for i in range(3):
            for j in range(3):
                board[i + row][j + col] = tmp[i][j]

        return

    # 180도 회전
    def rotate_180(board, row, col):
        tmp = [[0] * 3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                tmp[3 - i - 1][3 - j - 1] = board[i + row][j + col]

        for i in range(3):
            for j in range(3):
                board[i + row][j + col] = tmp[i][j]
        return

    # 270도 회전
    def rotate_270(board, row, col):
        tmp = [[0] * 3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                tmp[3 - j - 1][i] = board[i + row][j + col]

        for i in range(3):
            for j in range(3):
                board[i + row][j + col] = tmp[i][j]
        return

    candi = None
    max_val = 0

    for i in range(3):
        for y in range(N - 2):
            for x in range(N - 2):
                tmp = [b[:] for b in board]
                if i == 0:
                    rotate_90(tmp, x, y)
                elif i == 1:
                    rotate_180(tmp, x, y)
                elif i == 2:
                    rotate_270(tmp, x, y)

                val = get_val(tmp)
                if max_val < val:
                    candi = [t[:] for t in tmp]
                    max_val = val

    board = candi
    return max_val


# 유물의 가치
def get_val(board):
    def bfs(x, y):
        q = collections.deque()
        q.append((x, y))
        visited[x][y] = True
        ret = 1
        candi = [(x, y)]

        while q:
            x, y = q.popleft()

            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny] and board[nx][ny] == board[x][y]:
                    visited[nx][ny] = True
                    ret += 1
                    q.append((nx, ny))
                    candi.append((nx, ny))

        if ret >= 3:
            for x, y in candi:
                board[x][y] = 0
            return ret
        return 0

    visited = [[False] * N for _ in range(N)]
    ret = 0
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                ret += bfs(i, j)

    return ret


# 유물 채우기
def fill():
    candi = []
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                candi.append((j, -i, (i, j)))
    candi.sort()

    for c in candi:
        x, y = c[-1]
        board[x][y] = next(itr)


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    N = 5
    K, M = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]

    # 유물 조각
    itr = iter(map(int, input().split()))
    for _ in range(K):
        result = 0
        val = find()
        if val == 0:
            break
        result += val
        fill()
        while True:
            val = get_val(board)
            if val == 0:
                break
            result += val
            fill()
        print(result, end=' ')