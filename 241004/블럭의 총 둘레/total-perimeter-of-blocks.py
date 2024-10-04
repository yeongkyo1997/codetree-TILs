import collections
import sys



def bfs(x, y):
    q = collections.deque()
    visited = set()
    visited.add((x, y))
    q.append((x, y))

    while q:
        x, y = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and (nx, ny) not in visited:
                if board[nx][ny] == 1:
                    cnt_board[nx][ny] += 1
                else:
                    q.append((nx, ny))
                    visited.add((nx, ny))


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    block_num = int(input())

    N = 110

    board = [[0] * N for _ in range(N)]
    cnt_board = [[0] * N for _ in range(N)]
    for _ in range(block_num):
        r, c = map(int, input().split())
        
        board[r][c] = 1
    bfs(0, 0)
    print(sum(sum(b) for b in cnt_board))