import sys
from collections import defaultdict as dd

class Node:
    def __init__(self, id=0, color=0, max_depth=0, parent=0):
        self.id = id
        self.color = color
        self.max_depth = max_depth
        self.parent = parent
        self.child = []


if __name__ == '__main__':
    Q = int(input())
    node = [Node() for _ in range(100000 + 100)]
    check_root = [0] * (100000 + 100)

    for _ in range(Q):
        query, *data = map(int, input().split())

        if query == 100:
            def check(cur, depth):
                if cur.id == 0:
                    return True  # 최대 깊이 이전에 부모를 찾은 경우
                if cur.max_depth <= depth:
                    return False
                return check(node[cur.parent], depth + 1)


            m_id, p_id, color, max_depth = data
            if p_id == -1:
                check_root[m_id] = 1

            if check_root[m_id] == 1 or check(node[p_id], 1):
                node[m_id].id = m_id
                node[m_id].color = color
                node[m_id].max_depth = max_depth
                node[m_id].parent = 0 if check_root[m_id] == 1 else p_id

                if check_root[m_id] != 1:
                    node[p_id].child.append(m_id)

        elif query == 200:
            def dfs(m_id, color):
                node[m_id].color = color
                for child_id in node[m_id].child:
                    dfs(child_id, color)


            m_id, color = data
            dfs(m_id, color)

        elif query == 300:
            m_id = data[0]
            print(node[m_id].color)
        elif query == 400:
            def get_score():
                def calc(cur, color_cnt):
                    tmp_color_cnt = dd(int)
                    tmp_color_cnt[cur.color] = 1

                    ret = 0
                    for child_id in cur.child:
                        child = node[child_id]

                        child_color_cnt = dd(int)
                        score = calc(child, child_color_cnt)

                        for i in range(1, 5 + 1):
                            tmp_color_cnt[i] += child_color_cnt[i]

                        ret += score

                    cnt = sum(1 for i in range(1, 6) if tmp_color_cnt[i])

                    ret += cnt * cnt

                    for i in range(1, 5 + 1):
                        color_cnt[i] += tmp_color_cnt[i]

                    return ret

                ret = 0
                color_cnt = dd(int)
                for i in range(1, 100001):
                    if check_root[i] == 1:
                        ret += calc(node[i], color_cnt)
                return ret


            score = get_score()
            print(score)