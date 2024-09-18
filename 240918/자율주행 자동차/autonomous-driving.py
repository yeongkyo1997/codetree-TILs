import sys

# sys.stdin = open('자율주행 자동차', 'r')


# 움직이기
def move(sx, sy, sd):
    visited = [[False] * M for _ in range(N)]
    ret = 0

    while True:
        # 현재 위치 방문 여부 확인
        if not visited[sx][sy]:
            visited[sx][sy] = True
            ret += 1

        # 다음 위치 찾기
        for d in range(1, len(dir) + 1):
            nd = (sd - d) % 4
            dx, dy = dir[nd]
            nx, ny = sx + dx, sy + dy

            # 다음 위치를 찾았다면
            if 0 <= nx < N and 0 <= ny < M and not visited[nx][ny] and board[nx][ny] == 0:
                sx, sy, sd = nx, ny, nd
                break
        else:
            # 찾지 못 했다면
            dx, dy = dir[sd]
            nx, ny = sx - dx, sy - dy
            # 후진 가능
            if 0 <= nx < N and 0 <= ny < M and board[nx][ny] == 0:
                sx, sy = nx, ny
            else:
                break
    return ret


if __name__ == '__main__':
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    N, M = map(int, input().split())
    sx, sy, sd = map(int, input().split())
    car = (sx - 1, sy - 1, sd)
    board = [list(map(int, input().split())) for _ in range(N)]

    print(move(sx, sy, sd))