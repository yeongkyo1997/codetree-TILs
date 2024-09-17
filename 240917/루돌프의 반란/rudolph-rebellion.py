from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class Santa:
    number: int
    r: int
    c: int
    active: bool = True
    stunned_until_turn: int = 0
    score: int = 0

def main():
    import sys
    sys.setrecursionlimit(10000)
    
    N, M, P, C, D = map(int, sys.stdin.readline().split())
    Rr, Rc = map(int, sys.stdin.readline().split())
    
    santas: Dict[int, Santa] = {}
    positions: Dict[Tuple[int, int], int] = {}
    
    for _ in range(P):
        Pn, Sr, Sc = map(int, sys.stdin.readline().split())
        santas[Pn] = Santa(number=Pn, r=Sr, c=Sc)
        positions[(Sr, Sc)] = Pn
    
    rudolph_r, rudolph_c = Rr, Rc
    
    # Directions for Rudolph: up, up-right, right, down-right, down, down-left, left, up-left
    rudolph_dir_order = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
    
    # Directions for Santas: up, right, down, left
    santa_dir_order = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def push_santa(santa_num: int, dr: int, dc: int, distance: int):
        nonlocal santas, positions, N
        santa = santas[santa_num]
        if not santa.active:
            return
        final_r = santa.r + dr * distance
        final_c = santa.c + dc * distance
        
        # Check if final position is within the grid
        if not (1 <= final_r <= N and 1 <= final_c <= N):
            # Santa is eliminated
            santa.active = False
            del positions[(santa.r, santa.c)]
            return
        
        # Check if another Santa is on the final cell
        if (final_r, final_c) in positions:
            other_santa_num = positions[(final_r, final_c)]
            push_santa(other_santa_num, dr, dc, 1)
        
        # After pushing, check if the cell is free
        if (final_r, final_c) in positions:
            # If still occupied, cannot push further; Santa remains in place
            return
        
        # Move the Santa to the final position
        del positions[(santa.r, santa.c)]
        santa.r = final_r
        santa.c = final_c
        positions[(final_r, final_c)] = santa_num
    
    for turn in range(1, M + 1):
        # 1. Rudolph moves
        # Find closest active Santa(s)
        min_dist = float('inf')
        target_santas = []
        for santa in santas.values():
            if santa.active:
                dist = (santa.r - rudolph_r)**2 + (santa.c - rudolph_c)**2
                if dist < min_dist:
                    min_dist = dist
                    target_santas = [santa]
                elif dist == min_dist:
                    target_santas.append(santa)
        
        if not target_santas:
            # No active Santas left
            break
        
        # Select the Santa with largest r, then largest c
        target_santas.sort(key=lambda x: (-x.r, -x.c))
        target = target_santas[0]
        
        # Determine the direction to move
        best_dir = None
        best_dist = float('inf')
        for dr, dc in rudolph_dir_order:
            new_r = rudolph_r + dr
            new_c = rudolph_c + dc
            if not (1 <= new_r <= N and 1 <= new_c <= N):
                continue
            dist = (target.r - new_r)**2 + (target.c - new_c)**2
            if dist < best_dist:
                best_dist = dist
                best_dir = (dr, dc)
        
        if best_dir:
            rudolph_r += best_dir[0]
            rudolph_c += best_dir[1]
            rudolph_move_dir = best_dir
        else:
            # Rudolph cannot move (should not happen)
            rudolph_move_dir = (0, 0)
        
        # 2. Handle collision after Rudolph moved
        collided_santa_num = positions.get((rudolph_r, rudolph_c))
        if collided_santa_num:
            collided_santa = santas[collided_santa_num]
            if collided_santa.active:
                # Collision occurs
                collided_santa.score += C
                collided_santa.stunned_until_turn = turn + 2
                push_santa(collided_santa_num, rudolph_move_dir[0], rudolph_move_dir[1], C)
        
        # 3. Santas move
        for p in range(1, P + 1):
            santa = santas.get(p)
            if santa and santa.active and turn >= santa.stunned_until_turn:
                # Determine possible moves
                possible_moves = []
                current_dist = (santa.r - rudolph_r)**2 + (santa.c - rudolph_c)**2
                for idx, (dr, dc) in enumerate(santa_dir_order):
                    new_r = santa.r + dr
                    new_c = santa.c + dc
                    if not (1 <= new_r <= N and 1 <= new_c <= N):
                        continue
                    if (new_r, new_c) in positions:
                        continue
                    new_dist = (new_r - rudolph_r)**2 + (new_c - rudolph_c)**2
                    if new_dist < current_dist:
                        possible_moves.append((idx, dr, dc, new_r, new_c))
                
                if possible_moves:
                    # Sort by direction priority: up, right, down, left
                    possible_moves.sort(key=lambda x: x[0])
                    _, dr_move, dc_move, new_r, new_c = possible_moves[0]
                    
                    # Move the Santa
                    del positions[(santa.r, santa.c)]
                    santa.r = new_r
                    santa.c = new_c
                    positions[(new_r, new_c)] = p
                    
                    # Check for collision with Rudolph
                    if (new_r, new_c) == (rudolph_r, rudolph_c):
                        # Collision occurs
                        santa.score += D
                        santa.stunned_until_turn = turn + 2
                        # Push in opposite direction
                        opp_dr = -dr_move
                        opp_dc = -dc_move
                        push_santa(p, opp_dr, opp_dc, D)
        
        # 4. Add 1 point to all active Santas
        for santa in santas.values():
            if santa.active:
                santa.score += 1
        
        # 5. Check if all Santas are eliminated
        all_eliminated = all(not santa.active for santa in santas.values())
        if all_eliminated:
            break
    
    # Prepare the output
    output = []
    for p in range(1, P + 1):
        santa = santas.get(p)
        if santa:
            output.append(str(santa.score))
        else:
            output.append('0')
    
    print(' '.join(output))

if __name__ == "__main__":
    main()