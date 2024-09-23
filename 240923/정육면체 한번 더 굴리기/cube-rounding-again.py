import collections
import sys


def turn_right(up, bottom, right, left, front, rear):
    up, right, bottom, left = left, up, right, bottom

    return up, bottom, right, left, front, rear


def turn_left(up, bottom, right, left, front, rear):
    up, right, bottom, left = right, bottom, left, up

    return up, bottom, right, left, front, rear


def turn_front(up, bottom, right, left, front, rear):
    up, front, bottom, rear = rear, up, front, bottom

    return up, bottom, right, left, front, rear


def turn_rear(up, bottom, right, left, front, rear):
    up, front, bottom, rear = front, bottom, rear, up

    return up, bottom, right, left, front, rear


def DP():
    def bfs(x, y):
        q = collections.deque()
        q.append((x, y))
        total = board[x][y]
        path = {(x, y)}
        while q:
            x, y = q.popleft()
            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx < N and 0 <= ny < N and (nx, ny) not in path and board[nx][ny] == board[x][y]:
                    path.add((nx, ny))
                    q.append((nx, ny))
                    total += board[nx][ny]

        for px, py in path:
            dp[px][py] = total

    for i in range(N):
        for j in range(N):
            if dp[i][j] == 0:
                bfs(i, j)


if __name__ == '__main__':
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    up = 1
    bottom = 6
    right = 3
    left = 4
    front = 2
    rear = 5
    N, M = map(int, input().split())

    board = [list(map(int, input().split())) for _ in range(N)]
    dp = [[0] * N for _ in range(N)]
    DP()
    # 방향
    d = 0
    # 현재 좌표
    x, y = 0, 0
    result = 0

    for i in range(M):
        # 오른쪽으로
        if i == 0:
            up, bottom, right, left, front, rear = turn_right(up, bottom, right, left, front, rear)
            # 좌표만 움직이기
            dx, dy = dir[d]
            nx, ny = x + dx, y + dy
            if not (0 <= nx < N and 0 <= ny < N):
                d = (d + 2) % 4
                dx, dy = dir[d]
                nx, ny = x + dx, y + dy
            x, y = nx, ny
            result += dp[x][y]
        else:
            if bottom > board[x][y]:
                d = (d + 1) % 4
            elif bottom < board[x][y]:
                d = (d - 1) % 4
            # 좌표만 움직이기
            dx, dy = dir[d]
            nx, ny = x + dx, y + dy
            if not (0 <= nx < N and 0 <= ny < N):
                d = (d + 2) % 4
                dx, dy = dir[d]
                nx, ny = x + dx, y + dy
            x, y = nx, ny
            result += dp[x][y]
            # 회전
            if d == 0:
                up, bottom, right, left, front, rear = turn_right(up, bottom, right, left, front, rear)
            elif d == 1:
                up, bottom, right, left, front, rear = turn_front(up, bottom, right, left, front, rear)
            elif d == 2:
                up, bottom, right, left, front, rear = turn_left(up, bottom, right, left, front, rear)
            elif d == 3:
                up, bottom, right, left, front, rear = turn_rear(up, bottom, right, left, front, rear)



    print(result)