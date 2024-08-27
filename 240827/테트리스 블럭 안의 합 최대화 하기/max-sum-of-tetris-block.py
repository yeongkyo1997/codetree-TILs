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
            visited[x][y] = True
            block1(nx, ny, acc + board[nx][ny], depth + 1)
            visited[x][y] = False


# ㅗ 블록
def block2(x, y):
    global result
    path = [board[x][y]]
    for dx, dy in dir:
        nx, ny = x + dx, y + dy

        if 0 <= nx < n and 0 <= ny < m:
            path.append(board[nx][ny])

    if len(path) == 4:
        result = max(result, sum(path))
    elif len(path) == 5:
        path.sort()
        result = max(result, sum(path[1:]))


for i in range(n):
    for j in range(m):
        visited[i][j] = True
        block1(i, j, board[i][j], 1)
        visited[i][j] = False
        block2(i, j)
print(result)