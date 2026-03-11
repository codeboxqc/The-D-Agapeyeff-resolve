#!/usr/bin/env python3
import math, random, time, sys, multiprocessing as mp

# ============================================================================
# DATA FROM YOUR GEN 69 BREAKTHROUGH
# ============================================================================
RAW_CIPHER = "756282859162916481649174858464747482848381638181747482626475838284917574658375757593636565816381758575756462829285746382757483816581848564856485856382726283628181728164637582816483638285816363630474819191846385846564856562946262859185917491727564657571658362647481828462826491819365626484849183857491816572748383858283646272626562837592726382827272838285847582818372846282838164757485816292000"

# Locked Grid Keys from your successful run
LOCKED_ROW_KEY = [11, 6, 12, 7, 10, 8, 13, 5, 4, 1, 2, 0, 9, 3]
LOCKED_COL_KEY = [2, 3, 6, 5, 10, 11, 9, 4, 8, 0, 12, 13, 7, 1]
GRID_SIZE = 14

# ============================================================================
# DICTIONARY HEALER ENGINE
# ============================================================================
def monster_score(text):
    score = 0.0
    
    # We are forcing the script to fix the specific errors in your snippet
    # LONDTO -> LONDON, LRDA -> AREA, NTHHR -> NORTH
    targets = {
        "COORDINATES": 30000,
        "LONDON":      25000,
        "NORTH":       20000,
        "SOUTH":       20000,
        "AREA":        15000,
        "POSITION":    15000,
        "REDUCED":     15000,
        "TENMILES":    10000
    }
    
    for word, weight in targets.items():
        if word in text:
            score += weight
        else:
            # Fuzzy match: Give points for partials to guide the Pi
            for length in range(len(word)-1, 3, -1):
                if word[:length] in text:
                    score += (length * 1000)
                    break
    
    # Penalty for "garbage" letters repeating (like the LLLL in your snippet)
    for char in "LXZH":
        if char*3 in text:
            score -= 5000
            
    return score

def decrypt(sq, indices):
    chars = []
    for c in LOCKED_COL_KEY:
        for r in LOCKED_ROW_KEY:
            pos = r * GRID_SIZE + c
            if pos < len(indices):
                chars.append(sq[indices[pos]])
    return "".join(chars)

def worker_task(args):
    indices, iterations = args
    # Start exactly where Gen 69 left off:
    curr_sq = list("VHELXBCPSNTOARDIYWKGFMZQU")
    curr_text = decrypt(curr_sq, indices)
    curr_score = monster_score(curr_text)
    
    best_state = (curr_score, "".join(curr_sq), curr_text)

    for _ in range(iterations):
        new_sq = curr_sq[:]
        # Try a small mutation
        a, b = random.sample(range(25), 2)
        new_sq[a], new_sq[b] = new_sq[b], new_sq[a]
        
        new_text = decrypt(new_sq, indices)
        score = monster_score(new_text)
        
        # Accept only if it improves or stays near the peak
        if score >= curr_score:
            curr_score, curr_sq = score, new_sq
            if score > best_state[0]:
                best_state = (score, "".join(new_sq), new_text)
                
    return best_state

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    rows, cols = ['6','7','8','9','0'], ['1','2','3','4','5']
    clean = RAW_CIPHER.replace(" ", "").replace("000", "")
    indices = [rows.index(clean[i])*5 + cols.index(clean[i+1]) for i in range(0, len(clean), 2)]
    
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    best_overall = -float('inf')
    
    print("[!] PHASE 3: THE FINAL HEALER")
    print("[*] Target: Fixing LONDTO and NTHHR...")
    
    try:
        while True:
            # Batch of 50k iterations per core
            results = pool.map(worker_task, [(indices, 50000)] * cores)
            
            for score, sq, text in results:
                if score > best_overall:
                    best_overall = score
                    print(f"\n[!!!] HEALED SNAPSHOT (Score: {score})")
                    print(f"Square: {sq}")
                    print(f"Text: {text}")
                    with open("FINAL_SOLVE.log", "a") as f:
                        f.write(f"Score: {score}\nSq: {sq}\nMsg: {text}\n\n")
            
            sys.stdout.write(f"\rCores: {cores} | Best: {best_overall} ")
            sys.stdout.flush()
    except KeyboardInterrupt:
        pool.terminate()
