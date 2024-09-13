import heapq


class Rabbit:
    def __init__(self, pid, d):
        self.pid = pid
        self.d = d
        self.r = 1
        self.c = 1
        self.jumps = 0
        self.score = 0
        self.last_selected = False


def race(N, M, rabbits, K, S):
    for _ in range(K):
        # 우선순위가 가장 높은 토끼 선택
        selected = min(rabbits, key=lambda x: (x.jumps, x.r + x.c, x.r, x.c, x.pid))
        selected.jumps += 1
        selected.last_selected = True

        # 4방향 이동 계산
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        best_pos = (1, 1)
        best_sum = 0

        for dr, dc in directions:
            r, c = selected.r, selected.c
            dist = selected.d
            while dist > 0:
                if 1 <= r + dr <= N and 1 <= c + dc <= M:
                    r += dr
                    c += dc
                else:
                    dr, dc = -dr, -dc
                    r += dr
                    c += dc
                dist -= 1
            if r + c > best_sum or (r + c == best_sum and r > best_pos[0]):
                best_sum = r + c
                best_pos = (r, c)

        # 선택된 토끼 이동
        selected.r, selected.c = best_pos

        # 다른 토끼들 점수 획득
        for rabbit in rabbits:
            if rabbit != selected:
                rabbit.score += selected.r + selected.c

    # K번의 턴 이후 추가 점수 부여
    best_rabbit = max((r for r in rabbits if r.last_selected),
                      key=lambda x: (x.r + x.c, x.r, x.c, x.pid))
    best_rabbit.score += S


def change_distance(rabbits, pid_t, L):
    for rabbit in rabbits:
        if rabbit.pid == pid_t:
            rabbit.d *= L
            break


def main():
    Q = int(input())
    rabbits = []

    for _ in range(Q):
        command = list(map(int, input().split()))

        if command[0] == 100:
            N, M, P = command[1:4]
            rabbits = [Rabbit(command[i], command[i + 1]) for i in range(4, len(command), 2)]

        elif command[0] == 200:
            K, S = command[1:]
            race(N, M, rabbits, K, S)

        elif command[0] == 300:
            pid_t, L = command[1:]
            change_distance(rabbits, pid_t, L)

        elif command[0] == 400:
            print(max(rabbit.score for rabbit in rabbits))


if __name__ == "__main__":
    main()