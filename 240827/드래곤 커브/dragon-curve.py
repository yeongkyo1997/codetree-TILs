dir = [(1, 0), (0, -1), (-1, 0), (0, 1)]
N = 101
board = [[0] * N for _ in range(N)]
curve = []

for _ in range(int(input())):
    y, x, d, g = map(int, input().split())
    curve = [d]
    board[x][y] = 1

    for _ in range(g):
        for i in range(len(curve) - 1, -1, -1):
            curve.append((curve[i] + 1) % 4)

    for i in curve:
        dx, dy = dir[i]
        x_new, y_new = x + dx, y + dy
        if 0 <= x_new < N and 0 <= y_new < N:
            board[x_new][y_new] = 1
            x, y = x_new, y_new

result = 0

for i in range(N - 1):
    for j in range(N - 1):
        if board[i][j] and board[i + 1][j] and board[i][j + 1] and board[i + 1][j + 1]:
            result += 1

print(result)