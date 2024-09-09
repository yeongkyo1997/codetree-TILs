import collections
import sys

# sys.stdin = open('놀이기구 탑승', 'r')


# 학생 배치
def batch():
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    candi = []
    for x in range(N):
        for y in range(N):
            if board[x][y] != 0:
                continue
            cnt = 0
            friendly = 0
            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx < N and 0 <= ny < N:
                    if board[nx][ny] == 0:
                        cnt += 1
                    else:
                        if board[nx][ny] in students[idx]:
                            friendly += 1
            candi.append((-friendly, -cnt, x, y, (x, y)))

    candi.sort()
    x, y = candi[0][-1]
    board[x][y] = idx


def get_score():
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    ret = 0
    for x in range(N):
        for y in range(N):
            cnt = 0
            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx < N and 0 <= ny < N:
                    if board[nx][ny] in students[board[x][y]]:
                        cnt += 1
            ret += score[cnt]
    return ret


if __name__ == '__main__':
    N = int(input())
    board = [[0] * N for _ in range(N)]
    score = [0, 1, 10, 100, 1000]
    students = collections.defaultdict(list)

    for _ in range(N ** 2):
        idx, *friends = list(map(int, input().split()))
        students[idx] = friends
        batch()
    result = get_score()
    print(result)