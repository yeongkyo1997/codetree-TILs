import sys


def move(depth):
    def get_next(x, y, d):
        dx, dy = dir[d]
        nx, ny = x + dx, y + dy

        if 0 <= nx < N and 0 <= ny < N:
            if board[nx][ny] != 2:
                return nx, ny, d
            else:
                if d in [0, 1]:
                    d = 1 - d
                else:
                    d = 5 - d
                dx, dy = dir[d]
                nx, ny = x + dx, y + dy
                if not (0 <= nx < N and 0 <= ny < N) or board[nx][ny] == 2:
                    return x, y, d
                else:
                    return nx, ny, d
        else:
            if d in [0, 1]:
                d = 1 - d
            else:
                d = 5 - d
            dx, dy = dir[d]
            nx, ny = x + dx, y + dy
            if board[nx][ny] == 2:
                return x, y, d
            else:
                return nx, ny, d

    if depth == K:
        return

    ret = False
    for i in range(N):
        for j in range(N):
            if not pieces[i][j]:
                continue

            for num, (idx, d) in enumerate(pieces[i][j]):
                if idx == depth:
                    nx, ny, d = get_next(i, j, d)
                    pieces[i][j][num] = (idx, d)
                    arr = pieces[i][j][num:]
                    pieces[i][j] = pieces[i][j][:num]

                    if board[nx][ny] == 1:
                        arr = arr[::-1]

                    pieces[nx][ny].extend(arr)
                    if len(pieces[nx][ny]) >= 4:
                        ret = True

                    return move(depth + 1) or ret


if __name__ == '__main__':
    dir = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    N, K = map(int, input().split())

    board = [list(map(int, input().split())) for _ in range(N)]
    pieces = [[[] for _ in range(N)] for _ in range(N)]

    for idx in range(K):
        x, y, d = map(lambda x: int(x) - 1, input().split())
        pieces[x][y].append((idx, d))

    for t in range(1, 1001):
        if move(0):
            print(t)
            break
    else:
        print(-1)