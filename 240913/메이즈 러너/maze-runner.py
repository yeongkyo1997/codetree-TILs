import sys

# sys.stdin = open('메이즈 러너', 'r')


# 거리 계산
def get_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# 참가자 이동
def move():
    return


# 미로 회전
def rotate():
    global exit

    def rotate(row, col, size):
        global exit
        tmp = [[0] * size for _ in range(size)]

        # 벽 회전
        for i in range(size):
            for j in range(size):
                tmp[j][size - i - 1] = board[i + row][j + col]

        for i in range(size):
            for j in range(size):
                board[i + row][j + col] = max(0, tmp[i][j] - 1)

        # 참가자 회전
        for idx, (px, py) in enumerate(people):
            if row <= px < row + size and col <= py < col + size:
                ox, oy = px - row, py - col
                rx, ry = oy, size - ox - 1
                people[idx] = (rx + row, ry + col)

        # 출구 회전
        ex, ey = exit
        ox, oy = ex - row, ey - col
        rx, ry = oy, size - ox - 1
        exit = rx + row, ry + col

    # 가장 작은 정사각형 찾기
    for size in range(2, N + 1):
        for row in range(N - size + 1):
            for col in range(N - size + 1):
                is_people = False
                is_exit = False
                for px, py in people:
                    if exit == (px, py):
                        continue
                    if row <= exit[0] < row + size and col <= exit[1] < col + size:
                        is_exit = True
                    if row <= px < row + size and col <= py < col + size:
                        is_people = True
                # 가장 작은 정사각형을 찾았다면
                if is_people and is_exit:
                    rotate(row, col, size)
                    return


# 사람 움직이기
def move_people():
    cnt = 0
    for idx, (px, py) in enumerate(people):
        if exit == (px, py):
            continue
        # 다음 움직일 곳을 저장
        candi = [(get_dist(*exit, px, py), 0, (px, py))]

        for d, (dx, dy) in enumerate(dir):
            nx, ny = px + dx, py + dy
            if 0 <= nx < N and 0 <= ny < N and board[nx][ny] == 0:
                candi.append((get_dist(*exit, nx, ny), d, (nx, ny)))

        candi.sort()
        nx, ny = candi[0][-1]
        if (px, py) != (nx, ny):
            cnt += 1
        people[idx] = nx, ny
    return cnt


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    N, M, K = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    people = []
    for _ in range(M):
        people.append(tuple(map(lambda x: int(x) - 1, input().split())))
    exit = tuple(map(lambda x: int(x) - 1, input().split()))

    result = 0
    for _ in range(K):
        result += move_people()
        rotate()

    print(result)
    print(*map(lambda x: int(x) + 1, exit))