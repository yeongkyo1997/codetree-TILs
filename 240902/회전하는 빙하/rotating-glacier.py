import collections
import copy


# 군집 찾기
def find_group():
    global max_group

    def bfs(x, y):
        q = collections.deque()
        q.append((x, y))
        visited[x][y] = True
        total = 1

        while q:
            x, y = q.popleft()

            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board_size and 0 <= ny < board_size and not visited[nx][ny] and board[nx][ny] != 0:
                    q.append((nx, ny))
                    visited[nx][ny] = True
                    total += 1

        return total

    visited = [[False] * board_size for _ in range(board_size)]
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] != 0 and not visited[i][j]:
                max_group = max(max_group, bfs(i, j))


# 녹이기
def melting():
    def check(x, y):
        cnt = 0
        for dx, dy in dir:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board_size and 0 <= ny < board_size and tmp[nx][ny] != 0:
                cnt += 1
        return cnt >= 3

    tmp = copy.deepcopy(board)
    for i in range(board_size):
        for j in range(board_size):
            if tmp[i][j] != 0 and not check(i, j):
                board[i][j] -= 1


# 회전하기
def rotate(row, col, size):
    if size == (1 << L):
        mid = size // 2
        # 회전
        origin_board = copy.deepcopy(board)

        # 3->2
        for i in range(mid):
            for j in range(mid):
                board[row + i][col + j] = origin_board[row + i + mid][col + j]
        # 2->1
        for i in range(mid):
            for j in range(mid):
                board[row + i][col + j + mid] = origin_board[row + i][col + j]
        # 4->3
        for i in range(mid):
            for j in range(mid):
                board[row + i + mid][col + j] = origin_board[row + i + mid][col + j + mid]
        # 2->4
        for i in range(mid):
            for j in range(mid):
                board[row + i + mid][col + j + mid] = origin_board[row + i][col + j + mid]
        return
    mid = size // 2
    rotate(row, col, mid)
    rotate(row, col + mid, mid)
    rotate(row + mid, col, mid)
    rotate(row + mid, col + mid, mid)


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    n, q = map(int, input().split())
    board_size = 1 << n
    board = [list(map(int, input().split())) for _ in range((board_size))]

    for L in map(int, input().split()):
        if L != 0:
            rotate(0, 0, board_size)
        melting()

    total = 0
    for b in board:
        total += sum(b)
    max_group = 0
    print(total)
    find_group()
    print(max_group)