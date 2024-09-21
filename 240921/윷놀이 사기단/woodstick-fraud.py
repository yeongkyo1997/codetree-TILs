import sys

# sys.stdin = open('윷놀이 사기단', 'r')


def dfs(depth, horses, total):
    global result
    if depth == 10:
        result = max(result, total)
        return

    for i in range(4):
        # 현재 위치
        cur = horses[i]
        if cur == -1:
            continue

        # 현재 위치가 파란 칸이라면
        if len(path[cur]) == 2:
            # 파란 길로 이동
            cur = path[cur][1]
        else:
            # 빨간 길로 이동
            cur = path[cur][0]

        # 남은 칸만큼 이동
        for _ in range(dice[depth] - 1):
            cur = path[cur][0]

        # 도착했거나 빈 칸이라면
        if cur == 32 or cur not in horses:
            tmp = horses[:]
            tmp[i] = cur

            dfs(depth + 1, tmp, total + score[cur])


if __name__ == '__main__':
    path = {
        0: [1], 1: [2], 2: [3], 3: [4], 4: [5], 5: [6, 21],
        6: [7], 7: [8], 8: [9], 9: [10], 10: [11, 25],
        11: [12], 12: [13], 13: [14], 14: [15], 15: [16, 27],
        16: [17], 17: [18], 18: [19], 19: [20], 20: [32],
        21: [22], 22: [23], 23: [24], 24: [30], 25: [26],
        26: [24], 27: [28], 28: [29], 29: [24], 30: [31],
        31: [20], 32: [32]
    }
    score = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 10,
             6: 12, 7: 14, 8: 16, 9: 18, 10: 20,
             11: 22, 12: 24, 13: 26, 14: 28, 15: 30,
             16: 32, 17: 34, 18: 36, 19: 38, 20: 40,
             21: 13, 22: 16, 23: 19, 24: 25, 25: 22,
             26: 24, 27: 28, 28: 27, 29: 26, 30: 30,
             31: 35, 32: 0
             }

    dice = list(map(int, input().split()))

    horses = [0, 0, 0, 0]
    result = 0

    dfs(0, horses, 0)
    print(result)