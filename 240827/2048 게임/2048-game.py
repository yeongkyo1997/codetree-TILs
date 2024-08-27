import copy


# 오른쪽
def right(board):
    for row in range(n):
        # 기준점을 잡고 같으면 합체 아니면 이전까지 이동
        for pivot in range(n - 1, 0, -1):
            for i in range(pivot - 1, -1, -1):
                if board[row][i] != 0:
                    # 기준점이 0이면 위치로 이동
                    if board[row][pivot] == 0:
                        board[row][pivot] = board[row][i]
                        board[row][i] = 0
                        break
                    else:
                        # 같으면 합체
                        if board[row][pivot] == board[row][i]:
                            board[row][i] = 0
                            board[row][pivot] *= 2
                            break
                        else:
                            board[row][pivot - 1] = board[row][i]
                            board[row][i] = 0
                            break


# 왼쪽
def left(board):
    for row in range(n):
        for pivot in range(n - 1):
            for i in range(pivot + 1, n):
                if board[row][i] != 0:
                    if board[row][pivot] == 0:
                        board[row][pivot] = board[row][i]
                        board[row][i] = 0
                        break
                    else:
                        if board[row][pivot] == board[row][i]:
                            board[row][i] = 0
                            board[row][pivot] *= 2
                            break
                        else:
                            board[row][pivot + 1] = board[row][i]
                            board[row][i] = 0
                            break


# 위
def up(board):
    for col in range(n):
        # 기준점
        for pivot in range(n - 1):
            for i in range(pivot + 1, n):
                if board[i][col] != 0:
                    # 기준점이 0이면
                    if board[pivot][col] == 0:
                        board[pivot][col] = board[i][col]
                        board[i][col] = 0
                        break
                    else:
                        # 기준점이랑 같다면
                        if board[pivot][col] == board[i][col]:
                            board[i][col] = 0
                            board[pivot][col] *= 2
                            break
                        else:
                            board[pivot + 1][col] = board[i][col]
                            board[i][col] = 0
                            break


# 아래
def down(board):
    for col in range(n):
        # 기준점
        for pivot in range(n - 1, -1, -1):
            for i in range(pivot - 1, -1, -1):
                if board[i][col] != 0:
                    # 기준점이 0이면
                    if board[pivot][col] == 0:
                        board[pivot][col] = board[i][col]
                        board[i][col] = 0
                        break
                    else:
                        # 기준점과 같다면
                        if board[pivot][col] == board[i][col]:
                            board[i][col] = 0
                            board[pivot][col] *= 2
                            break
                        else:
                            board[pivot - 1][col] = board[i][col]
                            board[i][col] = 0
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