import heapq
from collections import deque


class Node:
    def __init__(self, x, y, dist):
        self.x = x
        self.y = y
        self.dist = dist


class Visual:
    def __init__(self, map_, d, warrior_cnt):
        self.map = map_
        self.d = d
        self.warrior_cnt = warrior_cnt


class Warrior:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True
        self.can_move = True

    def move(self, medusa):
        global warrior_map, visual_map
        if not self.can_move or not self.is_alive:
            return 0

        moved_dist = 0

        # 두 번의 이동 시도
        for move_cnt in range(2):
            if move_cnt == 0:
                # 첫 번째 이동: 상, 하, 좌, 우 순으로 메두사와의 거리를 줄일 수 있는 방향으로 이동
                for dx, dy in dir:
                    nx, ny = self.x + dx, self.y + dy
                    if is_out_of_range(nx, ny) or visual_map[nx][ny] == 1:
                        continue

                    cur_dist = get_dist(self.x, self.y, medusa.x, medusa.y)
                    next_dist = get_dist(nx, ny, medusa.x, medusa.y)

                    if next_dist < cur_dist:
                        warrior_map[self.x][self.y] -= 1
                        warrior_map[nx][ny] += 1
                        self.x = nx
                        self.y = ny
                        moved_dist += 1
                        break
                continue

            # 두 번째 이동: 좌, 우, 상, 하 순으로 메두사와의 거리를 줄일 수 있는 방향으로 이동
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = self.x + dx, self.y + dy
                if is_out_of_range(nx, ny) or visual_map[nx][ny] == 1:
                    continue

                cur_dist = get_dist(self.x, self.y, medusa.x, medusa.y)
                next_dist = get_dist(nx, ny, medusa.x, medusa.y)

                if next_dist < cur_dist:
                    warrior_map[self.x][self.y] -= 1
                    warrior_map[nx][ny] += 1
                    self.x = nx
                    self.y = ny
                    moved_dist += 1
                    break

        return moved_dist

    def attack_medusa(self):
        global warrior_map
        self.is_alive = False
        warrior_map[self.x][self.y] -= 1


