import sys



class Box:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight
        self.prev = None
        self.next = None

    def set_prev(self, prev):
        self.prev = prev

    def set_next(self, next):
        self.next = next

    def cut_prev(self):
        if self.prev is None:
            return
        self.prev.next = None
        self.prev = None

    def remove(self):
        if self.next:
            self.next.prev = self.prev
        if self.prev:
            self.prev.next = self.next
        self.prev = self.next = None


class Belt:
    def __init__(self):
        self.head = None
        self.tail = None
        self.boxes = dict()
        self.broken = False

    def add_box(self, box):
        self.boxes[box.id] = box
        if not self.head:
            self.head = box
        else:
            self.tail.set_next(box)
            box.set_prev(self.tail)
        self.tail = box

    def pop_box(self):
        box = self.head
        self.head = box.next
        if self.head:
            self.head.cut_prev()
        else:
            self.tail = None
        del self.boxes[box.id]
        return box


class Factory:
    def __init__(self, args):
        N, M, *data = args
        cnt = N // M
        self.belts = [Belt() for _ in range(M)]
        for idx, belt in enumerate(self.belts):
            for i in range(idx * cnt, (idx + 1) * cnt):
                belt.add_box(Box(data[i], data[i + N]))

    def load(self, max_weight):
        result = 0
        for belt in self.belts:
            if belt.head:
                box = belt.pop_box()
                if box.weight <= max_weight:
                    result += box.weight
                else:
                    belt.add_box(box)
        return result

    def remove(self, id):
        result = -1
        for belt in self.belts:
            if id in belt.boxes:
                box = belt.boxes[id]
                if belt.head == box:
                    belt.head = box.next
                if belt.tail == box:
                    belt.tail = box.prev
                box.remove()
                result = box.id
                del belt.boxes[id]
                break
        return result

    def find(self, id):
        result = -1
        for idx, belt in enumerate(self.belts):
            if id in belt.boxes:
                box = belt.boxes[id]
                if belt.head != box:
                    belt.head.set_prev(belt.tail)
                    belt.tail.set_next(belt.head)
                    belt.head = box
                    belt.tail = box.prev
                    box.cut_prev()
                result = idx + 1
                break
        return result

    def die(self, belt_id):
        result = -1
        idx = belt_id - 1
        if not self.belts[idx].broken:
            result = belt_id
            broken_belt = self.belts[idx]
            broken_belt.broken = True
            if broken_belt.boxes:
                for i in range(idx + 1, idx + len(self.belts)):
                    next_belt = self.belts[i % len(self.belts)]
                    if not next_belt.broken:
                        next_belt.boxes.update(broken_belt.boxes)
                        broken_belt.boxes.clear()
                        if next_belt.head:
                            broken_belt.tail.set_next(next_belt.head)
                            next_belt.head.set_prev(broken_belt.tail)
                        else:
                            next_belt.tail = broken_belt.tail
                        next_belt.head = broken_belt.head
                        broken_belt.head = broken_belt.tail = None
                        break
        return result


if __name__ == "__main__":
    Q = int(input())
    _, *args = map(int, input().split())
    factory = Factory(args)
    operations = {
        200: factory.load,
        300: factory.remove,
        400: factory.find,
        500: factory.die,
    }
    for _ in range(Q - 1):
        query, arg = map(int, input().split())
        print(operations[query](arg))