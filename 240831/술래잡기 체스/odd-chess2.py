import collections
import copy


# 술래 말 이동
def bfs(board, score, x, y, d):
    global result
    q = collections.deque()
    visited = set()
    visited.add(score)
    q.append((board, x, y, d, visited))
    move_sub(board, visited, x, y)


    while q:
        board, x, y, d, visited = q.popleft()
        # 다음으로 이동
        dx, dy = dir[d]
        nx, ny = x + dx, y + dy

        if nx < 0 or nx >= N or ny < 0 or ny >= N or board[nx][ny] == ():
            result = max(result, sum(visited))
            continue

        # 잡기
        tmp = copy.deepcopy(board)
        tmp[nx][ny] = ()
        # 도둑 이동시키기
        move_sub(tmp, visited, nx, ny)
        q.append((tmp, nx, ny, board[nx][ny][1], visited | {board[nx][ny][0]}))

        # 안잡기
        q.append((board, nx, ny, d, visited))


# 도둑 말 이동
def move_sub(board, visited, px, py):
    # 움직이기
    def move(num):
        for row in range(N):
            for col in range(N):
                if board[row][col] == ():
                    continue
                if board[row][col][0] == num:
                    d = board[row][col][1]
                    for _ in range(len(dir)):
                        dx, dy = dir[d]
                        nx, ny = row + dx, col + dy

                        if 0 <= nx < N and 0 <= ny < N:
                            # 술래 말이라면
                            if (row, col) == (px, py):
                                continue
                            board[row][col][1] = d
                            board[row][col], board[nx][ny] = board[nx][ny], board[row][col]
                            return
                        d = (d + 1) % len(dir)

    for num in range(1, 17):
        if num in visited:
            continue
        move(num)


if __name__ == '__main__':
    dir = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]

    N = 4
    _input = [list(map(int, input().split())) for _ in range(N)]

    board = [[] for _ in range(N)]

    for i in range(N):
        for j in range(0, N * 2, 2):
            board[i].append((_input[i][j:j + 2]))

    for i in range(N):
        for j in range(N):
            board[i][j][1] -= 1

    px, py, pd = 0, 0, board[0][0][1]
    result = board[0][0][0]
    board[0][0] = ()
    bfs(board, result, px, py, pd)

    print(result)