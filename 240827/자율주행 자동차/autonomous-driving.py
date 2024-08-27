def move(x, y, d):
    visited = [[False] * m for _ in range(n)]
    visited[x][y] = True
    ret = 1

    while True:
        # 반시계방향으로 회전하면서 이동 가능한 칸 찾기
        for _ in range(4):
            d = (d + 3) % 4
            dx, dy = dir[d]
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and board[nx][ny] == 0:
                x, y = nx, ny
                visited[nx][ny] = True
                ret += 1
                break
        else:
            # 못 찾을 경우 후진
            dx, dy = dir[d]
            x -= dx
            y -= dy
            if 0 <= x < n and 0 <= y < m and board[x][y] != 1:
                continue
            else:
                return ret


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    n, m = map(int, input().split())
    sx, sy, sd = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    result = move(sx, sy, sd)
    print(result)