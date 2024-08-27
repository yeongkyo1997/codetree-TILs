dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

n, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]

result = 0
visited = [[False] * m for _ in range(n)]


# ㅗ를 제외한 블록
def block1(x, y, acc, depth):
    global result

    if depth == 4:
        result = max(result, acc)
        return

    for dx, dy in dir:
        nx, ny = x + dx, y + dy

        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny]:
            visited[nx][ny] = True
            block1(nx, ny, acc + board[nx][ny], depth + 1)
            visited[nx][ny] = False


# ㅗ 블록
def block2(x, y):
    global result

    if x >= 1 and 1 <= y < m - 1:
        # ㅗ 모양
        result = max(result, board[x][y] + board[x-1][y] + board[x][y-1] + board[x][y+1])
    if x < n - 1 and 1 <= y < m - 1:
        # ㅜ 모양
        result = max(result, board[x][y] + board[x+1][y] + board[x][y-1] + board[x][y+1])
    if 1 <= x < n - 1 and y >= 1:
        # ㅓ 모양
        result = max(result, board[x][y] + board[x-1][y] + board[x+1][y] + board[x][y-1])
    if 1 <= x < n - 1 and y < m - 1:
        # ㅏ 모양
        result = max(result, board[x][y] + board[x-1][y] + board[x+1][y] + board[x][y+1])


for i in range(n):
    for j in range(m):  # 열의 개수는 m
        visited[i][j] = True
        block1(i, j, board[i][j], 1)
        visited[i][j] = False
        block2(i, j)

print(result)