import math


def get_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def dfs(path, depth, start):
    global result
    if depth == m:
        total = 0
        for px, py in people:
            min_cost = math.inf
            for hx, hy in path:
                min_cost = min(min_cost, get_dist(px, py, hx, hy))
            total += min_cost
        result = min(total, result)
        return

    for i in range(start, len(hospitals)):
        path.append((hospitals[i]))
        dfs(path, depth + 1, i + 1)
        path.pop()


if __name__ == '__main__':
    n, m = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]

    people = []
    hospitals = []

    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                people.append((i, j))
            elif board[i][j] == 2:
                hospitals.append((i, j))

    result = math.inf

    dfs([], 0, 0)
    print(result)