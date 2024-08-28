from collections import deque


def bfs(d):
    visited = [[False] * N for _ in range(M)]
    q = deque([painted_points[0]])
    visited[painted_points[0][0]][painted_points[0][1]] = True

    while q:
        x, y = q.popleft()
        for dx, dy in dir:
            nx, ny = x + dx, y + dy
            if 0 <= nx < M and 0 <= ny < N and not visited[nx][ny]:
                if abs(board[nx][ny] - board[x][y]) <= d:
                    visited[nx][ny] = True
                    q.append((nx, ny))

    return all(visited[i][j] for i, j in painted_points)


if __name__ == '__main__':
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    M, N = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(M)]
    painted_board = [list(map(int, input().split())) for _ in range(M)]

    painted_points = [(i, j) for i in range(M) for j in range(N) if painted_board[i][j] == 1]

    left, right = 0, 10 ** 9
    result = right

    while left <= right:
        mid = (left + right) // 2
        if bfs(mid):
            result = mid
            right = mid - 1
        else:
            left = mid + 1

    print(result)