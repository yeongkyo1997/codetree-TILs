import collections
import sys

input = lambda: sys.stdin.readline().rstrip()


class Box:
    def __init__(self, box_id):
        self.box_id = box_id
        self.next = None
        self.prev = None


class Belt:
    def __init__(self):
        self.header = None
        self.tail = None
        self.box_dict = {}

    # 뒤에 박스 넣기
    def append(self, box):
        self.box_dict[box.box_id] = box

        if self.tail is None:
            self.header = box
        else:
            self.tail.next = box
            box.prev = self.tail

        self.tail = box

    # 앞에 박스 넣기
    def appendleft(self, box):
        self.box_dict[box.box_id] = box

        if self.header is None:
            self.tail = box
        else:
            self.header.prev = box
            box.next = self.header

        self.header = box

    # 앞에서 빼기
    def popleft(self):
        box = self.header

        # 박스가 하나라면
        if box.next is None:
            self.tail = None
        else:
            box.next.prev = box.prev

        self.header = box.next
        box.next = None
        box.prev = None

        del self.box_dict[box.box_id]

        return box

    # 뒤에서 빼기
    def pop(self):
        box = self.tail

        if box.prev is None:
            self.header = None
        else:
            box.prev.next = None  # 이전 박스의 next를 None으로 설정

        self.tail = box.prev  # tail을 이전 박스로 설정
        box.next = None
        box.prev = None

        del self.box_dict[box.box_id]

        return box


def step2(m_src, m_dst):
    src_belt = belts[m_src]
    dst_belt = belts[m_dst]

    # src_belt가 비어있다면 이동할 박스가 없음
    if not src_belt.header:
        return len(dst_belt.box_dict)

    # src_belt의 모든 박스를 dst_belt로 옮기기
    if not dst_belt.header:  # dst_belt가 비어있다면
        dst_belt.header = src_belt.header
        dst_belt.tail = src_belt.tail
    else:
        # 연결 업데이트
        src_belt.tail.next = dst_belt.header
        dst_belt.header.prev = src_belt.tail
        dst_belt.header = src_belt.header

    dst_belt.box_dict.update(src_belt.box_dict)

    # src_belt 초기화
    src_belt.header = src_belt.tail = None
    src_belt.box_dict.clear()

    return len(dst_belt.box_dict)


def step3(m_src, m_dst):
    src_belt = belts[m_src]
    dst_belt = belts[m_dst]

    # 두 벨트가 모두 비어있다면 아무것도 하지 않음
    if src_belt.header is None and dst_belt.header is None:
        return 0

    # 하나의 벨트가 비어있다면, 다른 벨트의 박스를 옮김
    if src_belt.header is None:
        dst_box = dst_belt.popleft()
        src_belt.appendleft(dst_box)
    elif dst_belt.header is None:
        src_box = src_belt.popleft()
        dst_belt.appendleft(src_box)
    else:
        # 두 벨트가 비어있지 않을 때, 첫 번째 박스를 교환
        src_box = src_belt.popleft()
        dst_box = dst_belt.popleft()
        dst_belt.appendleft(src_box)
        src_belt.appendleft(dst_box)

    return len(dst_belt.box_dict)


def step4(m_src, m_dst):
    src_belt = belts[m_src]
    dst_belt = belts[m_dst]

    # src_belt가 비어있으면 아무 작업도 하지 않음
    if len(src_belt.box_dict) <= 1:
        return len(dst_belt.box_dict)

    # src_belt에서 절반의 박스를 dst_belt의 앞쪽에 옮기기
    size = len(src_belt.box_dict) // 2
    tmp = collections.deque()

    # src_belt에서 size만큼 popleft 해서 임시 deque에 넣기
    for _ in range(size):
        tmp.append(src_belt.popleft())

    # 임시 deque에서 하나씩 꺼내서 dst_belt의 앞에 appendleft 하기
    while tmp:
        dst_belt.appendleft(tmp.pop())

    return len(dst_belt.box_dict)


def step5(p_num):
    a, b = -1, -1
    for belt in belts[1:]:
        if p_num in belt.box_dict:
            box = belt.box_dict[p_num]
            if box.prev is not None:
                a = box.prev.box_id
            if box.next is not None:
                b = box.next.box_id
            break

    return a + 2 * b


def step6(b_num):
    belt = belts[b_num]
    a, b, c = 0, 0, 0

    if belt.header is None:
        a = b = -1
    else:
        a = belt.header.box_id
        b = belt.tail.box_id

    c = len(belt.box_dict)

    return a + 2 * b + 3 * c


if __name__ == '__main__':
    q = int(input())
    belts = None

    for _ in range(q):
        query, *data = map(int, input().split())
        if query == 100:
            N, M, *data = data
            belts = [Belt() for _ in range(N + 1)]
            it = iter(list(range(1, M + 1)))

            for idx in data:
                belts[idx].append(Box(next(it)))

        if query == 200:
            m_src, m_dst = data
            print(step2(m_src, m_dst))

        if query == 300:
            m_src, m_dst = data
            print(step3(m_src, m_dst))

        if query == 400:
            m_src, m_dst = data
            print(step4(m_src, m_dst))

        if query == 500:
            p_num = data[0]
            print(step5(p_num))

        if query == 600:
            b_num = data[0]
            print(step6(b_num))