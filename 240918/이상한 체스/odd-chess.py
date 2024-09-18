import sys

# sys.stdin = open('이상한 체스', 'r')


# 한 조각이 탐색할 수 있는 위치 개수 및 탐색 체크
def search_check(board, sx, sy, move):
    for idx, d in enumerate(move):
        if d == 0:
            continue
        nx, ny = sx, sy

        dx, dy = dir[idx]

        while True:
            nx += dx
            ny += dy

            if not (0 <= nx < N and 0 <= ny < M):
                break
            if board[nx][ny] == 6:
                break
            if not (1 <= board[nx][ny] <= 5):
                board[nx][ny] = -1


# 체스판 탐색
def search_pieces(board, depth):
    global result
    if depth == len(pieces):
        ret = 0
        for b in board:
            ret += b.count(0)
        result = min(result, ret)
        return

    x, y = pieces[depth]
    for move in can_move[board[x][y]]:
        tmp = [b[:] for b in board]
        search_check(tmp, x, y, move)
        search_pieces(tmp, depth + 1)


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    can_move = [
        [],
        [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)],
        [(1, 0, 1, 0), (0, 1, 0, 1)],
        [(1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 1, 1), (1, 0, 0, 1)],
        [(1, 1, 1, 0), (0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1)],
        [(1, 1, 1, 1)]
    ]

    # 체스 조각 위치 저장
    pieces = []

    N, M = map(int, input().split())

    board = [list(map(int, input().split())) for _ in range(N)]
    result = N * M

    for i in range(N):
        for j in range(M):
            if 1 <= board[i][j] <= 5:
                pieces.append((i, j))
    search_pieces(board, 0)
    print(result)