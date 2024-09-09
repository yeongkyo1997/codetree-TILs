import collections
import sys

def rotate():
    global board

    def rotate_90(board, row, col):
        size = 3
        tmp = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                tmp[j][size - i - 1] = board[i + row][j + col]

        for i in range(size):
            for j in range(size):
                board[i + row][j + col] = tmp[i][j]

    def rotate_180(board, row, col):
        size = 3
        tmp = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                tmp[size - i - 1][size - j - 1] = board[i + row][j + col]

        for i in range(size):
            for j in range(size):
                board[i + row][j + col] = tmp[i][j]

    def rotate_270(board, row, col):
        size = 3
        tmp = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                tmp[size - j - 1][i] = board[i + row][j + col]

        for i in range(size):
            for j in range(size):
                board[i + row][j + col] = tmp[i][j]

    next_board = None
    max_val = 0
    for i in range(3):
        for x in range(N - 2):
            for y in range(N - 2):
                tmp = [b[:] for b in board]
                if i == 0:
                    rotate_90(tmp, x, y)
                elif i == 1:
                    rotate_180(tmp, x, y)
                elif i == 2:
                    rotate_270(tmp, x, y)
                val = get_cnt(tmp)
                if max_val < val:
                    max_val = val
                    next_board = [t[:] for t in tmp]
    board = next_board
    return max_val


# 유물 개수
def get_cnt(board):
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def bfs(x, y):
        q = collections.deque()
        visited[x][y] = True
        q.append((x, y))
        path = [(x, y)]

        while q:
            x, y = q.popleft()
            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny] and board[x][y] == board[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))
                    path.append((nx, ny))

        if len(path) >= 3:
            for px, py in path:
                board[px][py] = 0
            return len(path)
        return 0

    ret = 0
    visited = [[False] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            ret += bfs(i, j)
    return ret


def fill():
    global idx
    for col in range(N):
        for row in range(N - 1, -1, -1):
            if board[row][col] == 0:
                board[row][col] = pieces[idx]
                idx += 1


if __name__ == '__main__':
    K, M = map(int, input().split())
    N = 5
    board = [list(map(int, input().split())) for _ in range(N)]
    pieces = list(map(int, input().split()))
    idx = 0
    for _ in range(K):
        result = 0
        cnt = rotate()

        if cnt == 0:
            break
        result += cnt
        fill()

        while True:
            cnt = get_cnt(board)
            fill()
            result += cnt
            if cnt == 0:
                print(result)
                break