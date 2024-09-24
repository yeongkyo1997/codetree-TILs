import collections
import copy
import sys

# sys.stdin = open('왕실의 기사 대결', 'r')


# 움직일 기사들 찾기
def find_knights(idx, d):
    def bfs(x, y):
        candi = [(x, y)]
        q = collections.deque()
        q.append((x, y))
        visited = [[False] * L for _ in range(L)]
        visited[x][y] = True
        while q:
            x, y = q.popleft()

            for num, (dx, dy) in enumerate(dir):
                nx, ny = x + dx, y + dy

                if 0 <= nx < L and 0 <= ny < L and not visited[nx][ny] and knights[nx][ny] != 0:
                    if knights[nx][ny] == knights[x][y]:
                        pass
                    elif num == d:
                        pass
                    else:
                        continue
                    candi.append((nx, ny))
                    visited[nx][ny] = True
                    q.append((nx, ny))
        return candi

    def move(candi, d):
        tmp = [[0] * L for _ in range(L)]
        dx, dy = dir[d]
        moved = []
        for x, y in candi:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < L and 0 <= ny < L and board[nx][ny] != 2):
                return []
            tmp[nx][ny] = knights[x][y]
            moved.append((nx, ny))
        for x, y in candi:
            knights[x][y] = 0
        for x, y in candi:
            nx, ny = x + dx, y + dy
            if tmp[nx][ny] != 0:
                knights[nx][ny] = tmp[nx][ny]
        return moved

    for i in range(L):
        for j in range(L):
            if knights[i][j] == idx:
                candi = bfs(i, j)
                val = move(candi, d)
                if val:
                    damage(idx, val)
                    return
                return


# 대미지 입히기
def damage(idx, moved):
    for x, y in moved:
        if knights[x][y] == idx:
            continue

        if board[x][y] == 1:
            energy[knights[x][y]] = max(energy[knights[x][y]] - 1, 0)

    for x, y in moved:
        if energy[knights[x][y]] == 0:
            knights[x][y] = 0


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    L, N, Q = map(int, input().split())

    board = [list(map(int, input().split())) for _ in range(L)]
    knights = [[0] * L for _ in range(L)]
    energy = collections.defaultdict(int)
    moved = {}
    for idx in range(1, N + 1):
        r, c, h, w, k = map(int, input().split())
        r -= 1
        c -= 1
        for i in range(r, r + h):
            for j in range(c, c + w):
                knights[i][j] = idx
        energy[idx] = k

    origin_energy = copy.deepcopy(energy)
    for _ in range(Q):
        idx, d = map(int, input().split())
        find_knights(idx, d)

    result = 0

    for o, e in zip(origin_energy.values(), energy.values()):
        if e == 0:
            continue
        result += o - e

    print(result)