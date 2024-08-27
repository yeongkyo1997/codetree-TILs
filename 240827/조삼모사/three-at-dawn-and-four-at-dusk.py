import math
import sys

input = lambda: sys.stdin.readline().rstrip()


def dfs(path, depth, start):
    global result
    if depth == n // 2:
        morning = 0
        night = 0

        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                else:
                    if i in path and j in path:
                        morning += board[i][j]
                    elif i not in path and j not in path:
                        night += board[i][j]

        result = min(result, abs(morning - night))

        return

    for i in range(start, n):
        if result == 0:
            return
        dfs(path | {i}, depth + 1, i + 1)


if __name__ == '__main__':
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(n)]
    result = math.inf
    dfs(set(), 0, 0)
    print(result)