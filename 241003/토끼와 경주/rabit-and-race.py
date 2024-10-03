import heapq
import sys
from collections import defaultdict

input = lambda: sys.stdin.readline().rstrip()



class Rabbit:
    def __init__(self, pid, d):
        self.pid = pid
        self.d = d
        self.x = 1  # 1-based
        self.y = 1
        self.jump = 0

    def get_priority(self):
        return self.jump, self.x + self.y, self.x, self.y, self.pid


def calc(x, y, d, dx, dy, N, M):
    if dx != 0:  # 행 방향 이동
        period = 2 * (N - 1)
        nx = x - 1 + dx * d
        nx %= period
        nx = min(nx, period - nx)
        nx += 1
    else:
        nx = x

    if dy != 0:  # 열 방향 이동
        period = 2 * (M - 1)
        ny = y - 1 + dy * d
        ny %= period
        ny = min(ny, period - ny)
        ny += 1
    else:
        ny = y

    return nx, ny


def main():
    Q = int(input())  # 명령어 수
    idx = 1

    rabbits = {}
    heap = []
    scores = defaultdict(int)
    selected_rabbits = set()
    N, M = 0, 0

    for _ in range(Q):
        q, *data = map(int, input().split())
        idx += 1

        if q == 100:
            N, M, P, *data = data
            for i in range(P):
                pid, d = data[i * 2], data[i * 2 + 1]
                rabbit = Rabbit(pid, d)
                rabbits[pid] = rabbit
                heapq.heappush(heap, (rabbit.get_priority(), pid))

        elif q == 200:
            K, S = data
            r_best = []

            for _ in range(K):
                if not heap:
                    break
                _, pid = heapq.heappop(heap)
                rabbit = rabbits[pid]
                selected_rabbits.add(pid)

                # 4방향으로 이동한 후의 후보 위치 계산
                candidates = []
                directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                for dx, dy in directions:
                    final_x, final_y = calc(rabbit.x, rabbit.y, rabbit.d, dx, dy, N, M)
                    candidates.append((-(final_x + final_y), -final_x, -final_y, final_x, final_y))

                # 다음 이동 위치 결정
                candidates.sort()
                _, _, _, final_x, final_y = candidates[0]

                # 토끼의 위치와 점프 횟수 업데이트
                rabbit.x, rabbit.y = final_x, final_y
                rabbit.jump += 1

                # 힙에 다시 삽입 (변경된 우선순위 반영)
                heapq.heappush(heap, (rabbit.get_priority(), pid))

                # 현재 토끼를 제외한 모든 토끼의 점수 갱신
                score_increment = final_x + final_y
                for other_pid in rabbits:
                    if other_pid != pid:
                        scores[other_pid] += score_increment

                # 현재 이동한 토끼의 정보를 베스트 토끼 후보로 저장
                r_best.append((-(final_x + final_y), -final_x, -final_y, -pid, pid))

            # K번의 이동 후 베스트 토끼 점수 업데이트
            if r_best:
                r_best.sort()
                best_pid = r_best[0][4]
                scores[best_pid] += S

        elif q == 300:
            pid_t, L = data
            if pid_t in rabbits:
                rabbits[pid_t].d *= L

        elif q == 400:
            # Find the maximum score among all rabbits
            max_score = max(scores.values()) if scores else 0
            print(max_score)


if __name__ == "__main__":
    main()