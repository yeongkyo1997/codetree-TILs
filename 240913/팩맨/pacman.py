import math
import sys



# 몬스터 복제 시도
def copy():
    for i in range(N):
        for j in range(N):
            # 해당 칸에 있는 모든 몬스터들이 알을 낳는다
            for d in monster[i][j]:
                eggs[i][j].append(d)


# 몬스터 이동
def monster_move():
    tmp = [[[] for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            for d in monster[i][j]:
                nd = d
                for _ in range(8):
                    dx, dy = dir8[nd]
                    nx, ny = i + dx, j + dy
                    # 움직일 수 있는 칸이 있다면
                    if 0 <= nx < N and 0 <= ny < N and pacman != (nx, ny) and death[nx][ny] == 0:
                        tmp[nx][ny].append(nd)
                        break
                    nd = (nd + 1) % 8
                # 움직일 수 있는 칸이 없다면
                else:
                    tmp.append(d)
                    print(d, nd)
    return tmp


# 팩맨 이동
def pacman_move():
    def perm(path, depth):
        if depth == 3:
            move_dir.append(path)
            return

        for i in range(4):
            perm(path + [i], depth + 1)

    move_dir = []

    # 움직일 수 있는 칸의 경우의 수를 중복 순열을 이용해서 구하기
    perm([], 0)

    global pacman
    x, y = pacman
    n_path = []
    for idx, path in enumerate(move_dir):
        nx, ny = x, y
        cnt = 0
        check = set()
        for d in path:
            dx, dy = dir4[d]
            nx, ny = nx + dx, ny + dy
            if 0 <= nx < N and 0 <= ny < N:
                if (nx, ny) not in check:
                    check.add((nx, ny))
                    cnt += len(monster[nx][ny])
            else:
                break
        else:
            n_path.append((-cnt, idx, path[:]))
            n_path.sort()
    path = n_path[0][-1]

    for d in path:
        dx, dy = dir4[d]
        x += dx
        y += dy
        # 시체를 2턴 동안 유지 시키기
        if monster[x][y]:
            death[x][y] = 2
        monster[x][y] = []

    pacman = (x, y)


# 몬스터 시체 소멸
def remove_monster():
    for i in range(N):
        for j in range(N):
            if death[i][j] > 0:
                death[i][j] -= 1


# 몬스터 복제 완성
def copy_finish():
    for i in range(N):
        for j in range(N):
            if eggs[i][j]:
                for d in eggs[i][j]:
                    monster[i][j].append(d)
                eggs[i][j] = []


if __name__ == '__main__':
    dir4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    dir8 = [(-1, 0), (-1, -1), (0, -1), (-1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]

    M, T = map(int, input().split())
    N = 4
    pacman = tuple(map(lambda x: int(x) - 1, input().split()))
    monster = [[[] for _ in range(N)] for _ in range(N)]
    death = [[0] * N for _ in range(N)]
    eggs = [[[] for _ in range(N)] for _ in range(N)]

    for _ in range(M):
        r, c, d = map(lambda x: int(x) - 1, input().split())
        monster[r][c].append(d)

    for _ in range(T):
        # 몬스터 복제 시도
        copy()
        # 몬스터 이동
        monster = monster_move()
        # 팩맨이동
        pacman_move()
        # 시체 소멸
        remove_monster()
        # 몬스터 복제 완료
        copy_finish()

    result = 0
    for i in range(N):
        for j in range(N):
            result += len(monster[i][j])
    print(result)