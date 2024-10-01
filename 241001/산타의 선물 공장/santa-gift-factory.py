import sys

input = lambda: sys.stdin.readline().rstrip()


class Box:
    def __init__(self, box_id, weight):
        self.box_id = box_id
        self.weight = weight
        self.next = None
        self.prev = None


class Belt:
    def __init__(self):
        self.header = None
        self.tail = None
        self.box_hash = {}
        self.broken = False

    def append(self, box):
        # 비어있다면
        if self.tail is None:
            self.header = box
        else:
            self.tail.next = box
            box.prev = self.tail

        self.tail = box
        self.box_hash[box.box_id] = box

    def appendleft(self, box):
        # 비어있다면
        if self.header is None:
            self.tail = box
        else:
            self.header.prev = box
            box.next = self.header

        self.header = box
        self.box_hash[box.box_id] = box

    # 맨 앞 물건 하차
    def popleft(self):
        box = self.header

        # 박스가 하나라면
        if box == self.tail:
            self.tail = None
            self.header = None
        else:
            self.header = box.next
            box.next.prev = None

        del self.box_hash[box.box_id]
        return box

    def pop(self):
        box = self.tail

        # 박스가 하나라면
        if box == self.header:
            self.header = None
            self.tail = None
        else:
            self.tail = box.prev
            box.prev.next = None

        del self.box_hash[box.box_id]
        return box

    # 번호에 해당하는 상자 제거
    def remove(self, r_id):
        box = self.box_hash[r_id]

        # 맨 앞에 있다면
        if self.header == box:
            return self.popleft()
        elif self.tail == box:
            return self.pop()
        else:
            box.prev.next = box.next
            box.next.prev = box.prev

        del self.box_hash[box.box_id]

        return box

    # f_id 뒤에 모든 상자를 뒤로 보내기
    def move_dump(self, f_id):
        box = self.box_hash[f_id]

        # 박스가 하나라면
        if self.header == self.tail:
            return
        # 상자가 맨 앞에 있다면
        elif self.header == box:
            return
        # 상자가 맨 뒤에 있다면
        elif self.tail == box:
            self.appendleft(self.pop())
        else:
            self.header.prev = self.tail
            self.tail.next = self.header
            self.header = box
            self.tail = box.prev
            box.prev.next = None
            box.prev = None


def step2(w_max):
    ret = 0
    for belt in belts:
        if belt.header is not None:
            box = belt.popleft()
            if box.weight <= w_max:
                ret += box.weight
            else:
                belt.append(box)

    return ret


def step3(r_id):
    for belt in belts:
        if r_id in belt.box_hash:
            belt.remove(r_id)
            return r_id

    return -1


def step4(f_id):
    for idx, belt in enumerate(belts):
        if f_id in belt.box_hash:
            belt.move_dump(f_id)
            return idx + 1

    return -1


def step5(b_num):
    if belts[b_num - 1].broken:
        return -1  # 벨트가 이미 고장났다면 -1 반환

    # 고장난 벨트 설정
    belts[b_num - 1].broken = True

    # 상자 이동할 대상 벨트를 찾기 위한 초기 인덱스 설정
    n = len(belts)
    idx = b_num % n  # 다음 벨트 인덱스

    # b_num 벨트의 상자들을 이동할 대상 벨트 찾기
    while idx != b_num - 1:
        if not belts[idx].broken:
            # 대상 벨트에 b_num 벨트의 상자들을 하나씩 옮김
            while belts[b_num - 1].header:
                box = belts[b_num - 1].popleft()
                belts[idx].append(box)
            return b_num  # 작업이 성공적으로 완료된 경우 b_num 반환
        idx = (idx + 1) % n  # 다음 벨트로 넘어감

    # 이 부분에 도달하면 안 되지만, 안전을 위해 추가
    return -1


if __name__ == '__main__':
    belts = None
    for _ in range(int(input())):
        query, *data = map(int, input().split())

        if query == 100:
            N, M, *data = data
            belts = [Belt() for _ in range(M)]
            size = N // M
            it1 = iter(data[:N])
            it2 = iter(data[N:])

            for belt in belts:
                for j in range(size):
                    box = next(it1)
                    weight = next(it2)
                    belt.append(Box(box, weight))
        if query == 200:
            w_max = data[0]
            print(step2(w_max))

        if query == 300:
            r_id = data[0]
            print(step3(r_id))

        if query == 400:
            f_id = data[0]
            print(step4(f_id))

        if query == 500:
            b_num = data[0]
            print(step5(b_num))