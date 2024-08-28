import collections


def insert_num(arr):
    cnt_num = dict(collections.Counter(arr))
    arr = [x for x in arr if x != 0]  # 0 제거
    arr.sort(key=lambda x: (cnt_num[x], x))

    new_arr = []
    visited = set()
    for a in arr:
        if a in visited:
            continue
        new_arr.extend([a, cnt_num[a]])
        visited.add(a)

    return new_arr


def r_operation(board):
    new_board = []
    for row in board:
        new_row = insert_num(row)
        new_row = new_row[:100]  # 100개로 제한
        new_board.append(new_row)
    max_len = max(len(row) for row in new_board)
    for row in new_board:
        row.extend([0] * (max_len - len(row)))
    return new_board


def c_operation(board):
    board = list(map(list, zip(*board)))  # 전치
    board = r_operation(board)
    return list(map(list, zip(*board)))  # 다시 전치


if __name__ == '__main__':
    r, c, k = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(3)]

    result = -1
    for time in range(101):
        if r - 1 < len(board) and c - 1 < len(board[0]):
            if board[r - 1][c - 1] == k:
                result = time
                break

        if len(board) >= len(board[0]):
            board = r_operation(board)
        else:
            board = c_operation(board)

    print(result)