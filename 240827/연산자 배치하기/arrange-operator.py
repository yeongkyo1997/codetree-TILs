import math


def dfs(acc, depth, plus, minus, multi):
    global max_result, min_result
    if depth == len(arr):
        max_result = max(max_result, acc)
        min_result = min(min_result, acc)
        return

    if plus > 0:
        dfs(acc + arr[depth], depth + 1, plus - 1, minus, multi)
    if minus > 0:
        dfs(acc - arr[depth], depth + 1, plus, minus - 1, multi)
    if multi > 0:
        dfs(acc * arr[depth], depth + 1, plus, minus, multi - 1)


if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))
    plus, minus, multi = map(int, input().split())
    max_result = -math.inf
    min_result = math.inf

    dfs(arr[0], 1, plus, minus, multi)
    print(min_result, max_result)