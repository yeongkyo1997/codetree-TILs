import collections
import copy

dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# 불 퍼뜨리기
def bfs(board):
    global zero_cnt, result

    q = collections.deque(fire)
    cnt = zero_cnt
    while q:
        x, y = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < m and board[nx][ny] == 0:
                q.append((nx, ny))
                board[nx][ny] = 2
                cnt -= 1
    result = max(cnt, result)


# 방화벽 설치
def dfs(board, depth):
    if depth == 3:
        bfs(board)
        return

    for i in range(n):
        for j in range(m):
            tmp = copy.deepcopy(board)
            if tmp[i][j] == 0:
                tmp[i][j] = 1
                dfs(tmp, depth + 1)
                tmp[i][j] = 0


if __name__ == '__main__':
    n, m = map(int, input().split())

    board = [list(map(int, input().split())) for _ in range(n)]

    zero_cnt = -3
    fire = []

    for i in range(n):
        for j in range(m):
            if board[i][j] == 0:
                zero_cnt += 1
            elif board[i][j] == 2:
                fire.append((i, j))

    result = 0
    dfs(board, 0)
    print(result)