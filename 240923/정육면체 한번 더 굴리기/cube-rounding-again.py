import collections
import sys

# sys.stdin = open('정육면체 한번 더 굴리기', 'r')


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
    up, front, bottom, rear = rear, up, front, bottom

    return up, bottom, right, left, front, rear


def get_score(x, y):
    q = collections.deque()
    q.append((x, y))
    ret = board[x][y]
    visited = [[False] * N for _ in range(N)]
    visited[x][y] = True

    while q:
        x, y = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and board[x][y] == board[nx][ny] and not visited[nx][ny]:
                visited[nx][ny] = True
                ret += board[nx][ny]
                q.append((nx, ny))

    return ret


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
    # 방향
    d = 0
    # 현재 좌표
    x, y = 0, 1
    result = 0

    # 오른쪽으로 한칸 움직이기
    up, bottom, right, left, front, rear = turn_right(up, bottom, right, left, front, rear)
    result += get_score(x, y)

    for _ in range(M - 1):
        if bottom > board[x][y]:
            d = (d + 1) % 4
        elif bottom < board[x][y]:
            d = (d - 1) % 4
        dx, dy = dir[d]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < N and 0 <= ny < N):
            d = (d + 2) % 4
            dx, dy = dir[d]
            nx, ny = x + dx, y + dy
        x, y = nx, ny
        result += get_score(x, y)
        if d == 0:
            up, bottom, right, left, front, rear = turn_right(up, bottom, right, left, front, rear)
        elif d == 1:
            up, bottom, right, left, front, rear = turn_rear(up, bottom, right, left, front, rear)
        elif d == 2:
            up, bottom, right, left, front, rear = turn_left(up, bottom, right, left, front, rear)
        elif d == 3:
            up, bottom, right, left, front, rear = turn_front(up, bottom, right, left, front, rear)

    print(result)