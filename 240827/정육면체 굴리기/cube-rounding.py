import collections

dir = [(), (0, 1), (0, -1), (-1, 0), (1, 0)]

n, m, x, y, k = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]
command_dir = list(map(int, input().split()))

dice = [0] * 6

def east():
    dice[0], dice[2], dice[5], dice[3] = dice[3], dice[0], dice[2], dice[5]

def west():
    dice[0], dice[3], dice[5], dice[2] = dice[2], dice[0], dice[3], dice[5]

def north():
    dice[0], dice[1], dice[5], dice[4] = dice[1], dice[5], dice[4], dice[0]

def south():
    dice[0], dice[4], dice[5], dice[1] = dice[4], dice[5], dice[1], dice[0]

def move(x, y, c):
    nx, ny = x + dir[c][0], y + dir[c][1]
    if 0 <= nx < n and 0 <= ny < m:
        return nx, ny
    return x, y

for c in command_dir:
    nx, ny = move(x, y, c)
    if (nx, ny) != (x, y):
        if c == 1:
            east()
        elif c == 2:
            west()
        elif c == 3:
            north()
        elif c == 4:
            south()

        if board[nx][ny] == 0:
            board[nx][ny] = dice[5]
        else:
            dice[5] = board[nx][ny]
            board[nx][ny] = 0

        print(dice[0])
        x, y = nx, ny