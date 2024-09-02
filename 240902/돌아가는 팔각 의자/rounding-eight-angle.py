import collections
import copy


def rotate(n, d):
    tmp = [copy.copy(b) for b in board]
    board[n].rotate(d)

    nn, nd = n, d
    # 오른쪽
    while nn + 1 <= 4:
        if tmp[nn][2] == tmp[nn + 1][-2]:
            break
        else:
            nd *= -1
            board[nn + 1].rotate(nd)
        nn += 1

    nn, nd = n, d
    # 왼쪽
    while nn - 1 >= 1:
        if tmp[nn][-2] == tmp[nn - 1][2]:
            break
        else:
            nd *= -1
            board[nn - 1].rotate(nd)
        nn -= 1


if __name__ == '__main__':
    board = [[]]
    for _ in range(4):
        board.append(collections.deque(list(map(int, input()))))

    k = int(input())
    for _ in range(k):
        rotate(*map(int, input().split()))

    result = 0
    for i, b in enumerate(board[1:]):
        result += b[0] << i

    print(result)