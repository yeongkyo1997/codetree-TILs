import heapq
from collections import deque


def main():
    global N, er, ec, warriors, warrior_map, sight_map, dx, dy
    N, M = map(int, input().split())
    tile_map = [[0] * N for _ in range(N)]
    warrior_map = [[0] * N for _ in range(N)]
    sight_map = [[0] * N for _ in range(N)]

    sr, sc, er, ec = map(int, input().split())
    medusa = Medusa(sr, sc)

    warrior_pos = list(map(int, input().split()))
    warriors = []
    for i in range(0, len(warrior_pos), 2):
        x = warrior_pos[i]
        y = warrior_pos[i + 1]
        warrior_map[x][y] += 1
        warriors.append(Warrior(x, y))

    for i in range(N):
        tile_map[i] = list(map(int, input().split()))

    dist_map = get_dist_map(tile_map)
    if dist_map[medusa.x][medusa.y] == 0 and (medusa.x != er or medusa.y != ec):
        print(-1)
        return

    results = []
    while not medusa.is_arrived:
        warrior_moved_dist = 0
        attacked_warriors = 0

        medusa.move(dist_map)
        bound_warriors = medusa.see_warriors()
        for warrior in warriors:
            if not warrior.is_alive:
                continue
            warrior_moved_dist += warrior.move(medusa)
            if is_on_medusa(warrior, medusa):
                warrior.attack_medusa()
                attacked_warriors += 1

        if medusa.is_arrived:
            results.append("0")
        else:
            results.append(f"{warrior_moved_dist} {bound_warriors} {attacked_warriors}")

        sight_map = [[0] * N for _ in range(N)]
        reset_warriors_status(warriors)

    print('\n'.join(results))


def is_out_of_range(x, y):
    return x < 0 or y < 0 or x >= N or y >= N


def get_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def is_on_medusa(warrior, medusa):
    return warrior.x == medusa.x and warrior.y == medusa.y


def reset_warriors_status(warriors):
    for warrior in warriors:
        if warrior.is_alive and not warrior.can_move:
            warrior.can_move = True


def get_dist_map(tileMap):
    INF = 1_000_000_000
    dist_map = [[0] * N for _ in range(N)]
    visited = [[False] * N for _ in range(N)]
    q = deque()
    q.append(Node(er, ec, 0))
    visited[er][ec] = True
    while q:
        cur = q.popleft()
        for i in range(4):
            nx = cur.x + dx[i]
            ny = cur.y + dy[i]
            if is_out_of_range(nx, ny):
                continue
            if visited[nx][ny]:
                continue
            if tileMap[nx][ny] == 1:
                dist_map[nx][ny] = INF
                continue
            visited[nx][ny] = True
            dist_map[nx][ny] = cur.dist + 1
            q.append(Node(nx, ny, dist_map[nx][ny]))
    return dist_map


class Node:
    def __init__(self, x, y, dist):
        self.x = x
        self.y = y
        self.dist = dist


