#!/usr/bin/env python3
import math
import random
import time
import sys
import os
import multiprocessing as mp
import signal

# ============================================================================
# DATA & CONSTRAINTS
# ============================================================================
RAW_CIPHER = "756282859162916481649174858464747482848381638181747482626475838284917574658375757593636565816381758575756462829285746382757483816581848564856485856382726283628181728164637582816483638285816363630474819191846385846564856562946262859185917491727564657571658362647481828462826491819365626484849183857491816572748383858283646272626562837592726382827272838285847582818372846282838164757485816292000"

LOCKED_ROW_KEY = [11, 6, 12, 7, 10, 8, 13, 5, 4, 1, 2, 0, 9, 3]
LOCKED_COL_KEY = [2, 3, 6, 5, 10, 11, 9, 4, 8, 0, 12, 13, 7, 1]
GRID_SIZE = 14

# ============================================================================
# EXPANDED LINGUISTIC MODEL
# ============================================================================
def get_quadgrams():
    q = {
        'TION': -2.1, 'NTHE': -2.2, 'THER': -2.3, 'THAT': -2.3, 'OFTH': -2.4,
        'IONS': -2.6, 'ANDT': -2.7, 'INGT': -2.7, 'HERE': -2.6, 'MENT': -2.7,
        'COOR': -3.1, 'ORDI': -3.2, 'RDIN': -3.3, 'DINA': -3.1, 'INAT': -3.0,
        'NATE': -2.9, 'ATES': -2.8, 'LAND': -3.4, 'NORT': -3.5, 'ORTH': -3.2,
        'ONLY': -3.1, 'NEAR': -3.4, 'WEST': -3.2, 'EAST': -3.2, 'CITY': -3.3
    }
    return q, -15.0

def monster_score(text, quadgrams, floor):
    score = 0.0
    for i in range(len(text) - 3):
        score += quadgrams.get(text[i:i+4], floor)
    
    # Priority Anchors
    anchors = ["COORDINATES", "POSITION", "DEGREES", "LONDON", "NORTH", "SOUTH", "EAST", "WEST", "ONLY"]
    for word in anchors:
        if word in text:
            score += 15000.0 
        else:
            for length in range(len(word)-1, 3, -1):
                if word[:length] in text:
                    score += (length * 1000.0)
                    break
    return score

# ============================================================================
# CORE ENGINE
# ============================================================================
def prepare_indices(raw_text):
    clean = raw_text.replace(" ", "").replace("000", "")
    rows, cols = ['6', '7', '8', '9', '0'], ['1', '2', '3', '4', '5']
    return [rows.index(clean[i]) * 5 + cols.index(clean[i+1]) for i in range(0, len(clean), 2)]

def decrypt(sq, indices):
    chars = []
    for c in LOCKED_COL_KEY:
        for r in LOCKED_ROW_KEY:
            pos = r * GRID_SIZE + c
            if pos < len(indices):
                chars.append(sq[indices[pos]])
    return "".join(chars)

def worker_task(args):
    indices, quadgrams, floor, iterations = args
    # YOUR PEAK SQUARE
    curr_sq = list("VHELXBCPSNTOARDIYWKGFMZQU")
    
    # FREEZE LOGIC: Lock letters that form our confirmed words
    # This prevents the hill-climber from destroying 'COORDINATES'
    protected_letters = "COORDINATESLON"
    protected_indices = [curr_sq.index(c) for c in protected_letters if c in curr_sq]
    available_indices = [i for i in range(25) if i not in protected_indices]
    
    # If we accidentally lock too many, allow one random swap from the full set
    if len(available_indices) < 2:
        available_indices = list(range(25))

    curr_text = decrypt(curr_sq, indices)
    curr_score = monster_score(curr_text, quadgrams, floor)
    best_state = (curr_score, "".join(curr_sq), curr_text)

    for _ in range(iterations):
        new_sq = curr_sq[:]
        
        # Swapping only the 'unprotected' letters
        a, b = random.sample(available_indices, 2)
        new_sq[a], new_sq[b] = new_sq[b], new_sq[a]
        
        new_text = decrypt(new_sq, indices)
        score = monster_score(new_text, quadgrams, floor)
        
        if score > curr_score:
            curr_score = score
            curr_sq = new_sq
            if score > best_state[0]:
                best_state = (score, "".join(new_sq), new_text)
    return best_state

def run():
    print("==========================================================")
    print("  ORANGE PI 5 MAX: RK3588 PROTECTED CRUNCHER")
    print("  FOCUS: LONDON / COORDINATES / GEOGRAPHY")
    print("==========================================================")
    
    indices = prepare_indices(RAW_CIPHER)
    quads, floor = get_quadgrams()
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    
    best_overall = -float('inf')
    gen = 1
    
    try:
        while True:
            # Frequent updates (100k) to keep the 8 cores synchronized
            jobs = [(indices, quads, floor, 100000) for _ in range(cores)]
            results = pool.map(worker_task, jobs)

            for score, sq_str, text in results:
                if score > best_overall:
                    best_overall = score
                    print(f"\n[!!!] NEW PEAK (Score: {score:.2f})")
                    print(f"Square: {sq_str}")
                    print(f"Snippet: {text[-60:]}") # Shows the end of the message
                    
                    with open("THE_FINAL_MESSAGE.log", "a") as f:
                        f.write(f"Gen: {gen} | Score: {score}\nSquare: {sq_str}\nText: {text}\n\n")

            sys.stdout.write(f"\rGen {gen} | Threads: {cores} | Best Score: {best_overall:.2f}")
            sys.stdout.flush()
            gen += 1
    except KeyboardInterrupt:
        pool.terminate()
        print("\n\nStopped. Progress saved to THE_FINAL_MESSAGE.log.")

if __name__ == "__main__":
    run()
