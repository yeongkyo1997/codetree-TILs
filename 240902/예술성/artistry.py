import collections


# 십자가 기준 회전하기
def cross_rotate(board):
    def rotate(row, col):
        tmp = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                tmp[j][size - i - 1] = board[row + i][col + j]
        for i in range(size):
            for j in range(size):
                board[row + i][col + j] = tmp[i][j]

    # 십자가 회전하기
    def plus_rotate():
        tmp = [[0] * n for _ in range(n)]
        for i in range(n):
            for r, c in [(i, size), (size, i)]:
                tmp[n - c - 1][r] = board[r][c]

        for i in range(n):
            for r, c in [(i, size), (size, i)]:
                board[r][c] = tmp[r][c]

    size = n // 2
    # 1 사분면
    rotate(0, size + 1)

    # 2 사분면
    rotate(0, 0)

    # 3 사분면
    rotate(size + 1, 0)

    # 4 사분면
    rotate(size + 1, size + 1)
    plus_rotate()


# 그룹 나누기
def split_group():
    def split(x, y, num):
        q = collections.deque()
        q.append((x, y))
        group_board[x][y] = group_num
        group_info[group_num].append((x, y))

        while q:
            x, y = q.popleft()

            for dx, dy in dir:
                nx, ny = x + dx, y + dy

                if 0 <= nx < n and 0 <= ny < n and group_board[nx][ny] == 0 and board[nx][ny] == num:
                    group_board[nx][ny] = group_num
                    q.append((nx, ny))
                    group_info[group_num].append((nx, ny))

    group_num = 1
    for i in range(n):
        for j in range(n):
            if group_board[i][j] == 0:
                split(i, j, board[i][j])
                group_num += 1


# 점수계산하기
def get_score():
    ret = 0
    matches = [[0] * (len(group_info) + 1) for _ in range(len(group_info) + 1)]
    for i in group_info.keys():
        for x, y in group_info[i]:
            # 맞닿아 있는 것 확인
            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    if group_board[nx][ny] != i:
                        matches[i][group_board[nx][ny]] += 1
        total = 0
        # 계산하기
        for col in group_info.keys():
            if i >= col:
                continue
            x, y = group_info[i][0]
            gx, gy = group_info[col][0]
            total += (len(group_info[i]) + len(group_info[col])) * board[x][y] * board[gx][gy] * matches[i][col]
        ret += total
    return ret


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(n)]

    result = 0
    for _ in range(4):
        group_board = [[0] * n for _ in range(n)]
        group_info = collections.defaultdict(list)
        split_group()
        result += get_score()
        cross_rotate(board)

    print(result)