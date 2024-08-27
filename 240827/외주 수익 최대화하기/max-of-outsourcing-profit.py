def dfs(acc, depth):
    global result
    if depth >= n:
        result = max(result, acc)
        return

    # 일하기
    if depth + arr[depth][0] <= n:
        dfs(acc + arr[depth][1], depth + arr[depth][0])
    # 일 안 하기
    dfs(acc, depth + 1)


if __name__ == '__main__':
    n = int(input())
    arr = [list(map(int, input().split())) for _ in range(n)]
    result = 0

    dfs(0, 0)
    print(result)