class Medusa:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_arrived = False

    def move(self, distMap):
        global warrior_map, er, ec, dx, dy
        dir = self.get_dir(distMap)
        self.x += dx[dir]
        self.y += dy[dir]
        if warrior_map[self.x][self.y] > 0:
            self.kill_warrior()
        if self.x == er and self.y == ec:
            self.is_arrived = True

    def get_dir(self, distMap):
        hq = []
        for i in range(4):
            nx = self.x + dx[i]
            ny = self.y + dy[i]
            if is_out_of_range(nx, ny):
                continue
            if distMap[nx][ny] == 1_000_000_000:
                continue
            heapq.heappush(hq, (distMap[nx][ny], i))
        if hq:
            _, dir = heapq.heappop(hq)
            return dir
        else:
            return 0

    def kill_warrior(self):
        global warrior_map, warriors
        tx = self.x
        ty = self.y
        for warrior in warriors:
            if warrior_map[tx][ty] == 0:
                break
            if warrior.x == tx and warrior.y == ty:
                warrior.is_alive = False
                warrior_map[tx][ty] -= 1

    def see_warriors(self):
        picked_sight = self.pick_sight_case()
        global sight_map
        sight_map = picked_sight.map
        self.bind_warrior()
        return picked_sight.warrior_cnt

    def pick_sight_case(self):
        sight_cases = []
        sight_cases.append(self.see_up())
        sight_cases.append(self.see_down())
        sight_cases.append(self.see_left())
        sight_cases.append(self.see_right())
        sight_cases.sort(key=lambda s: (-s.warrior_cnt, s.dir))
        return sight_cases[0]

    def bind_warrior(self):
        global warriors, sight_map
        for warrior in warriors:
            if sight_map[warrior.x][warrior.y] == 1:
                warrior.can_move = False

    def see_up(self):
        global N, warrior_map
        sight_case_map = [[0] * N for _ in range(N)]
        warrior_cnt = 0
        stage = 1
        x = self.x - 1
        while x > -1:
            for y in range(self.y - stage, self.y + stage + 1):
                if is_out_of_range(x, y):
                    continue
                if sight_case_map[x][y] == 1 or sight_case_map[x][y] == -1:
                    continue
                if warrior_map[x][y] > 0 and sight_case_map[x][y] == 0:
                    warrior_cnt += warrior_map[x][y]
                    sight_case_map[x][y] = 1
                    self.fill_shade_up(sight_case_map, x, y)
                elif sight_case_map[x][y] == 0:
                    sight_case_map[x][y] = 1
            stage += 1
            x -= 1
        return Sight(sight_case_map, 0, warrior_cnt)

    def see_down(self):
        global N, warrior_map
        sight_case_map = [[0] * N for _ in range(N)]
        warrior_cnt = 0
        stage = 1
        x = self.x + 1
        while x < N:
            for y in range(self.y - stage, self.y + stage + 1):
                if is_out_of_range(x, y):
                    continue
                if sight_case_map[x][y] == 1 or sight_case_map[x][y] == -1:
                    continue
                if warrior_map[x][y] > 0 and sight_case_map[x][y] == 0:
                    warrior_cnt += warrior_map[x][y]
                    sight_case_map[x][y] = 1
                    self.fill_shade_down(sight_case_map, x, y)
                elif sight_case_map[x][y] == 0:
                    sight_case_map[x][y] = 1
            stage += 1
            x += 1
        return Sight(sight_case_map, 1, warrior_cnt)

    def see_left(self):
        global N, warrior_map
        sight_case_map = [[0] * N for _ in range(N)]
        warrior_cnt = 0
        stage = 1
        y = self.y - 1
        while y > -1:
            for x in range(self.x - stage, self.x + stage + 1):
                if is_out_of_range(x, y):
                    continue
                if sight_case_map[x][y] == 1 or sight_case_map[x][y] == -1:
                    continue
                if warrior_map[x][y] > 0 and sight_case_map[x][y] == 0:
                    warrior_cnt += warrior_map[x][y]
                    sight_case_map[x][y] = 1
                    self.fill_shade_left(sight_case_map, x, y)
                elif sight_case_map[x][y] == 0:
                    sight_case_map[x][y] = 1
            stage += 1
            y -= 1
        return Sight(sight_case_map, 2, warrior_cnt)

    def see_right(self):
        global N, warrior_map
        sight_case_map = [[0] * N for _ in range(N)]
        warrior_cnt = 0
        stage = 1
        y = self.y + 1
        while y < N:
            for x in range(self.x - stage, self.x + stage + 1):
                if is_out_of_range(x, y):
                    continue
                if sight_case_map[x][y] == 1 or sight_case_map[x][y] == -1:
                    continue
                if warrior_map[x][y] > 0 and sight_case_map[x][y] == 0:
                    warrior_cnt += warrior_map[x][y]
                    sight_case_map[x][y] = 1
                    self.fill_shade_right(sight_case_map, x, y)
                elif sight_case_map[x][y] == 0:
                    sight_case_map[x][y] = 1
            stage += 1
            y += 1
        return Sight(sight_case_map, 3, warrior_cnt)

    def fill_shade_up(self, sight_case_map, wx, wy):
        global N
        if wy == self.y:
            for x in range(wx - 1, -1, -1):
                if sight_case_map[x][wy] == 0:
                    sight_case_map[x][wy] = -1
            return

        if wy < self.y:
            stage = 1
            for x in range(wx - 1, -1, -1):
                for y in range(wy - stage, wy + 1):
                    tx = x
                    ty = y
                    if ty < 0:
                        ty = 0
                    if sight_case_map[tx][ty] == 0:
                        sight_case_map[tx][ty] = -1
                stage += 1
            return

        # wy > self.y
        stage = 1
        for x in range(wx - 1, -1, -1):
            for y in range(wy, wy + stage + 1):
                tx = x
                ty = y
                if ty >= N:
                    ty = N - 1
                if sight_case_map[tx][ty] == 0:
                    sight_case_map[tx][ty] = -1
            stage += 1

    def fill_shade_down(self, sight_case_map, wx, wy):
        global N
        if wy == self.y:
            for x in range(wx + 1, N):
                if sight_case_map[x][wy] == 0:
                    sight_case_map[x][wy] = -1
            return

        if wy < self.y:
            stage = 1
            for x in range(wx + 1, N):
                for y in range(wy - stage, wy + 1):
                    tx = x
                    ty = y
                    if ty < 0:
                        ty = 0
                    if sight_case_map[tx][ty] == 0:
                        sight_case_map[tx][ty] = -1
                stage += 1
            return

        # wy > self.y
        stage = 1
        for x in range(wx + 1, N):
            for y in range(wy, wy + stage + 1):
                tx = x
                ty = y
                if ty >= N:
                    ty = N - 1
                if sight_case_map[tx][ty] == 0:
                    sight_case_map[tx][ty] = -1
            stage += 1

    def fill_shade_left(self, sight_case_map, wx, wy):
        global N
        if wx == self.x:
            for y in range(wy - 1, -1, -1):
                if sight_case_map[wx][y] == 0:
                    sight_case_map[wx][y] = -1
            return

        if wx < self.x:
            stage = 1
            for y in range(wy - 1, -1, -1):
                for x in range(wx - stage, wx + 1):
                    tx = x
                    ty = y
                    if tx < 0:
                        tx = 0
                    if sight_case_map[tx][ty] == 0:
                        sight_case_map[tx][ty] = -1
                stage += 1
            return

        # wx > self.x
        stage = 1
        for y in range(wy - 1, -1, -1):
            for x in range(wx, wx + stage + 1):
                tx = x
                ty = y
                if tx >= N:
                    tx = N - 1
                if sight_case_map[tx][ty] == 0:
                    sight_case_map[tx][ty] = -1
            stage += 1

    def fill_shade_right(self, sight_case_map, wx, wy):
        global N
        if wx == self.x:
            for y in range(wy + 1, N):
                if sight_case_map[wx][y] == 0:
                    sight_case_map[wx][y] = -1
            return

        if wx < self.x:
            stage = 1
            for y in range(wy + 1, N):
                for x in range(wx - stage, wx + 1):
                    tx = x
                    ty = y
                    if tx < 0:
                        tx = 0
                    if sight_case_map[tx][ty] == 0:
                        sight_case_map[tx][ty] = -1
                stage += 1
            return

        # wx > self.x
        stage = 1
        for y in range(wy + 1, N):
            for x in range(wx, wx + stage + 1):
                tx = x
                ty = y
                if tx >= N:
                    tx = N - 1
                if sight_case_map[tx][ty] == 0:
                    sight_case_map[tx][ty] = -1
            stage += 1


class Sight:
    def __init__(self, map_, dir, warrior_cnt):
        self.map = map_
        self.dir = dir
        self.warrior_cnt = warrior_cnt


class Warrior:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True
        self.can_move = True

    def move(self, medusa):
        global warrior_map, sight_map
        if not self.can_move or not self.is_alive:
            return 0
        moved_dist = 0

        for move_cnt in range(2):
            if move_cnt == 0:
                for i in range(4):
                    nx = self.x + dx[i]
                    ny = self.y + dy[i]
                    if is_out_of_range(nx, ny) or sight_map[nx][ny] == 1:
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
            dx2 = [0, 0, -1, 1]
            dy2 = [-1, 1, 0, 0]
            for i in range(4):
                nx = self.x + dx2[i]
                ny = self.y + dy2[i]
                if is_out_of_range(nx, ny) or sight_map[nx][ny] == 1:
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


dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

if __name__ == '__main__':
    main()