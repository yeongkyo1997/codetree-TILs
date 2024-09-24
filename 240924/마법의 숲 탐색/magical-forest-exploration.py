import collections
import math
import sys

# sys.stdin = open('마법의 숲 탐색', 'r')


# 골램 내리기
def move_down(col, d):
    global board
    x, y = 1, col

    while True:
        # 남쪽으로 이동
        left, right, down = y - 1, y + 1, x + 1
        if (0 <= down + 1 < R + 3
                and board[down][left] == 0
                and board[down][right] == 0
                and board[down + 1][y] == 0):
            x += 1
            continue
        # 왼쪽으로 이동
        up, right, left, down = x - 1, y + 1, y - 1, x + 1
        if (0 <= left - 1 < C
                and board[up][left] == 0
                and board[down][left] == 0
                and board[x][left - 1] == 0
                and 0 <= down + 1 < R + 3
                and board[down][y] == 0
                and board[down][left - 1] == 0
                and board[down + 1][left] == 0):
            x += 1
            y -= 1
            d = (d - 1) % 4
            continue

        # 오른쪽으로 이동
        up, right, left, down = x - 1, y + 1, y - 1, x + 1
        # 오른쪽 확인
        if (0 <= right + 1 < C
                and board[up][right] == 0
                and board[down][right] == 0
                and board[x][right + 1] == 0
                and 0 <= down + 1 < R + 3
                and board[down][y] == 0
                and board[down][right + 1] == 0
                and board[down + 1][right] == 0):
            # 아래 확인
            x += 1
            y += 1
            d = (d + 1) % 4
            continue
        if 0 <= x <= 3:
            board = [[0] * C for _ in range(R + 3)]
            return 0
        break

    board[x][y] = i
    for idx, (dx, dy) in enumerate(dir):
        nx, ny = x + dx, y + dy
        if idx == d:
            board[nx][ny] = -i
        else:
            board[nx][ny] = i
    return bfs(x, y, i)


# bfs
def bfs(x, y, val):
    q = collections.deque()
    visited = [[math.inf] * C for _ in range(R + 3)]
    q.append((x, y, val))
    ret = x - 3 + 1
    visited[x][y] = 1

    while q:
        x, y, val = q.popleft()
        ret = max(ret, x - 3 + 1)
        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < R + 3 and 0 <= ny < C and visited[x][y] + 1 <= visited[nx][ny] and board[nx][ny] != 0:
                # 번호라면 이동가능
                if abs(board[nx][ny]) == val:
                    visited[nx][ny] = visited[x][y] + 1
                    q.append((nx, ny, val))
                # 번호는 다르지만 출구인 경우
                elif board[x][y] == -val:

                    visited[nx][ny] = visited[x][y] + 1
                    q.append((nx, ny, abs(board[nx][ny])))
    return ret


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    R, C, K = map(int, input().split())

    board = [[0] * C for _ in range(R + 3)]
    result = 0
    for i in range(1, K + 1):
        c, d = map(int, input().split())
        c -= 1
        result += move_down(c, d)

    print(result)