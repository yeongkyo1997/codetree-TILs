import sys



# 도둑말 도망 치기
def run(board, depth):
    if depth > 16:
        return
    for i in range(N):
        for j in range(N):
            if not board[i][j] or not board[i][j][0] == depth:
                continue
            d = board[i][j][1]
            for _ in range(len(dir)):
                dx, dy = dir[d]
                nx, ny = i + dx, j + dy
                if 0 <= nx < N and 0 <= ny < N and (sx, sy) != (nx, ny):
                    board[i][j], board[nx][ny] = board[nx][ny], board[i][j]
                    break
                d = (d + 1) % len(dir)
            run(board, depth + 1)
            return
    run(board, depth + 1)


# 술래 움직이기
def move(board, x, y, d, acc):
    global result
    if not (0 <= x < N and 0 <= y < N) or board[x][y] == 0:
        result = max(result, acc)
        return
    if acc!=0:
        # 도망치기
        run(board, 1)
        
    if acc != 0:
        # 현재 도둑을 잡지 않는다면 바로 다음으로 이동
        dx, dy = dir[d]
        nx, ny = x + dx, y + dy
        move(board, nx, ny, d, acc)


    # 현재 도둑을 잡는다면
    tmp = [row[:] for row in board]
    nd = board[x][y][1]
    dx, dy = dir[nd]
    nx, ny = x + dx, y + dy
    tmp[x][y] = None
    move(tmp, nx, ny, nd, acc + board[x][y][0])


if __name__ == '__main__':
    dir = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]

    N = 4
    board = [[None] * N for _ in range(N)]

    for i in range(N):
        data = list(map(int, input().split()))
        for j in range(N):
            board[i][j] = (data[j * 2], data[j * 2 + 1] - 1)

    sx, sy, sd = 0, 0, board[i][j][1]
    result = 0
    move(board, sx, sy, sd, 0)
    print(result)