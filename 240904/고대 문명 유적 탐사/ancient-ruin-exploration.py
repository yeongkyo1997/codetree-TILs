import collections
import sys

# sys.stdin = open('input.txt', 'r')


# 격자 선택하기
def choose():
    def rotate_90(board, x, y):
        tmp = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                tmp[j][3 - i - 1] = board[i + x][j + y]

        apply(board, tmp, x, y)

    def rotate_180(board, x, y):
        tmp = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                tmp[3 - j - 1][3 - i - 1] = board[i + x][j + y]

        apply(board, tmp, x, y)

    def rotate_270(board, x, y):
        tmp = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                tmp[3 - j - 1][i] = board[i + x][j + y]

        apply(board, tmp, x, y)

    def apply(board, tmp, x, y):
        for i in range(3):
            for j in range(3):
                board[i + x][j + y] = tmp[i][j]

    min_board = None
    max_value = 0

    for i in range(3):
        for row in range(N - 2):
            for col in range(N - 2):
                rotate_board = [b[::] for b in board]
                if i == 0:
                    rotate_90(rotate_board, row, col)
                    total = get(rotate_board)
                    if max_value < total:
                        min_board = [b[::] for b in rotate_board]
                        max_value = total
                elif i == 1:
                    rotate_180(rotate_board, row, col)
                    total = get(rotate_board)
                    if max_value < total:
                        min_board = [b[::] for b in rotate_board]
                        max_value = total
                elif i == 2:
                    rotate_270(rotate_board, row, col)
                    total = get(rotate_board)
                    if max_value < total:
                        min_board = [b[::] for b in rotate_board]
                        max_value = total
    return min_board


# 유물 1차 획득
def get(board):
    def bfs(x, y, num):
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        q = collections.deque()
        q.append((x, y))
        visited[x][y] = True
        total = 1

        while q:
            x, y = q.popleft()
            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny] and board[nx][ny] == num:
                    visited[nx][ny] = True
                    q.append((nx, ny))
                    total += 1

        return total if total >= 3 else 0

    visited = [[False] * N for _ in range(N)]
    ret = 0
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                ret += bfs(i, j, board[i][j])
    return ret


# 유물 지우기
def remove():
    def bfs(x, y):
        global result
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        q = collections.deque()
        q.append((x, y))
        path = set()
        path.add((x, y))
        visited[x][y] = True

        while q:
            x, y = q.popleft()
            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < N and 0 <= ny < N and board[x][y] == board[nx][ny] and (nx, ny) not in path and not \
                        visited[nx][ny]:
                    path.add((nx, ny))
                    visited[nx][ny] = True
                    q.append((nx, ny))

        if len(path) >= 3:
            result += len(path)
            for px, py in path:
                board[px][py] = 0

    visited = [[False] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                bfs(i, j)


# 유물 채우기
def fill():
    global idx
    for col in range(N):
        for row in range(N - 1, -1, -1):
            if board[row][col] == 0:
                board[row][col] = arr[idx]
                idx += 1


# 0이 있는지 확인
def is_zero():
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return True
    return False


if __name__ == '__main__':
    K, M = map(int, input().split())
    N = 5
    board = [list(map(int, input().split())) for _ in range(N)]
    arr = list(map(int, input().split()))
    result = 0

    idx = 0
    for _ in range(K):
        board = choose()
        if not board:
            break
        while True:
            if not is_zero():
                remove()
                break
            fill()
    print(result)