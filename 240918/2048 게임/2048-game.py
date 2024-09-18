import sys

# sys.stdin = open('Main_12100', 'r')


# 상
def up(board):
    for col in range(N):
        pivot = 0
        merged = set()
        while True:
            if pivot == N:
                break
            for row in range(pivot + 1, N):
                # 현재 값이 0이라면 무시
                if board[row][col] == 0:
                    continue

                # pivot에 있는 값이 0이라면 바로 이동
                if board[pivot][col] == 0:
                    board[pivot][col] = board[row][col]
                    board[row][col] = 0
                else:
                    # pivot과 현재 값이 같다면
                    if board[pivot][col] == board[row][col] and pivot not in merged:
                        board[row][col] = 0
                        board[pivot][col] *= 2
                        merged.add(pivot)
                        pivot += 1
                        break
                    # 다르다면 앞 칸에 배치
                    else:
                        if board[pivot + 1][col] == 0:
                            board[pivot + 1][col] = board[row][col]
                            board[row][col] = 0
                        pivot += 1
                        break
            else:
                break


# 하
def down(board):
    for col in range(N):
        pivot = N - 1
        merged = set()
        while True:
            if pivot == 0:
                break
            for row in range(pivot - 1, -1, -1):
                # 현재 값이 0이라면 무시
                if board[row][col] == 0:
                    continue

                # pivot에 있는 값이 0이라면 바로 이동
                if board[pivot][col] == 0:
                    board[pivot][col] = board[row][col]
                    board[row][col] = 0
                else:
                    # pivot과 현재 값이 같다면
                    if board[pivot][col] == board[row][col] and pivot not in merged:
                        board[row][col] = 0
                        board[pivot][col] *= 2
                        merged.add(pivot)
                        pivot -= 1
                        break
                    # 다르다면 앞 칸에 배치
                    else:
                        if board[pivot - 1][col] == 0:
                            board[pivot - 1][col] = board[row][col]
                            board[row][col] = 0
                        pivot -= 1
                        break
            else:
                break


# 좌
def left(board):
    for row in range(N):
        pivot = 0
        merged = set()
        while True:
            if pivot == N:
                break
            for col in range(pivot + 1, N):
                # 현재 값이 0이라면 무시
                if board[row][col] == 0:
                    continue

                # pivot에 있는 값이 0이라면 바로 이동
                if board[row][pivot] == 0:
                    board[row][pivot] = board[row][col]
                    board[row][col] = 0
                else:
                    # pivot과 현재 값이 같다면
                    if board[row][pivot] == board[row][col] and pivot not in merged:
                        board[row][col] = 0
                        board[row][pivot] *= 2
                        merged.add(pivot)
                        pivot += 1
                        break
                    # 다르다면 앞 칸에 배치
                    else:
                        if board[row][pivot + 1] == 0:
                            board[row][pivot + 1] = board[row][col]
                            board[row][col] = 0
                        pivot += 1
                        break
            else:
                break


# 우
def right(board):
    for row in range(N):
        pivot = N - 1
        merged = set()
        while True:
            if pivot == 0:
                break
            for col in range(pivot - 1, -1, -1):
                # 현재 값이 0이라면 무시
                if board[row][col] == 0:
                    continue

                # pivot에 있는 값이 0이라면 바로 이동
                if board[row][pivot] == 0:
                    board[row][pivot] = board[row][col]
                    board[row][col] = 0
                else:
                    # pivot과 현재 값이 같다면
                    if board[row][pivot] == board[row][col] and pivot not in merged:
                        board[row][col] = 0
                        board[row][pivot] *= 2
                        merged.add(pivot)
                        pivot -= 1
                        break
                    # 다르다면 앞 칸에 배치
                    else:
                        if board[row][pivot - 1] == 0:
                            board[row][pivot - 1] = board[row][col]
                            board[row][col] = 0
                        pivot -= 1
                        break
            else:
                break


# 방향 dfs
def dfs(board, depth):
    global result

    if depth == 5:
        val = max(max(b) for b in board)
        result = max(result, val)
        return

    tmp = [b[:] for b in board]
    up(tmp)
    dfs(tmp, depth + 1)
    tmp = [b[:] for b in board]
    down(tmp)
    dfs(tmp, depth + 1)
    tmp = [b[:] for b in board]
    left(tmp)
    dfs(tmp, depth + 1)
    tmp = [b[:] for b in board]
    right(tmp)
    dfs(tmp, depth + 1)


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    N = int(input())
    board = [list(map(int, input().split())) for _ in range(N)]

    result = 0

    dfs(board, 0)

    print(result)