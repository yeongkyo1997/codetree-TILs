import collections


def insert_num(arr):
    cnt_num = dict(collections.Counter(arr))
    arr.sort(key=lambda x: (cnt_num[x], x))

    new_arr = []

    visited = set()
    for a in arr:
        if a in visited:
            continue
        new_arr.append(a)
        new_arr.append(cnt_num[a])
        visited.add(a)

    if len(new_arr) > 100:
        new_arr = new_arr[:100]

    return new_arr


if __name__ == '__main__':
    r, c, k = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(3)]

    result = -1
    for time in range(101):
        if r - 1 < len(board) and c - 1 < len(board[0]) and board[r - 1][c - 1] == k:
            result = time
            break

        if len(board) >= len(board[0]):
            new_board = []
            max_len = 0
            for row in board:
                new_row = insert_num(row)
                new_board.append(new_row)
                max_len = max(max_len, len(new_row))
            for row in new_board:
                row.extend([0] * (max_len - len(row)))
            board = new_board
        else:
            board = list(map(list, zip(*board)))
            new_board = []
            max_len = 0
            for col in board:
                new_col = insert_num(col)
                new_board.append(new_col)
                max_len = max(max_len, len(new_col))
            for col in new_board:
                col.extend([0] * (max_len - len(col)))
            board = list(map(list, zip(*new_board)))

    print(result)