import heapq


# 사람들 이동시키기
def bfs():
    global people, result
    heapq.heapify(people)

    while people:
        t, x, y, idx = heapq.heappop(people)
        if len(people) == len(finished_people):
            break
        if idx in finished_people:
            continue

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < n and times[nx][ny] <= t + 1:
                if (nx, ny) == store[idx]:
                    finished_people.add(idx)
                    times[nx][ny] = t + 1
                    result = max(result, t + 1)
                heapq.heappush(people, (t + 1, nx, ny, idx))


# 편의점에서 가장 가까운 베이스 캠프 구하기
def get_shortest_basecamp(x, y):
    heap = []
    heapq.heappush(heap, ((0, x, y)))
    visited = [[False] * n for _ in range(n)]
    visited[x][y] = True

    while heap:
        depth, x, y = heapq.heappop(heap)

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            # board 2는 베이스캠프에 방문한 것으로 간주
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and board[nx][ny] != 2:
                visited[nx][ny] = True
                if board[nx][ny] == 1:
                    board[nx][ny] = 2
                    return nx, ny
                heapq.heappush(heap, (depth + 1, nx, ny))


if __name__ == '__main__':
    dir = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    n, m = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    people = []
    store = [()]

    for _ in range(m):
        x, y = map(lambda x: int(x) - 1, input().split())
        store.append((x, y))
    times = [[0] * n for _ in range(n)]
    finished_people = set()
    result = 0
    # 1분씩 증가 시켜서 프로세스 진행
    for t in range(1, m + 1):
        # 베이스 캠프에 있는 사람들 움직이기
        # 사람들을 베이스 캠프에 넣기
        if t <= m:
            # 가장 가까운 베이스 캠프
            x, y = store[t]
            sx, sy = get_shortest_basecamp(x, y)
            # 베이스 캠프에 들어간 시점 이후 시간은 방문이 안됨 같으면 들어갈수있음
            times[sx][sy] = t
            # 사람 좌표에 번호를 추가하기, 시작시간을 넣음
            people.append((t, sx, sy, t))

    bfs()
    print(result)