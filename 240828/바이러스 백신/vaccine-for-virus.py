import collections
import math

# 병원-바이러스 최소시간 구하기
def bfs(path):
    global result
    q = collections.deque(path)
    visited = [[-1] * n for _ in range(n)]
    for px, py in path:
        visited[px][py] = 0

    while q:
        x, y = q.popleft()

        for dx, dy in dir:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < n and visited[nx][ny] == -1 and board[nx][ny] != 1:
                visited[nx][ny] = visited[x][y] + 1
                q.append((nx, ny))

    max_time = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                if visited[i][j] == -1:
                    return  # 모든 빈 칸에 도달할 수 없는 경우
                max_time = max(max_time, visited[i][j])

    result = min(result, max_time)


# 병원 선택하기
def dfs(path, depth, start):
    if depth == m:
        bfs(path)
        return

    for i in range(start, len(hospitals)):
        path.append(hospitals[i])
        dfs(path, depth + 1, i + 1)
        path.pop()


if __name__ == '__main__':
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    n, m = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    hospitals = []
    for i in range(n):
        for j in range(n):
            if board[i][j] == 2:
                hospitals.append((i, j))

    result = math.inf
    dfs([], 0, 0)

    # 모든 빈 칸에 도달할 수 없는 경우를 처리
    if result == math.inf:
        print(-1)
    else:
        print(result)