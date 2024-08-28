def move_fungus(x, y, s, d, b):
    for _ in range(s):
        nx, ny = x + dx[d], y + dy[d]
        if 0 <= nx < n and 0 <= ny < m:
            x, y = nx, ny
        else:
            d = d ^ 1
            x, y = x + dx[d], y + dy[d]
    return x, y, d, b


def solve():
    global board
    ret = 0

    for col in range(m):
        for row in range(n):
            if board[row][col]:
                _, _, size = board[row][col][0]
                ret += size
                board[row][col] = []
                break

        new_board = [[[] for _ in range(m)] for _ in range(n)]
        for x in range(n):
            for y in range(m):
                for s, d, b in board[x][y]:
                    nx, ny, nd, nb = move_fungus(x, y, s, d, b)
                    new_board[nx][ny].append((s, nd, nb))

        for x in range(n):
            for y in range(m):
                if len(new_board[x][y]) > 1:
                    new_board[x][y].sort(key=lambda x: x[2], reverse=True)
                    new_board[x][y] = [new_board[x][y][0]]

        board = new_board

    return ret


if __name__ == '__main__':
    n, m, k = map(int, input().split())
    board = [[[] for _ in range(m)] for _ in range(n)]

    for _ in range(k):
        x, y, s, d, b = map(int, input().split())
        board[x - 1][y - 1].append((s, d - 1, b))

    dx = [-1, 1, 0, 0]
    dy = [0, 0, 1, -1]
    print(solve())