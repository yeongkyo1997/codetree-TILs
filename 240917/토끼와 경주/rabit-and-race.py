class Rabbit:
    def __init__(self, pid, d_i):
        self.pid = pid        # Unique identifier
        self.d_i = d_i        # Movement distance
        self.row = 1          # Current row position
        self.col = 1          # Current column position
        self.total_jumps = 0  # Total number of jumps made
        self.score = 0        # Total score accumulated

def move(pos0, delta, limit, distance):
    pos0 -= 1  # Convert to 0-based index
    period = 2 * (limit - 1)
    pos = (pos0 + delta * distance) % period
    if pos >= limit:
        pos = period - pos
    return pos + 1  # Convert back to 1-based index

import sys
import threading

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    Q = int(sys.stdin.readline())
    commands = []
    for _ in range(Q):
        commands.append(sys.stdin.readline().strip())

    rabbits = {}
    rabbit_list = []
    N = M = P = 0
    moved_rabbits_set = set()

    for cmd in commands:
        tokens = cmd.split()
        cmd_type = int(tokens[0])
        if cmd_type == 100:
            # Race preparation
            N = int(tokens[1])
            M = int(tokens[2])
            P = int(tokens[3])
            idx = 4
            for _ in range(P):
                pid_i = int(tokens[idx])
                d_i = int(tokens[idx +1])
                idx +=2
                rabbit = Rabbit(pid_i, d_i)
                rabbits[pid_i] = rabbit
                rabbit_list.append(rabbit)
        elif cmd_type ==200:
            # Race progress
            K = int(tokens[1])
            S = int(tokens[2])
            for _ in range(K):
                # Select the rabbit with highest priority
                rabbit = min(rabbit_list, key=lambda r: (r.total_jumps, r.row + r.col, r.row, r.col, r.pid))
                # Mark that this rabbit has moved
                moved_rabbits_set.add(rabbit.pid)
                # For each direction, compute final position
                positions = []
                d_i = rabbit.d_i
                r0 = rabbit.row
                c0 = rabbit.col
                # Up
                new_row = move(r0, -1, N, d_i)
                positions.append((-(new_row + c0), -new_row, -c0, new_row, c0))
                # Down
                new_row = move(r0, +1, N, d_i)
                positions.append((-(new_row + c0), -new_row, -c0, new_row, c0))
                # Left
                new_col = move(c0, -1, M, d_i)
                positions.append((-(r0 + new_col), -r0, -new_col, r0, new_col))
                # Right
                new_col = move(c0, +1, M, d_i)
                positions.append((-(r0 + new_col), -r0, -new_col, r0, new_col))
                # Select position with highest priority
                positions.sort()
                _, _, _, new_r, new_c = positions[0]
                # Update rabbit's position and total jumps
                rabbit.row = new_r
                rabbit.col = new_c
                rabbit.total_jumps +=1
                # All other rabbits gain (r_i + c_i) points
                score_increase = rabbit.row + rabbit.col
                for other_rabbit in rabbit_list:
                    if other_rabbit.pid != rabbit.pid:
                        other_rabbit.score += score_increase
        elif cmd_type ==300:
            # Change movement distance
            pid_t = int(tokens[1])
            L = int(tokens[2])
            if pid_t in rabbits:
                rabbits[pid_t].d_i *= L
        elif cmd_type ==400:
            # Select the best rabbit
            # Among rabbits that moved, select the one with highest priority
            moved_rabbits = [rabbits[pid] for pid in moved_rabbits_set]
            if moved_rabbits:
                best_rabbit = min(moved_rabbits, key=lambda r: (-(r.row + r.col), -r.row, -r.col, -r.pid))
                best_rabbit.score += S  # S was from the last command 200
            # Output the highest score among all rabbits
            max_score = max(rabbit.score for rabbit in rabbit_list)
            print(max_score)
            # No more commands after 400, so we can break
            break

threading.Thread(target=main).start()