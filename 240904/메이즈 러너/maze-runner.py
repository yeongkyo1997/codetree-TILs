import sys

# sys.stdin = open('input.txt', 'r')


# 영역 회전시키기
def rotate(row, col, size, candi):
    global ex, ey
    tmp = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            # 내구도 감소시키기
            tmp[i][j] = max(0, board[row + i][col + j] - 1)

    tmp = list(zip(*tmp[::-1]))

    for i in range(size):
        for j in range(size):
            board[row + i][col + j] = tmp[i][j]

    # 출구 회전 시키기
    ox, oy = ex - row, ey - col
    rx, ry = oy, size - ox - 1
    ex = rx + row
    ey = ry + col

    for i in candi:
        px, py = people[i]
        ox, oy = px - row, py - col
        rx, ry = oy, size - ox - 1
        px = rx + row
        py = ry + col
        people[i] = (px, py)


# 영역 찾기
def find_area():
    for size in range(2, N + 1):
        for i in range(N - size + 1):
            for j in range(N - size + 1):
                is_exit = False
                candi = []
                for r in range(i, i + size):
                    for c in range(j, j + size):
                        if (r, c) == (ex, ey):
                            is_exit = True
                            continue
                        for idx, (px, py) in enumerate(people):
                            if (px, py) == (r, c):
                                candi.append(idx)
                                break

                if is_exit and candi:
                    return i, j, size, candi


# 이동하기
def move():
    global result

    def get_dist(x, y):
        return abs(ex - x) + abs(ey - y)

    # 다음 좌표 찾기
    def next_pos(x, y):
        global result
        min_dist = get_dist(x, y)
        px, py = x, y
        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and board[nx][ny] == 0:
                dist = get_dist(nx, ny)
                if dist < min_dist:
                    px, py = nx, ny
                    min_dist = dist
        if (x, y) != (px, py):
            result += 1
        return px, py

    for i in range(len(people) - 1, -1, -1):
        px, py = people[i]

        px, py = next_pos(px, py)
        people[i] = px, py

        if (px, py) == (ex, ey):
            del people[i]


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    N, M, K = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(N)]
    people = []

    for _ in range(M):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        people.append((x, y))

    ex, ey = map(lambda x: int(x) - 1, input().split())
    result = 0
    for _ in range(K):
        move()
        x, y, size, candi = find_area()
        rotate(x, y, size, candi)
        if not people:
            break
    print(result)
    print(ex + 1, ey + 1)