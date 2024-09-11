import collections
import sys

# sys.stdin = open('왕실의 기사 대결', 'r')


def move(idx, d):
    def bfs(sx, sy, s_idx, sd):
        q = collections.deque()
        q.append((sx, sy, s_idx))
        visited = [[0] * L for _ in range(L)]
        candi = [(sx, sy)]
        visited[sx][sy] = 1
        while q:
            x, y, idx = q.popleft()
            for d, (dx, dy) in enumerate(dir):
                nx, ny = x + dx, y + dy

                if 0 <= nx < L and 0 <= ny < L and (visited[nx][ny] >= visited[x][y] + 1 or visited[nx][ny] == 0):
                    visited[nx][ny] = visited[x][y] + 1
                    # 다음 이동이 벽이라면
                    if sd == d and board[nx][ny] == 2:
                        return None
                    # 나이트가 없다면 후보가 될 수 없다
                    if not knights[nx][ny]:
                        continue

                    # 다음 이동과 인덱스가 같다면 무조건 추가
                    if idx == knights[nx][ny]:
                        candi.append((nx, ny))
                        q.append((nx, ny, idx))
                    else:
                        # 다르다면 sd 방향에 있는 것만 추가
                        if d == sd:
                            candi.append((nx, ny))
                            q.append((nx, ny, knights[nx][ny]))
        return candi

    for i in range(L):
        for j in range(L):
            global knights
            if knights[i][j] == idx:
                candi = bfs(i, j, idx, d)
                if candi:
                    tmp = [[0] * L for _ in range(L)]
                    dx, dy = dir[d]
                    for cx, cy in candi:
                        if 0 <= cx + dx < L and 0 <= cy + dy < L:
                            tmp[cx + dx][cy + dy] = knights[cx][cy]
                            knights[cx][cy] = 0
                    for x in range(L):
                        for y in range(L):
                            if tmp[x][y]:
                                continue
                            if knights[x][y]:
                                tmp[x][y] = knights[x][y]
                    knights = tmp
                return


# 데미지 입히기
def damage():
    for i in range(L):
        for j in range(L):
            if board[i][j] == 1 and knights[i][j]:
                if knights[i][j] == idx:
                    continue
                damaged[knights[i][j]] += 1
                power[knights[i][j]] -= 1

    for i in range(L):
        for j in range(L):
            if power[knights[i][j]] <= 0:
                knights[i][j] = 0
                damaged[knights[i][j]] = 0


# 살아있는 기사가 받은 데미지 계산하기
def calc():
    ret = 0
    for i in range(1, N + 1):
        ret += damaged[i]

    return ret




if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    L, N, Q = map(int, input().split())

    board = [list(map(int, input().split())) for _ in range(L)]
    knights = [[0] * L for _ in range(L)]
    damaged = collections.defaultdict(int)
    power = collections.defaultdict(int)
    for idx in range(1, N + 1):
        r, c, h, w, k = map(int, input().split())
        r, c = map(lambda x: x - 1, (r, c))
        power[idx] = k

        for i in range(r, r + h):
            for j in range(c, c + w):
                knights[i][j] = idx
    result = 0
    for _ in range(Q):
        idx, d = map(int, input().split())
        move(idx, d)
        damage()
    result = calc()
    print(result)