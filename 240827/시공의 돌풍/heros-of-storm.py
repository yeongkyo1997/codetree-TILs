R, C, T = map(int, input().rstrip().split())
board = [list(map(int, input().rstrip().split())) for _ in range(R)]
dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
up_row = -1
down_row = -1

for row in range(R):
    if board[row][0] == -1:
        if up_row == -1:
            up_row = row
        else:
            down_row = row


def spread_dust(board):
    ret_board = [[0] * C for _ in range(R)]
    for x in range(R):
        for y in range(C):
            if board[x][y] > 0:
                cnt = 0
                spread_amount = board[x][y] // 5
                for dx, dy in dir:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < R and 0 <= ny < C and board[nx][ny] != -1:
                        ret_board[nx][ny] += spread_amount
                        cnt += 1
                ret_board[x][y] += board[x][y] - spread_amount * cnt
            else:
                ret_board[x][y] += board[x][y]
    return ret_board


def move_dust(board):
    ret_board = [row[:] for row in board]

    # 위쪽 공기청정기
    for row in range(up_row - 1, 0, -1):
        ret_board[row][0] = board[row - 1][0]
    for col in range(C - 1):
        ret_board[0][col] = board[0][col + 1]
    for row in range(up_row):
        ret_board[row][C - 1] = board[row + 1][C - 1]
    for col in range(C - 1, 1, -1):
        ret_board[up_row][col] = board[up_row][col - 1]
    ret_board[up_row][1] = 0

    # 아래쪽 공기청정기
    for row in range(down_row + 1, R - 1):
        ret_board[row][0] = board[row + 1][0]
    for col in range(C - 1):
        ret_board[R - 1][col] = board[R - 1][col + 1]
    for row in range(R - 1, down_row, -1):
        ret_board[row][C - 1] = board[row - 1][C - 1]
    for col in range(C - 1, 1, -1):
        ret_board[down_row][col] = board[down_row][col - 1]
    ret_board[down_row][1] = 0

    ret_board[up_row][0] = -1
    ret_board[down_row][0] = -1

    return ret_board


for _ in range(T):
    board = spread_dust(board)
    board = move_dust(board)

print(sum(sum(b) for b in board) + 2)