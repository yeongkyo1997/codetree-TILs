import collections
import math
import sys

sys.stdin = open('Main_20058', 'r')


# 마법 시전
def firestorm(row, col, size):
    if size == (1 << L):
        mid = size // 2
        origin_board = [b[::] for b in board]

        # 1->4
        for i in range(mid):
            for j in range(mid):
                board[row + i + mid][col + j + mid] = origin_board[row + i][col + j + mid]

        # 4->3
        for i in range(mid):
            for j in range(mid):
                board[row + i + mid][col + j] = origin_board[row + i + mid][col + j + mid]

        # 3->2
        for i in range(mid):
            for j in range(mid):
                board[row + i][col + j] = origin_board[row + i + mid][col + j]

        # 2->1
        for i in range(mid):
            for j in range(mid):
                board[row + i][col + j + mid] = origin_board[row + i][col + j]
        return
    mid = size // 2
    firestorm(row, col, mid)
    firestorm(row + mid, col, mid)
    firestorm(row, col + mid, mid)
    firestorm(row + mid, col + mid, mid)


# 얼음 녹이기
def melting():
    global board
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    tmp = [b[::] for b in board]
    for x in range(size):
        for y in range(size):
            cnt = 0
            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size and board[nx][ny] > 0:
                    cnt += 1
            if cnt < 3:
                tmp[x][y] = max(0, board[x][y] - 1)
    board = tmp


# 군집찾기
def find_cluster():
    def bfs(x, y):
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        q = collections.deque()
        visited = [[False] * size for _ in range(size)]
        visited[x][y] = True
        q.append((x, y))
        ret = 1

        while q:
            x, y = q.popleft()

            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < size and 0 <= ny < size and not visited[nx][ny] and board[nx][ny] != 0:
                    visited[nx][ny] = True
                    ret += 1
                    q.append((nx, ny))
        return ret

    ret = -math.inf

    for x in range(size):
        for y in range(size):
            if board[x][y] != 0:
                ret = max(ret, bfs(x, y))
    return ret


if __name__ == '__main__':
    N, Q = map(int, input().split())
    size = 1 << N
    board = [list(map(int, input().split())) for _ in range(size)]

    for L in map(int, input().split()):
        if L != 0:
            firestorm(0, 0, size)
        melting()

    total = sum(sum(b) for b in board)
    print(total)
    print(find_cluster())