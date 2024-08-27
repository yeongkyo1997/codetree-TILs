import copy

def right(board):
    for row in range(n):
        merged = [False] * n
        for pivot in range(n - 1, 0, -1):
            if board[row][pivot] == 0:
                continue
            for i in range(pivot - 1, -1, -1):
                if board[row][i] == 0:
                    continue
                if board[row][pivot] == board[row][i] and not merged[pivot]:
                    board[row][pivot] *= 2
                    board[row][i] = 0
                    merged[pivot] = True
                elif board[row][pivot] == 0:
                    board[row][pivot] = board[row][i]
                    board[row][i] = 0
                break
        # 빈 공간을 채우기 위해 다시 오른쪽으로 밀기
        for i in range(n - 1, 0, -1):
            if board[row][i] == 0:
                for j in range(i - 1, -1, -1):
                    if board[row][j] != 0:
                        board[row][i] = board[row][j]
                        board[row][j] = 0
                        break

# 왼쪽, 위, 아래 함수도 비슷하게 수정

def left(board):
    for row in range(n):
        merged = [False] * n
        for pivot in range(n - 1):
            if board[row][pivot] == 0:
                continue
            for i in range(pivot + 1, n):
                if board[row][i] == 0:
                    continue
                if board[row][pivot] == board[row][i] and not merged[pivot]:
                    board[row][pivot] *= 2
                    board[row][i] = 0
                    merged[pivot] = True
                elif board[row][pivot] == 0:
                    board[row][pivot] = board[row][i]
                    board[row][i] = 0
                break
        for i in range(n - 1):
            if board[row][i] == 0:
                for j in range(i + 1, n):
                    if board[row][j] != 0:
                        board[row][i] = board[row][j]
                        board[row][j] = 0
                        break

def up(board):
    for col in range(n):
        merged = [False] * n
        for pivot in range(n - 1):
            if board[pivot][col] == 0:
                continue
            for i in range(pivot + 1, n):
                if board[i][col] == 0:
                    continue
                if board[pivot][col] == board[i][col] and not merged[pivot]:
                    board[pivot][col] *= 2
                    board[i][col] = 0
                    merged[pivot] = True
                elif board[pivot][col] == 0:
                    board[pivot][col] = board[i][col]
                    board[i][col] = 0
                break
        for i in range(n - 1):
            if board[i][col] == 0:
                for j in range(i + 1, n):
                    if board[j][col] != 0:
                        board[i][col] = board[j][col]
                        board[j][col] = 0
                        break

def down(board):
    for col in range(n):
        merged = [False] * n
        for pivot in range(n - 1, 0, -1):
            if board[pivot][col] == 0:
                continue
            for i in range(pivot - 1, -1, -1):
                if board[i][col] == 0:
                    continue
                if board[pivot][col] == board[i][col] and not merged[pivot]:
                    board[pivot][col] *= 2
                    board[i][col] = 0
                    merged[pivot] = True
                elif board[pivot][col] == 0:
                    board[pivot][col] = board[i][col]
                    board[i][col] = 0
                break
        for i in range(n - 1, 0, -1):
            if board[i][col] == 0:
                for j in range(i - 1, -1, -1):
                    if board[j][col] != 0:
                        board[i][col] = board[j][col]
                        board[j][col] = 0
                        break

def dfs(board, depth):
    global result

    if depth == 5:
        for i in range(n):
            for j in range(n):
                result = max(result, board[i][j])
        return

    tmp = copy.deepcopy(board)
    left(tmp)
    dfs(tmp, depth + 1)
    tmp = copy.deepcopy(board)
    right(tmp)
    dfs(tmp, depth + 1)
    tmp = copy.deepcopy(board)
    up(tmp)
    dfs(tmp, depth + 1)
    tmp = copy.deepcopy(board)
    down(tmp)
    dfs(tmp, depth + 1)

if __name__ == '__main__':
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(n)]
    result = 0
    dfs(board, 0)
    print(result)