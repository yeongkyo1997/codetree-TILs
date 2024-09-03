# 나무 성장
def grow():
    def cnt(x, y):
        ret = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] > 0:
                ret += 1
        return ret

    for i in range(n):
        for j in range(n):
            if board[i][j] > 0:
                board[i][j] += cnt(i, j)


# 나무 번식
def spread():
    global board

    def can_point(x, y):
        ret = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == 0:
                # 제초제가 뿌려진 경우 번식 불가
                if death[nx][ny] > 0:
                    continue
                ret.append((nx, ny))

        return ret

    new_board = [b[:] for b in board]

    for i in range(n):
        for j in range(n):
            if board[i][j] <= 0:
                continue
            points = can_point(i, j)
            for px, py in points:
                new_board[px][py] += board[i][j] // len(points)

    board = new_board


# 제초제 뿌리기
def remove_tree():
    global result

    # 제초제 뿌릴 곳 찾기
    def find(x, y):
        total = board[x][y]
        dir = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in dir:
            for i in range(1, k + 1):
                nx, ny = x + dx * i, y + dy * i

                if 0 <= nx < n and 0 <= ny < n:
                    if board[nx][ny] == -1:
                        break
                    if board[nx][ny] == 0:
                        break
                    total += board[nx][ny]

        return total

    # 가장 많이 제거할 수 있는 좌표와 양
    mount, mx, my = 0, -1, -1
    for i in range(n):
        for j in range(n):
            if board[i][j] <= 0:
                continue
            f = find(i, j)
            if f > mount:
                mount = f
                mx, my = i, j

    x, y = mx, my
    result += board[x][y]
    board[x][y] = 0
    death[x][y] = c + 1
    # 제초하기
    dir = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in dir:
        for i in range(1, k + 1):
            nx, ny = x + dx * i, y + dy * i

            if 0 <= nx < n and 0 <= ny < n:
                if board[nx][ny] == -1:
                    break
                if board[nx][ny] == 0:
                    death[nx][ny] = c + 1
                    break
                # 나무 죽이고
                result += board[nx][ny]
                board[nx][ny] = 0
                # 제초제 뿌리기
                death[nx][ny] = c + 1


# 제초제 감소시키기
def remove_death():
    for i in range(n):
        for j in range(n):
            death[i][j] = max(0, death[i][j] - 1)


if __name__ == '__main__':
    n, m, k, c = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    # 제초제
    death = [[0] * n for _ in range(n)]
    result = 0
    for _ in range(m):
        remove_death()
        grow()
        spread()
        remove_tree()

    print(result)