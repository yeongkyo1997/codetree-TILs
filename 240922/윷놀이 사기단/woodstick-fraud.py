import sys

# sys.stdin = open('윷놀이 사기단', 'r')


def dfs(depth, horses, total):
    global result

    if depth == 10:
        result = max(total, result)
        return

    # 말이 4개이므로
    for i in range(4):
        # 현재 움직일 말
        pos = horses[i]
        # 이미 도착지에 있다면
        if pos == 32:
            continue

        # 현재 갈림길이 아니라면
        if len(path[pos]) == 1:
            pos = path[pos][0]
        else:
            pos = path[pos][1]

        # 남은 칸만큼 움직이기
        for _ in range(dice[depth] - 1):
            pos = path[pos][0]

        # 움직일 말의 위치가 도착지이거나 비어있다면
        if pos == 32 or pos not in horses:
            tmp = horses[:]
            tmp[i] = pos
            dfs(depth + 1, tmp, total + score[pos])


if __name__ == '__main__':
    path = [[1], [2], [3], [4], [5], [6, 21],
            [7], [8], [9], [10], [11, 25],
            [12], [13], [14], [15], [16, 27],
            [17], [18], [19], [20], [32],
            [22], [23], [24], [30],
            [26], [24],
            [28], [29], [24], [31], [20], [32]]

    score = [0, 2, 4, 6, 8, 10,
             12, 14, 16, 18, 20, 22, 24, 26, 28, 30,
             32, 34, 36, 38, 40,
             13, 16, 19, 25,
             22, 24, 28, 27, 26,
             30, 35, 0]

    horses = [0, 0, 0, 0]

    result = 0
    dice = list(map(int, input().split()))

    dfs(0, horses, 0)
    print(result)