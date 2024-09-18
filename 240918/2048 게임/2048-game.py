import sys

# sys.stdin = open('Main_12100', 'r')


# 상
def up(board):
    for col in range(N):
        merged = False
        for pivot in range(N):
            for row in range(pivot + 1, N):
                if board[row][col] == 0:
                    continue

                # 기준과 움직이려는 값이 같고 아직 합친적이 없다면
                if board[row][col] == board[pivot][col] and not merged:
                    merged = True
                    board[pivot][col] *= 2
                    board[row][col] = 0
                    break
                else:
                    # 기준이 0이라면 움직이려는 값을 기준으로 이동
                    if board[pivot][col] == 0:
                        board[pivot][col], board[row][col] = board[row][col], board[pivot][col]
                    # 기준이 0이 아니라면 움직이려는 값 다음 칸으로 이동
                    else:
                        board[pivot + 1][col], board[row][col] = board[row][col], board[pivot + 1][col]
                        break


# 하
def down(board):
    for col in range(N):
        merged = False
        for pivot in range(N - 1, -1, -1):
            for row in range(pivot - 1, -1, -1):
                if board[row][col] == 0:
                    continue

                # 기준과 움직이려는 값이 같고 아직 합친적이 없다면
                if board[row][col] == board[pivot][col] and not merged:
                    merged = True
                    board[pivot][col] *= 2
                    board[row][col] = 0
                    break
                else:
                    # 기준이 0이라면 움직이려는 값을 기준으로 이동
                    if board[pivot][col] == 0:
                        board[pivot][col], board[row][col] = board[row][col], board[pivot][col]
                    # 기준이 0이 아니라면 움직이려는 값 다음 칸으로 이동
                    else:
                        board[pivot - 1][col], board[row][col] = board[row][col], board[pivot - 1][col]
                        break


# 좌
def left(board):
    for row in range(N):
        merged = False

        for pivot in range(N):
            for col in range(pivot + 1, N):
                if board[row][col] == 0:
                    continue
                # 기준과 움직이려는 값이 같고 아직 합친적이 없다면
                if board[row][col] == board[row][pivot] and not merged:
                    board[row][pivot] *= 2
                    board[row][col] = 0
                    merged = True
                    break
                else:
                    # 기준이 0이라면 움직이려는 값을 기준으로 이동
                    if board[row][pivot] == 0:
                        board[row][pivot], board[row][col] = board[row][col], board[row][pivot]
                    # 기준이 0이 아니라면 움직이려는 값 다음 칸으로 이동
                    else:
                        board[row][pivot + 1], board[row][col] = board[row][col], board[row][pivot + 1]
                        break


# 우
def right(board):
    for row in range(N):
        merged = False
        for pivot in range(N - 1, -1, -1):
            for col in range(pivot - 1, -1, -1):
                if board[row][col] == 0:
                    continue
                # 기준과 움직이려는 값이 같고 아직 합친적이 없다면
                if board[row][col] == board[row][pivot] and not merged:
                    board[row][pivot] *= 2
                    board[row][col] = 0
                    merged = True
                else:
                    # 기준이 0이라면 움직이려는 값을 기준으로 이동
                    if board[row][pivot] == 0:
                        board[row][pivot], board[row][col] = board[row][col], board[row][pivot]
                    # 기준이 0이 아니라면 움직이려는 값 다음 칸으로 이동
                    else:
                        board[row][pivot - 1], board[row][col] = board[row][col], board[row][pivot - 1]
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