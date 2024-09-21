import sys

# sys.stdin = open('윷놀이 사기단', 'r')



def dfs(depth, horses, total):
    global result

    if depth == 10:
        result = max(result, total)
        return
    for i in range(4):
        # 현재 말의 위치
        cur = horses[i]

        # 갈림길이라면
        if len(path[cur]) == 2:
            # 빨간 길로 한칸 이동
            cur = path[cur][1]
        else:
            # 파란 길로 한칸 이동
            cur = path[cur][0]

        # 이동
        for _ in range(dice[depth] - 1):
            cur = path[cur][0]

        # 도착했거나 다른 말이 없다면
        if cur == 32 or cur not in horses:
            # 말 위치 갱신
            tmp = horses[:]
            tmp[i] = cur

            dfs(depth + 1, tmp, total + score[cur])


if __name__ == '__main__':
    path = [[1], [2], [3], [4], [5],
            [6, 21], [7], [8], [9], [10],
            [11, 25], [12], [13], [14], [15],
            [16, 27], [17], [18], [19], [20],
            [32], [22], [23], [24], [30],
            [26], [24], [28], [29], [24],
            [31], [20], [32]]
    score = [0, 2, 4, 6, 8,
             10, 12, 14, 16, 18,
             20, 22, 24, 26, 28,
             30, 32, 34, 36, 38,
             40, 13, 16, 19, 25,
             22, 24, 28, 27, 26,
             30, 35, 0]

    # 현재 좌표
    cur = 0
    result = 0

    # 주사위
    dice = list(map(int, input().split()))
    dfs(0, [0, 0, 0, 0], 0)
    print(result)