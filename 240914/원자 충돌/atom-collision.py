import sys

# sys.stdin = open('원자 충돌', 'r')


# 자신의 방향으로 자신의 속력만큼 이동
def move_common():
    tmp = [[[] for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for m, s, d in board[i][j]:
                dx, dy = dir[d]
                nx, ny = (i + dx * s) % N, (j + dy * s) % N
                tmp[nx][ny].append((m, s, d))
    return tmp


# 원자 합치기
def merge():
    def is_plus(ele):
        _, _, d = ele[0]
        prev = d % 2
        for _, _, d in ele:
            if prev != d % 2:
                return False
        return True

    for i in range(N):
        for j in range(N):
            if len(board[i][j]) >= 2:
                total = sum(e[0] for e in board[i][j])
                speed = sum(e[1] for e in board[i][j])
                l = len(board[i][j])

                if total // 5 == 0:
                    board[i][j] = []
                    break
                # # 십자가로 합치기
                if is_plus(board[i][j]):
                    board[i][j] = []
                    for d in range(0, len(dir), 2):
                        board[i][j].append((total // 5, speed // l, d))
                else:
                    board[i][j] = []
                    for d in range(1, len(dir), 2):
                        board[i][j].append((total // 5, speed // l, d))


if __name__ == '__main__':
    dir = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    N, M, K = map(int, input().split())
    board = [[[] for _ in range(N)] for _ in range(N)]

    for _ in range(M):
        x, y, m, s, d = map(int, input().split())
        x -= 1
        y -= 1
        board[x][y].append((m, s, d))

    for _ in range(K):
        board = move_common()
        merge()

    result = 0
    for i in range(N):
        for j in range(N):
            if board[i][j]:
                result += sum(b[0] for b in board[i][j])

    print(result)