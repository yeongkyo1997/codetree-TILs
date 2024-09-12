import collections
import sys

sys.stdin = open('색깔 폭탄', 'r')


# 터뜨릴 폭탄 묶음 찾고 터뜨리기
def bomb():
    # 폭탄 묶음의 개수
    def bfs(x, y):
        q = collections.deque()
        cnt = 1
        red_cnt = 0
        q.append((x, y))
        visited[x][y] = True

        while q:
            x, y = q.popleft()
            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < N and 0 <= ny < N and (board[nx][ny] == board[x][y] or board[nx][ny] == -2) and not \
                        visited[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))
                    cnt += 1
                    if board[nx][ny] == -2:
                        red_cnt += 1

        return cnt, red_cnt

    candi = []
    visited = [[False] * N for _ in range(N)]
    for i in range(N - 1, -1, -1):
        for j in range(N):
            if board[i][j] > 0 and not visited[i][j]:
                cnt, red_cnt = bfs(i, j)
                if cnt >= 2:
                    candi.append((-cnt, red_cnt, -i, j, (i, j)))
    if not candi:
        return False
    candi.sort()
    cnt = -candi[0][0]
    global result
    result += cnt ** 2
    x, y = candi[0][-1]

    # 터뜨리기
    q = collections.deque()
    visited = [[False] * N for _ in range(N)]
    q.append((x, y))
    path = [(x, y)]
    visited[x][y] = True

    while q:
        x, y = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny] and (
                    board[nx][ny] == -2 or board[nx][ny] == board[x][y]):
                q.append((nx, ny))
                visited[nx][ny] = True
                path.append((nx, ny))

    for px, py in path:
        board[px][py] = 0
    return True


# 중력작용
def down():
    for col in range(N):
        for row in range(N - 1, -1, -1):
            if board[row][col] == -1 or board[row][col] == 0:
                continue
            r = row
            while r + 1 < N:
                if board[r + 1][col] == 0:
                    board[r][col], board[r + 1][col] = board[r + 1][col], board[r][col]
                else:
                    break
                r += 1


# 반시계 회전
def rotate():
    global board
    board = list(map(list, zip(*board)))[::-1]


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    N, M = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    # 빨강 블록을 0이 아닌 -2로 변경
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                board[i][j] = -2
    result = 0
    while True:
        if not bomb():
            break
        down()
        rotate()
        down()
    print(result)