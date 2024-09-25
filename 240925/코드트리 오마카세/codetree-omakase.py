import math
import sys
import heapq
from collections import defaultdict as dd

L = 0
guest_map = dd(int)
o_idx = 0
total_guest = 0
total_sushi = 0
guest_info = dd(lambda: GuestInfo())
waiting = {}
heap = []


class Sushi:
    def __init__(self, time_stamp, pos, guest_idx, eating_time):
        self.time_stamp = time_stamp
        self.pos = pos
        self.guest_index = guest_idx
        self.eating_time = eating_time


class GuestInfo:
    def __init__(self, time_stamp=0, pos=0, cnt=0, enter=0):
        self.time_stamp = time_stamp
        self.pos = pos
        self.cnt = cnt
        self.enter = enter


class HeapItem:
    def __init__(self, eating_time, guest_idx):
        self.eating_time = eating_time
        self.guest_idx = guest_idx

    def __lt__(self, other):
        return self.eating_time < other.eating_time


def get_eating_time(oi, sushi):
    guest_time = oi.time_stamp
    guest_pos = oi.pos
    sushi_time = sushi.time_stamp
    sushi_pos = sushi.pos

    if guest_time < sushi_time:
        if guest_pos < sushi_pos:
            time_diff = L - sushi_pos + guest_pos
        else:
            time_diff = guest_pos - sushi_pos
        return sushi_time + time_diff
    else:
        sushi_guest_pos = (sushi_pos + (guest_time - sushi_time)) % L
        if guest_pos < sushi_guest_pos:
            time_diff = L - sushi_guest_pos + guest_pos
        else:
            time_diff = guest_pos - sushi_guest_pos
        return guest_time + time_diff


def make_sushi(t, x, name):
    global o_idx, total_sushi

    guest_name = name

    if guest_name not in guest_map:
        guest_map[guest_name] = o_idx
        o_idx += 1

    guest_idx = guest_map[guest_name]

    sushi = Sushi(t, x, guest_idx, math.inf)

    if guest_idx not in guest_info:
        guest_info[guest_idx] = GuestInfo()
        waiting[guest_idx] = []

    if guest_info[guest_idx].enter == 0:
        waiting[guest_idx].append(sushi)
    else:
        eating_time = get_eating_time(guest_info[guest_idx], sushi)
        heapq.heappush(heap, HeapItem(eating_time, guest_idx))

    total_sushi += 1


def enter_guest(t, x, name, n):
    global o_idx, total_guest

    guest_name = name

    if guest_name not in guest_map:
        guest_map[guest_name] = o_idx
        o_idx += 1

    guest_idx = guest_map[guest_name]

    if guest_idx not in guest_info:
        guest_info[guest_idx] = GuestInfo()
        waiting[guest_idx] = []

    guest_info[guest_idx] = GuestInfo(t, x, n, 1)

    total_guest += 1

    if waiting[guest_idx]:
        for sushi in waiting[guest_idx]:
            eating_time = get_eating_time(guest_info[guest_idx], sushi)
            heapq.heappush(heap, HeapItem(eating_time, guest_idx))
        waiting[guest_idx] = []


def photo(t):
    global total_guest, total_sushi

    while heap:
        h = heap[0]
        if h.eating_time > t:
            break

        heapq.heappop(heap)
        total_sushi -= 1
        guest_info[h.guest_idx].cnt -= 1

        if guest_info[h.guest_idx].cnt == 0:
            total_guest -= 1

    print(f"{total_guest} {total_sushi}")


def main():
    global L

    L, Q = map(int, input().split())

    for _ in range(Q):
        query, *data = input().split()
        query = int(query)

        if query == 100:
            t, x, name = data
            t = int(t)
            x = int(x)
            make_sushi(t, x, name)
        elif query == 200:
            t, x, name, n = data
            t = int(t)
            x = int(x)
            n = int(n)
            enter_guest(t, x, name, n)
        elif query == 300:
            t = int(data[0])
            photo(t)


if __name__ == "__main__":
    main()