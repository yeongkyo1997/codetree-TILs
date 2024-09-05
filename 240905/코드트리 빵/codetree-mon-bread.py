import sys
from collections import deque

# sys.stdin = open('코드트리 빵', 'r')
# 격자의 크기 n과 사람의 수 m 입력
n, m = map(int, input().split())

# 격자 정보 입력
grid = [list(map(int, input().split())) for _ in range(n)]

# 편의점 위치 입력
stores = [tuple(map(lambda x: int(x) - 1, input().split())) for _ in range(m)]

# 이동 방향 (상, 좌, 우, 하 순서)
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

# 사람들의 현재 위치
people = []


# 각 편의점까지의 최단 거리를 계산하는 함수
def bfs(start, end):
    queue = deque([(start, 0)])
    visited = [[False] * n for _ in range(n)]
    visited[start[0]][start[1]] = True

    while queue:
        (x, y), dist = queue.popleft()
        if (x, y) == end:
            return dist
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append(((nx, ny), dist + 1))
    return float('inf')


# 베이스캠프 찾기
def find_basecamp(store):
    min_dist = float('inf')
    basecamp = None
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                dist = bfs((i, j), store)
                if dist < min_dist:
                    min_dist = dist
                    basecamp = (i, j)
    return basecamp


# 시뮬레이션
time = 0
arrived = [False] * m

while not all(arrived):
    # 이미 격자에 있는 사람들 이동
    for i, person in enumerate(people):
        if not arrived[i]:
            x, y = person
            store = stores[i]
            min_dist = float('inf')
            next_pos = None
            for j in range(4):
                nx, ny = x + dx[j], y + dy[j]
                if 0 <= nx < n and 0 <= ny < n:
                    dist = bfs((nx, ny), store)
                    if dist < min_dist:
                        min_dist = dist
                        next_pos = (nx, ny)
            people[i] = next_pos
            if people[i] == store:
                arrived[i] = True
                grid[store[0]][store[1]] = 2  # 편의점 도착 표시

    # 새로운 사람 추가
    if time < m:
        basecamp = find_basecamp(stores[time])
        people.append(basecamp)
        grid[basecamp[0]][basecamp[1]] = 2  # 베이스캠프 사용 표시

    time += 1

print(time)