class Medusa:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_arrived = False

    def move(self, dist_map):
        global warrior_map
        direction = self.get_direction(dist_map)
        dx, dy = dir[direction]
        self.x += dx
        self.y += dy

        if warrior_map[self.x][self.y] > 0:
            self.kill_warrior()

        if self.x == Er and self.y == Ec:
            self.is_arrived = True

    def get_direction(self, dist_map):
        heap = []
        for i, (dx, dy) in enumerate(dir):
            nx, ny = self.x + dx, self.y + dy
            if is_out_of_range(nx, ny):
                continue
            if dist_map[nx][ny] == 1_000_000_000:
                continue
            heapq.heappush(heap, (dist_map[nx][ny], i))

        if not heap:
            return 0  # 유효한 이동이 없을 경우 기본 방향 반환

        return heapq.heappop(heap)[1]

    def see_warriors(self):
        global visual_map
        picked_visual = self.pick_visual_case()
        visual_map = picked_visual.map
        self.bind_warrior()
        return picked_visual.warrior_cnt

    def pick_visual_case(self):
        # 모든 네 방향을 평가하고 가장 좋은 방향 선택
        see_up = self.see_up()
        see_down = self.see_down()
        see_left = self.see_left()
        see_right = self.see_right()

        heap = []
        heapq.heappush(heap, (-see_up.warrior_cnt, see_up.d, see_up))
        heapq.heappush(heap, (-see_down.warrior_cnt, see_down.d, see_down))
        heapq.heappush(heap, (-see_left.warrior_cnt, see_left.d, see_left))
        heapq.heappush(heap, (-see_right.warrior_cnt, see_right.d, see_right))

        return heapq.heappop(heap)[2]

    def see_up(self):
        visual_case_map = [[0] * N for _ in range(N)]
        warrior_cnt = 0
        stage = 1

        for x in range(self.x - 1, -1, -1):
            for y in range(self.y - stage, self.y + stage + 1):
                if is_out_of_range(x, y):
                    continue
                if visual_case_map[x][y] in [1, -1]:
                    continue

                if warrior_map[x][y] > 0 and visual_case_map[x][y] == 0:
                    warrior_cnt += warrior_map[x][y]
                    visual_case_map[x][y] = 1
                    self.fill_shade_up(visual_case_map, x, y)
                elif visual_case_map[x][y] == 0:
                    visual_case_map[x][y] = 1
            stage += 1

        return Visual(visual_case_map, 0, warrior_cnt)

    def see_down(self):
        visual_case_map = [[0] * N for _ in range(N)]
        warrior_cnt = 0
        stage = 1

        for x in range(self.x + 1, N):
            for y in range(self.y - stage, self.y + stage + 1):
                if is_out_of_range(x, y):
                    continue
                if visual_case_map[x][y] in [1, -1]:
                    continue

                if warrior_map[x][y] > 0 and visual_case_map[x][y] == 0:
                    warrior_cnt += warrior_map[x][y]
                    visual_case_map[x][y] = 1
                    self.fill_shade_down(visual_case_map, x, y)
                elif visual_case_map[x][y] == 0:
                    visual_case_map[x][y] = 1
            stage += 1

        return Visual(visual_case_map, 1, warrior_cnt)

    def see_left(self):
        visual_case_map = [[0] * N for _ in range(N)]
        warrior_cnt = 0
        stage = 1

        for y in range(self.y - 1, -1, -1):
            for x in range(self.x - stage, self.x + stage + 1):
                if is_out_of_range(x, y):
                    continue
                if visual_case_map[x][y] in [1, -1]:
                    continue

                if warrior_map[x][y] > 0 and visual_case_map[x][y] == 0:
                    warrior_cnt += warrior_map[x][y]
                    visual_case_map[x][y] = 1
                    self.fill_shade_left(visual_case_map, x, y)
                elif visual_case_map[x][y] == 0:
                    visual_case_map[x][y] = 1
            stage += 1

        return Visual(visual_case_map, 2, warrior_cnt)

    def see_right(self):
        visual_case_map = [[0] * N for _ in range(N)]
        warrior_cnt = 0
        stage = 1

        for y in range(self.y + 1, N):
            for x in range(self.x - stage, self.x + stage + 1):
                if is_out_of_range(x, y):
                    continue
                if visual_case_map[x][y] in [1, -1]:
                    continue

                if warrior_map[x][y] > 0 and visual_case_map[x][y] == 0:
                    warrior_cnt += warrior_map[x][y]
                    visual_case_map[x][y] = 1
                    self.fill_shade_right(visual_case_map, x, y)
                elif visual_case_map[x][y] == 0:
                    visual_case_map[x][y] = 1
            stage += 1

        return Visual(visual_case_map, 3, warrior_cnt)

    def fill_shade_up(self, visual_case_map, wx, wy):
        if wy == self.y:
            # 전사와 메두사가 일직선 상에 있는 경우
            for x in range(wx - 1, -1, -1):
                if visual_case_map[x][wy] == 0:
                    visual_case_map[x][wy] = -1
            return

        if wy < self.y:
            # 전사가 메두사보다 왼쪽에 있는 경우
            stage = 1
            for x in range(wx - 1, -1, -1):
                for y in range(wy - stage, wy + 1):
                    tx, ty = x, y
                    if ty < 0:
                        ty = 0
                    if visual_case_map[tx][ty] == 0:
                        visual_case_map[tx][ty] = -1
                stage += 1
            return

        # wy > self.y: 전사가 메두사보다 오른쪽에 있는 경우
        stage = 1
        for x in range(wx - 1, -1, -1):
            for y in range(wy, wy + stage + 1):
                tx = x
                ty = y
                if ty >= N:
                    ty = N - 1
                if visual_case_map[tx][ty] == 0:
                    visual_case_map[tx][ty] = -1
            stage += 1

    def fill_shade_down(self, visual_case_map, wx, wy):
        if wy == self.y:
            # 전사와 메두사가 일직선 상에 있는 경우
            for x in range(wx + 1, N):
                if visual_case_map[x][wy] == 0:
                    visual_case_map[x][wy] = -1
            return

        if wy < self.y:
            # 전사가 메두사보다 왼쪽에 있는 경우
            stage = 1
            for x in range(wx + 1, N):
                for y in range(wy - stage, wy + 1):
                    tx, ty = x, y
                    if ty < 0:
                        ty = 0
                    if visual_case_map[tx][ty] == 0:
                        visual_case_map[tx][ty] = -1
                stage += 1
            return

        # wy > self.y: 전사가 메두사보다 오른쪽에 있는 경우
        stage = 1
        for x in range(wx + 1, N):
            for y in range(wy, wy + stage + 1):
                tx = x
                ty = y
                if ty >= N:
                    ty = N - 1
                if visual_case_map[tx][ty] == 0:
                    visual_case_map[tx][ty] = -1
            stage += 1

    def fill_shade_left(self, visual_case_map, wx, wy):
        if wx == self.x:
            # 전사와 메두사가 일직선 상에 있는 경우
            for y in range(wy - 1, -1, -1):
                if visual_case_map[wx][y] == 0:
                    visual_case_map[wx][y] = -1
            return

        if wx < self.x:
            # 전사가 메두사보다 위에 있는 경우
            stage = 1
            for y in range(wy - 1, -1, -1):
                for x in range(wx, wx - stage - 1, -1):
                    tx, ty = x, y
                    if tx < 0:
                        tx = 0
                    if visual_case_map[tx][ty] == 0:
                        visual_case_map[tx][ty] = -1
                stage += 1
            return

        # wx > self.x: 전사가 메두사보다 아래에 있는 경우
        stage = 1
        for y in range(wy - 1, -1, -1):
            for x in range(wx, wx + stage + 1):
                tx, ty = x, y
                if tx >= N:
                    tx = N - 1
                if visual_case_map[tx][ty] == 0:
                    visual_case_map[tx][ty] = -1
            stage += 1

    def fill_shade_right(self, visual_case_map, wx, wy):
        if wx == self.x:
            # 전사와 메두사가 일직선 상에 있는 경우
            for y in range(wy + 1, N):
                if visual_case_map[wx][y] == 0:
                    visual_case_map[wx][y] = -1
            return

        if wx < self.x:
            # 전사가 메두사보다 위에 있는 경우
            stage = 1
            for y in range(wy + 1, N):
                for x in range(wx, wx - stage - 1, -1):
                    tx, ty = x, y
                    if tx < 0:
                        tx = 0
                    if visual_case_map[tx][ty] == 0:
                        visual_case_map[tx][ty] = -1
                stage += 1
            return

        # wx > self.x: 전사가 메두사보다 아래에 있는 경우
        stage = 1
        for y in range(wy + 1, N):
            for x in range(wx, wx + stage + 1):
                tx, ty = x, y
                if tx >= N:
                    tx = N - 1
                if visual_case_map[tx][ty] == 0:
                    visual_case_map[tx][ty] = -1
            stage += 1

    def kill_warrior(self):
        global warriors, warrior_map
        tx, ty = self.x, self.y
        for warrior in warriors:
            if warrior_map[tx][ty] == 0:
                break
            if warrior.x == tx and warrior.y == ty and warrior.is_alive:
                warrior.attack_medusa()
                break

    def bind_warrior(self):
        global warriors, visual_map
        for warrior in warriors:
            if warrior.is_alive and visual_map[warrior.x][warrior.y] == 1:
                warrior.can_move = False


