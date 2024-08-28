def solution(n, h, ladders):
    board = [[0] * n for _ in range(h + 1)]

    for a, b in ladders:
        board[a - 1][b - 1] = 1

    def check():
        for i in range(n):
            cur = i
            for j in range(h):
                if board[j][cur]:
                    cur += 1
                elif cur > 0 and board[j][cur - 1]:
                    cur -= 1
            if cur != i:
                return False
        return True

    def dfs(cnt, x, y):
        if cnt > 3:
            return -1
        if check():
            return cnt

        ret = -1
        for i in range(x, h):
            k = y if i == x else 0
            for j in range(k, n - 1):
                if board[i][j] == 0:
                    if (j > 0 and board[i][j - 1] == 1) or (board[i][j + 1] == 1):
                        continue
                    board[i][j] = 1
                    temp = dfs(cnt + 1, i, j + 2)
                    if temp != -1:
                        ret = temp if ret == -1 else min(ret, temp)
                    board[i][j] = 0
        return ret

    return dfs(0, 0, 0)


n, m, h = map(int, input().split())
ladders = [list(map(int, input().split())) for _ in range(m)]

print(solution(n, h, ladders))