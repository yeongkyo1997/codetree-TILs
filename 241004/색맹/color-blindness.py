import collections
import sys


def get_area(board1, board2):
    def bfs(x, y):
        q = collections.deque()
        q.append((x, y))
        visited[x][y] = True
        if board1[x][y] == 'R':
            board2[x][y] = 'G'

        while q:
            x, y = q.popleft()

            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny] and board1[nx][ny] == board1[x][y]:
                    visited[nx][ny] = True
                    q.append((nx, ny))
                    if board1[nx][ny] == 'R':
                        board2[nx][ny] = 'G'
        return 1

    visited = [[False] * N for _ in range(N)]
    ret = 0
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                ret += bfs(i, j)

    return ret


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    N = int(input())
    board1 = [list(input()) for _ in range(N)]
    board2 = [b[:] for b in board1]
    print(get_area(board1, board2), get_area(board2, board2))