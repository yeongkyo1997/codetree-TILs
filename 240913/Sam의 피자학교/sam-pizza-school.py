import sys
from collections import deque

# sys.stdin = open('Sam의 피자학교', 'r')


def rotate90(mat):
    tmp = [[0] * len(mat) for _ in range(len(mat[0]))]

    for y in range(len(mat)):
        for x in range(len(mat[0])):
            tmp[x][len(mat) - y - 1] = mat[y][x]
    return tmp


def add_one(lst):
    min_n = 999999
    for i in range(len(lst)):
        if lst[i] < min_n:
            min_n = lst[i]

    for i in range(len(lst)):
        if lst[i] == min_n:
            lst[i] += 1
    return lst


def rolling(lst):
    mat = [[lst[0]], [lst[1]]]
    remain = deque(lst[2:])

    while len(mat) <= len(remain):  # 도우 말 수 있는 만큼
        n_row = len(mat)  # 1자형 도우에서 접혀야 하는 개수
        mat = rotate90(mat)

        tmp = [remain.popleft() for _ in range(n_row)]  # 1자형 도우에서 접힐 부분
        mat.append(tmp)

    return mat, list(remain)  # 직사각형 모양으로 접힌 부분과 나머지 부분


def push_dough(mat, remain):
    tmp_mat = [[0] * len(x) for x in mat]  # 원래 도우와 같은 크기 빈 도우 생성
    if remain:  # 안 접힌 부분 남아있으면?
        tmp_remain = [0] * (len(remain))
    else:
        tmp_remain = []

    for y in range(len(mat)):
        for x in range(len(mat[y])):
            for i in range(2):  # 중복 막기 위해 우/하 방향만 체크
                new_y, new_x = y + dir[i][1], x + dir[i][0]
                if 0 <= new_y < len(mat) and 0 <= new_x < len(mat[y]):  # 안쪽이면
                    d = abs(mat[y][x] - mat[new_y][new_x]) // 5
                    if mat[y][x] > mat[new_y][new_x]:  # 큰 쪽에서 작은쪽으로 d만큼
                        tmp_mat[y][x] -= d
                        tmp_mat[new_y][new_x] += d
                    else:
                        tmp_mat[y][x] += d
                        tmp_mat[new_y][new_x] -= d
    if remain:  # 안 접힌 부분이 있다면
        d = abs(mat[-1][-1] - remain[0]) // 5
        if mat[-1][-1] > remain[0]:
            tmp_mat[-1][-1] -= d
            tmp_remain[0] += d
        else:
            tmp_mat[-1][-1] += d
            tmp_remain[0] -= d
        for x in range(len(remain) - 1):
            d = abs(remain[x] - remain[x + 1]) // 5
            if remain[x] > remain[x + 1]:
                tmp_remain[x] -= d
                tmp_remain[x + 1] += d
            else:
                tmp_remain[x] += d
                tmp_remain[x + 1] -= d

    for y in range(len(mat)):
        for x in range(len(mat[y])):
            tmp_mat[y][x] += mat[y][x]
    if remain:
        for x in range(len(remain)):
            tmp_remain[x] += remain[x]

    return tmp_mat, tmp_remain


def flatten(mat, remain):
    lst = []

    for x in range(len(mat[0])):
        for y in range(len(mat) - 1, -1, -1):
            lst.append(mat[y][x])
    lst += remain  # 안 접힌 부분 붙여주기
    return lst


def rolling_twice(lst):
    n = len(lst) // 4
    lst = deque(lst)
    a = [lst.popleft() for _ in range(n)]
    b = [lst.popleft() for _ in range(n)]
    c = [lst.popleft() for _ in range(n)]
    d = [lst.popleft() for _ in range(n)]

    a.reverse()
    c.reverse()

    return [c, b, a, d]


def check(lst, k):
    return max(lst) - min(lst) <= k


if __name__ == "__main__":
    n, k = map(int, input().split())
    lst = list(map(int, input().split()))
    dir = [[0, 1], [1, 0]]

    sol = 0
    while True:
        sol += 1
        lst = add_one(lst)  # 가장 작은 곳 1 더하기
        mat, lst = rolling(lst)  # 말기
        mat, lst = push_dough(mat, lst)  # 도우 누르기
        lst = flatten(mat, lst)  # 평평하게 만들기
        mat = rolling_twice(lst)  # 다른 방법으로 말기
        mat, lst = push_dough(mat, [])  # 도우 누르기
        lst = flatten(mat, lst)  # 평평하게 만들기

        if check(lst, k):  # k 이하 체크
            print(sol)
            break