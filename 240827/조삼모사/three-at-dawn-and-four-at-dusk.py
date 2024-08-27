import math
import sys

input = lambda: sys.stdin.readline().rstrip()

def dfs(path, depth, start):
    global result
    if depth == n // 2:
        morning = 0
        night = 0

        morning_indices = list(path)
        night_indices = [i for i in range(n) if i not in path]

        for i in range(n // 2):
            for j in range(i + 1, n // 2):
                morning += board[morning_indices[i]][morning_indices[j]] + board[morning_indices[j]][morning_indices[i]]
                night += board[night_indices[i]][night_indices[j]] + board[night_indices[j]][night_indices[i]]

        result = min(result, abs(morning - night))
        return

    for i in range(start, n):
        if result == 0:
            return
        path.add(i)
        dfs(path, depth + 1, i + 1)
        path.discard(i)

if __name__ == '__main__':
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(n)]
    result = math.inf
    dfs(set(), 0, 0)
    print(result)