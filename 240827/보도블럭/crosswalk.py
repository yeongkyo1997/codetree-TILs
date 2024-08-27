def check(arr):
    visited = [False] * len(arr)

    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            continue
        # 오른쪽이 더 큰 경우
        elif arr[i + 1] - arr[i] == 1:
            # 시작은 i 끝은 i-L
            for j in range(i, i - L, -1):
                if j < 0:
                    return 0
                if arr[j] != arr[i] or visited[j]:
                    return 0
                visited[j] = True
        # 왼쪽이 더 큰 경우
        elif arr[i] - arr[i + 1] == 1:
            # 시작은 i+1
            for j in range(i + 1, i + 1 + L):
                if j >= n:
                    return 0
                if arr[j] != arr[i + 1] or visited[j]:
                    return 0
                visited[j] = True
        else:
            return 0
    return 1


if __name__ == '__main__':
    n, L = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    result = 0
    for b in board:
        result += check(b)
    board = list(zip(*board))

    for b in board:
        result += check(b)

    print(result)