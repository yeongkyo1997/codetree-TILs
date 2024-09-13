import collections
import sys

# sys.stdin = open('루돌프의 반란', 'r')


# 거리
def get_dist(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2


# 유효한 산타인지 확인하는 함수
def is_valid_santa(idx):
    sx, sy = santa[idx]
    return 0 <= sx < N and 0 <= sy < N


# 루돌프의 움직임
def move_R():
    # 가장 가까운 산타 찾기
    def find_santa():
        candi = []
        for key, (sx, sy) in santa.items():
            # 탈락했다면
            if not is_valid_santa(key):
                continue
            candi.append((get_dist(Rr, Rc, sx, sy), -sx, -sy, key))

        candi.sort()
        return candi[0][-1]

    # 이동하기
    def move():
        santa_idx = find_santa()
        sx, sy = santa[santa_idx]
        # 이동 좌표에 대한 후보
        candi = []
        for idx, (dx, dy) in enumerate(dir8):
            nx, ny = Rr + dx, Rc + dy
            if 0 <= nx < N and 0 <= ny < N:
                candi.append((get_dist(sx, sy, nx, ny), (nx, ny, idx)))
        candi.sort()
        return candi[0][-1]

    rx, ry, rd = move()
    for idx, (sx, sy) in santa.items():
        if (sx, sy) == (rx, ry):
            collapse(idx, sx, sy, rd, dir8, C, True)
            santa_stun[idx] = 2
            santa_score[idx] += C
    return rx, ry


# 산타 움직이기
def move_S():
    for key, (sx, sy) in santa.items():
        # 산타가 탈락했다면
        if not is_valid_santa(key):
            continue

        # 기절한 산타라면
        if santa_stun[key] > 0:
            continue

        # 산타가 움직일 수 있는 위치 찾기
        candi = [(get_dist(Rr, Rc, sx, sy), (sx, sy, 0))]
        for d, (dx, dy) in enumerate(dir4):
            nx, ny = sx + dx, sy + dy
            if 0 <= nx < N and 0 <= ny < N:
                # 산타가 있는지 확인
                for idx, val in santa.items():
                    if key != idx and (is_valid_santa(idx) and val == (nx, ny)):
                        break
                else:
                    # 없다면
                    candi.append((get_dist(Rr, Rc, nx, ny), d, (nx, ny, d)))
        candi.sort()
        nx, ny, nd = candi[0][-1]

        if (nx, ny) == (Rr, Rc):
            collapse(key, nx, ny, nd, dir4, D, False)
            santa_score[key] += D
            santa_stun[key] = 2
        else:
            santa[key] = (nx, ny)


# 충돌이 났을 때
# 루돌프와 산타의 이동 가능 방향이 다르기 때문에 상황에 맞게 넣어 줘야 함
def collapse(key, sx, sy, sd, dir, val, is_R):
    # 밀려났을 때의 좌표
    dx, dy = dir[sd]
    if is_R:
        sx += dx * val
        sy += dy * val
    else:
        sx -= dx * val
        sy -= dy * val
    santa[key] = (sx, sy)

    # 게임판 밖으로 나간 경우라면
    if not (0 <= sx < N and 0 <= sy < N):
        return

    candi = []
    # 좌표에서 시작해서 방향으로 산타가 없을 때 까지 반복
    nx, ny = sx, sy
    while True:
        for idx, val in santa.items():
            if idx == key:
                continue
            if val == (nx, ny):
                candi.append(idx)
        if is_R:
            nx += dx
            ny += dy
        else:
            nx -= dx
            ny -= dy
        if not (0 <= nx < N and 0 <= ny < N):
            break

    for c in candi:
        val = santa[c]
        if is_R:
            santa[c] = (val[0] + dx, val[1] + dy)
        else:
            santa[c] = (val[0] - dx, val[1] - dy)


# 턴이 끝났을 때 탈락하지 않은 산타들 1점 추가 부여
def plus():
    for key in santa.keys():
        if is_valid_santa(key):
            santa_score[key] += 1


# 스턴 1씩 감소
def minus():
    for key, val in santa_stun.items():
        if val > 0:
            santa_stun[key] -= 1


# 산타가 전부 탈락했는지 확인
def is_fail():
    for key in santa.keys():
        if is_valid_santa(key):
            return False
    return True


if __name__ == '__main__':
    dir8 = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    dir4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    N, M, P, C, D = map(int, input().split())
    Rr, Rc = map(lambda x: int(x) - 1, input().split())
    santa = collections.defaultdict(tuple)

    # 산타 점수
    santa_score = collections.defaultdict(int)

    # 기절한 산타
    santa_stun = collections.defaultdict(int)
    for _ in range(P):
        idx, x, y = map(int, input().split())
        x -= 1
        y -= 1
        santa[idx] = (x, y)

    # 턴시작
    for t in range(M):
        # 루돌프 움직이기
        Rr, Rc = move_R()

        # 산타 움직이기
        move_S()
        plus()
        minus()
        if is_fail():
            break

    for i in range(1, P + 1):
        print(santa_score[i], end=' ')