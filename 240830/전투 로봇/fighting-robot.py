# 없앨 수 있는 몬스터 위치 구하기
import collections


def kill_pos():
    global exp, robot_level
    visited = [[False] * N for _ in range(N)]

    visited[rx][ry] = True
    q = collections.deque()
    q.append((rx, ry, 0))

    while q:
        x, y, depth = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and not visited[nx][ny] and robot_level >= board[nx][ny]:
                visited[nx][ny] = True

                # 레벨이 몬스터와 같다면
                if robot_level == board[nx][ny]:
                    q.append((nx, ny, depth + 1))
                # 크다면
                else:
                    if board[nx][ny] == 0:
                        q.append((nx, ny, depth + 1))
                    else:
                        exp += 1
                        board[nx][ny] = 0
                        if exp == robot_level:
                            robot_level += 1
                            exp = 0
                        return nx, ny, depth + 1

    # 없앨 수 있는 몬스터가 없다면
    return -1, -1, 0


if __name__ == '__main__':
    dir = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    N = int(input())
    board = [list(map(int, input().split())) for _ in range(N)]
    # 로봇 좌표
    rx, ry = -1, -1
    # 로봇 레벨
    robot_level = 2
    # 경험치
    exp = 0

    for i in range(N):
        for j in range(N):
            if board[i][j] == 9:
                rx, ry = i, j
                board[i][j] = 0

    result = 0
    while True:
        x, y, depth = kill_pos()
        rx, ry = x, y
        if depth == 0:
            break
        result += depth

    print(result)