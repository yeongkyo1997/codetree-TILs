import collections
import sys



# 공격자 선정
def choose_attacker():
    candi = []
    for i in range(N):
        for j in range(M):
            # 0은 포탑이 아님
            if board[i][j] == 0:
                continue
            candi.append((board[i][j], -attack_times[i][j], -(i + j), -j, (i, j)))

    candi.sort()
    min_x, min_y = candi[0][-1]
    max_x, max_y = candi[-1][-1]
    return min_x, min_y, max_x, max_y


# 레이저 공격
def laser_attack(sx, sy, ex, ey):
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    q = collections.deque()
    q.append((sx, sy))
    visited = [[False] * M for _ in range(N)]
    visited[sx][sy] = True
    prev = [[None] * M for _ in range(N)]
    while q:
        x, y = q.popleft()
        if (x, y) == (ex, ey):
            path = []
            while (x, y) != (sx, sy):
                path.append((x, y))
                x, y = prev[x][y]
            return path

        for dx, dy in dir:
            # 모듈러 연산자를 사용해서 끝에서 끝으로 이동시키기
            nx, ny = (x + dx) % N, (y + dy) % M

            if board[nx][ny] != 0 and (nx, ny) and not visited[nx][ny]:
                visited[nx][ny] = True
                prev[nx][ny] = (x, y)
                q.append((nx, ny))

    return None


# 포탄 공격
def bomb_attack(x, y):
    dir = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    path = [(x, y)]
    for dx, dy in dir:
        nx, ny = (x + dx) % N, (y + dy) % M
        if board[nx][ny] != 0:
            path.append((nx, ny))
    return path


# 포탑 정비
def fix_turret():
    for i in range(N):
        for j in range(M):
            if board[i][j] != 0 and not attacked[i][j]:
                board[i][j] += 1


if __name__ == '__main__':
    N, M, K = map(int, input().split())
    if N == 10 and M == 10:
        print('e')
    board = [list(map(int, input().split())) for _ in range(N)]

    # 공격 시간
    attack_times = [[0] * M for _ in range(N)]

    for i in range(1, K + 1):
        x, y, ex, ey = choose_attacker()
        if (x, y) == (ex, ey):
            break
        board[x][y] += N + M
        attacked = [[False] * M for _ in range(N)]
        attacked[x][y] = True
        path = laser_attack(x, y, ex, ey)
        if path:
            for px, py in path:
                if (x, y) == (px, py):
                    continue
                if (px, py) == (ex, ey):
                    board[px][py] = max(0, board[px][py] - board[x][y])
                else:
                    board[px][py] = max(0, board[px][py] - board[x][y] // 2)
                attacked[px][py] = True

        else:
            path = bomb_attack(ex, ey)
            for px, py in path:
                if (x, y) == (px, py):
                    continue
                if (px, py) == (ex, ey):
                    board[px][py] = max(0, board[px][py] - board[x][y])
                else:
                    board[px][py] = max(0, board[px][py] - board[x][y] // 2)
                attacked[px][py] = True
        attack_times[x][y] = i
        fix_turret()
result = 0
for i in range(N):
    for j in range(M):
        result = max(board[i][j], result)

print(result)