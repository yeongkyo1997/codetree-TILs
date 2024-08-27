import collections

dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

N, M = map(int, input().split())
board = [list(input()) for _ in range(N)]
rx, ry = -1, -1
bx, by = -1, -1
for i in range(N):
    for j in range(M):
        if board[i][j] == 'R':
            rx, ry = i, j
        elif board[i][j] == 'B':
            bx, by = i, j

visited = set()


def move(x, y, d):
    dx, dy = dir[d]
    cnt = 0

    while True:
        x += dx
        y += dy

        if board[x][y] == '#':
            return x - dx, y - dy, cnt
        elif board[x][y] == 'O':
            return x, y, cnt
        else:
            cnt += 1


def bfs(rx, ry, bx, by):
    q = collections.deque()
    q.append((rx, ry, bx, by, 0))
    visited.add((rx, ry, bx, by))

    while q:
        rx, ry, bx, by, depth = q.popleft()

        if depth > 10:
            return -1

        for d in range(len(dir)):
            dx, dy = dir[d]
            nbx, nby, b_cnt = move(bx, by, d)
            if board[nbx][nby] == 'O':
                continue
            nrx, nry, r_cnt = move(rx, ry, d)
            if board[nrx][nry] == 'O':
                return depth + 1

            if (nbx, nby) == (nrx, nry):
                if r_cnt > b_cnt:
                    nrx -= dx
                    nry -= dy
                else:
                    nbx -= dx
                    nby -= dy

            if (nrx, nry, nbx, nby) in visited:
                continue
            else:
                visited.add((nrx, nry, nbx, nby))
                q.append((nrx, nry, nbx, nby, depth + 1))
    return -1


print(bfs(rx, ry, bx, by))