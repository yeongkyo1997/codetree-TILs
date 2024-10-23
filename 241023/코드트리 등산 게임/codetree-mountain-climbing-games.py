import bisect


def main():
    def solve():
        Q = int(input())

        mountains = []  # 산 리스트
        lis = []  # 각 산에서의 LIS
        tail = []  # LIS 계산 저장
        changes = []  # tail 리스트의 변경 기록 추적
        highest_list = []  # 최대 높이 저장
        LIS_max = 0  # 현재까지의 최대 LIS 길이

        result = []

        for _ in range(Q):
            cmd = list(map(int, input().split()))
            # 초기 지도 설정
            if cmd[0] == 100:
                _, n, *data = cmd
                h_list = data

                mountains = []
                lis = []
                tail = []
                changes = []
                highest_list = []
                LIS_max = 0

                # 각 산의 높이에 LIS
                for h in h_list:
                    # 이분탐색
                    pos = bisect.bisect_left(tail, h)
                    if pos == len(tail):
                        tail.append(h)
                        changes.append((pos, None))
                    else:
                        old_h = tail[pos]
                        tail[pos] = h
                        changes.append((pos, old_h))
                    LIS_i = pos + 1
                    mountains.append(h)
                    lis.append(LIS_i)

                    # LIS 갱신
                    if LIS_i > LIS_max:
                        LIS_max = LIS_i
                        highest_list.append([(h, h)])
                    elif LIS_i == LIS_max:
                        if highest_list:
                            current_max = highest_list[-1][-1][1]
                            new_max = max(current_max, h)
                            highest_list[-1].append((h, new_max))
                        else:
                            highest_list.append([(h, h)])
                    else:
                        pass

            # 산 추가(우공이산)
            elif cmd[0] == 200:
                h = cmd[1]

                # h가 들어갈 위치 찾기
                pos = bisect.bisect_left(tail, h)
                if pos == len(tail):
                    tail.append(h)
                    changes.append((pos, None))
                else:
                    old_h = tail[pos]
                    tail[pos] = h
                    changes.append((pos, old_h))
                LIS_i = pos + 1
                mountains.append(h)
                lis.append(LIS_i)

                # LIS 갱신
                if LIS_i > LIS_max:
                    LIS_max = LIS_i
                    highest_list.append([(h, h)])
                elif LIS_i == LIS_max:
                    if highest_list:
                        current_max = highest_list[-1][-1][1]
                        new_max = max(current_max, h)
                        highest_list[-1].append((h, new_max))
                    else:
                        highest_list.append([(h, h)])
                else:
                    pass

            # 마지막 산 제거(지진)
            elif cmd == 300:
                if not mountains:
                    continue

                # 마지막 산과 LIS 정보 제거
                LIS_i = lis.pop()
                pos = LIS_i - 1
                change = changes.pop()

                # tail 복구
                if change[1] is None:
                    tail.pop()
                else:
                    tail[pos] = change[1]
                if LIS_i == LIS_max:
                    if highest_list:
                        highest_list[-1].pop()
                        if not highest_list[-1]:
                            highest_list.pop()
                            LIS_max -= 1

            # 등산 시뮬레이션 처리
            elif cmd[0] == 400:
                idx = cmd[1]

                # 점수 계산
                if not mountains:
                    score = 0
                else:
                    if len(mountains) < idx or idx < 1:
                        score = 0
                    else:
                        LIS_m = lis[idx - 1]
                        cur_lis_max = LIS_max
                        if cur_lis_max >= 1 and highest_list:
                            max_h_LIS_max = highest_list[-1][-1][1]
                        else:
                            max_h_LIS_max = 0
                        score = (LIS_m + cur_lis_max - 1) * 1000000 + max_h_LIS_max
                result.append(str(score))

        print('\n'.join(result))

    solve()


if __name__ == "__main__":
    main()