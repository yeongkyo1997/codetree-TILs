def first(board, virus):
    for i in range(n):
        for j in range(n):
            if virus[i][j]:
                virus[i][j].sort()

            new_virus = []
            dead_virus = 0
            for v in virus[i][j]:
                if board[i][j] >= v:
                    board[i][j] -= v
                    new_virus.append(v + 1)
                else:
                    dead_virus += v // 2
            board[i][j] += dead_virus
            virus[i][j] = new_virus


def third(virus):
    for i in range(n):
        for j in range(n):
            for v in virus[i][j]:
                if v % 5 == 0:
                    for dx, dy in dir:
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < n and 0 <= ny < n:
                            virus[nx][ny].append(1)


if __name__ == '__main__':
    dir = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    n, m, k = map(int, input().split())
    nutrients = [list(map(int, input().split())) for _ in range(n)]
    board = [[5] * n for _ in range(n)]  
    virus = [[[] for _ in range(n)] for _ in range(n)]
    for _ in range(m):
        r, c, age = map(int, input().split())
        r -= 1
        c -= 1
        virus[r][c].append(age)

    for _ in range(k):
        first(board, virus)
        third(virus)

        # 양분 추가
        for i in range(n):
            for j in range(n):
                board[i][j] += nutrients[i][j]

    result = sum(len(virus[i][j]) for i in range(n) for j in range(n))
    print(result)