def get_dist_map(tile_map):
    INF = 1_000_000_000
    dist_map = [[INF] * N for _ in range(N)]
    visited = [[False] * N for _ in range(N)]
    q = deque()
    q.append(Node(Er, Ec, 0))
    visited[Er][Ec] = True
    dist_map[Er][Ec] = 0

    while q:
        cur = q.popleft()
        for dx, dy in dir:
            nx = cur.x + dx
            ny = cur.y + dy
            if is_out_of_range(nx, ny):
                continue
            if visited[nx][ny]:
                continue
            if tile_map[nx][ny] == 1:
                dist_map[nx][ny] = 1_000_000_000
                continue
            visited[nx][ny] = True
            dist_map[nx][ny] = cur.dist + 1
            q.append(Node(nx, ny, dist_map[nx][ny]))

    return dist_map


def get_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def is_out_of_range(x, y):
    return x < 0 or y < 0 or x >= N or y >= N


def is_on_medusa(warrior, medusa):
    return warrior.x == medusa.x and warrior.y == medusa.y


def reset_warriors_status():
    global warriors
    for warrior in warriors:
        if warrior.is_alive and not warrior.can_move:
            warrior.can_move = True


if __name__ == "__main__":
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 첫 번째 줄: N (그리드 크기), M (전사의 수)
    N, M = map(int, input().split())

    # 그리드 초기화
    warrior_map = [[0] * N for _ in range(N)]
    visual_map = [[0] * N for _ in range(N)]

    # 두 번째 줄: 메두사의 시작 위치(mx, my)와 도착 지점(arrX, arrY)
    Sr, Sc, Er, Ec = map(int, input().split())

    medusa = Medusa(Sr, Sc)

    warriors = []
    # 전사들의 위치 입력
    it = iter(map(int, input().split()))
    for _ in range(M):
        x, y = next(it), next(it)
        warrior_map[x][y] += 1
        warriors.append(Warrior(x, y))

    board = [list(map(int, input().split())) for _ in range(N)]

    # 거리 맵 생성
    dist_map = get_dist_map(board)

    # 메두사가 도착 지점에 도달할 수 없는 경우
    if dist_map[medusa.x][medusa.y] == 0 and (medusa.x != Er or medusa.y != Ec):
        print(-1)
    else:
        results = []

        # 메두사가 도착할 때까지 시뮬레이션 반복
        while not medusa.is_arrived:
            warrior_moved_dist = 0
            attacked_warriors = 0

            # 1. 메두사 이동
            medusa.move(dist_map)

            # 2. 메두사가 전사를 시야로 인식
            bound_warriors = medusa.see_warriors()

            # 3. 전사들이 이동
            for warrior in warriors:
                if not warrior.is_alive:
                    continue
                moved = warrior.move(medusa)
                warrior_moved_dist += moved
                if is_on_medusa(warrior, medusa):
                    warrior.attack_medusa()
                    attacked_warriors += 1

            # 4. 점수 기록
            if medusa.is_arrived:
                results.append("0")
            else:
                results.append(f"{warrior_moved_dist} {bound_warriors} {attacked_warriors}")

            # 5. 시야 맵과 전사 상태 리셋
            visual_map = [[0] * N for _ in range(N)]
            reset_warriors_status()

        print("\n".join(results))