 #!/usr/bin/env python3
import math, random, time, sys, multiprocessing as mp

# ============================================================================
# DATA & CONSTRAINTS (96K BREAKTHROUGH)
# ============================================================================
RAW_CIPHER = "756282859162916481649174858464747482848381638181747482626475838284917574658375757593636565816381758575756462829285746382757483816581848564856485856382726283628181728164637582816483638285816363630474819191846385846564856562946262859185917491727564657571658362647481828462826491819365626484849183857491816572748383858283646272626562837592726382827272838285847582818372846282838164757485816292000"

LOCKED_ROW_KEY = [11, 6, 12, 7, 10, 8, 13, 5, 4, 1, 2, 0, 9, 3]
LOCKED_COL_KEY = [2, 3, 6, 5, 10, 11, 9, 4, 8, 0, 12, 13, 7, 1]
GRID_SIZE = 14

# ============================================================================
# PHASE 7 ULTRA-SCORING
# ============================================================================
def monster_score(text):
    score = 0.0
    # Massive weights to force the final letters to snap into place
    targets = {
        "COORDINATES": 100000, 
        "CITYLONDON":  80000,
        "AREANORTH":   70000,
        "POSITION":    60000,
        "DEGREES":     50000
    }
    
    for word, weight in targets.items():
        if word in text:
            score += weight
        else:
            # Fuzzy match to pull the "M" ghosts toward English words
            for length in range(len(word)-1, 4, -1):
                if word[:length] in text:
                    score += (length * 5000)
                    break
        
    # PENALTY: Aggressively target the 'M' and 'P' ghosts from your 96k peak
    if "AREANETM" in text: score -= 30000
    if "MCNP" in text:     score -= 30000
    if "MMMM" in text:     score -= 50000
            
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
    # Starting square from your 96,000.0 Peak
    curr_sq = list("UMELFVCQSNTOARDIPWHKBYZXG")
    
    # LOCK these 14 letters - they are 100% correct for COORDINATES and LONDON
    protected_letters = "COORDINATESLON"
    protected_indices = [curr_sq.index(c) for c in protected_letters if c in curr_sq]
    available_indices = [i for i in range(25) if i not in protected_indices]

    curr_text = decrypt(curr_sq, indices)
    curr_score = monster_score(curr_text)
    best_state = (curr_score, "".join(curr_sq), curr_text)

    for _ in range(iterations):
        new_sq = curr_sq[:]
        # TINY MUTATIONS: Only swap the 11 unknown letters
        a, b = random.sample(available_indices, 2)
        new_sq[a], new_sq[b] = new_sq[b], new_sq[a]
        
        new_text = decrypt(new_sq, indices)
        score = monster_score(new_text)
        
        if score >= curr_score:
            curr_score, curr_sq = score, new_sq
            if score > best_state[0]:
                best_state = (score, "".join(new_sq), new_text)
    return best_state

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    rows, cols = ['6','7','8','9','0'], ['1','2','3','4','5']
    clean = RAW_CIPHER.replace(" ", "").replace("000", "")
    indices = [rows.index(clean[i])*5 + cols.index(clean[i+1]) for i in range(0, len(clean), 2)]
    
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    best_overall = -float('inf')
    
    print("==========================================================")
    print("  ORANGE PI 5 MAX: RK3588 PHASE 7 TOTAL SOLVE")
    print("  TARGETING: PURGING 'M' GHOSTS FOR 100K SCORE")
    print("==========================================================")
    
    try:
        while True:
            # Short, high-intensity batches (50k) to force faster sync
            results = pool.map(worker_task, [(indices, 50000)] * cores)
            
            for score, sq, text in results:
                if score > best_overall:
                    best_overall = score
                    print(f"\n[!!!] FINAL SOLVE PEAK (Score: {score})")
                    print(f"Square: {sq}")
                    print(f"Text Snippet: ...{text[-80:]}")
                    
                    with open("THE_FINAL_MESSAGE.log", "a") as f:
                        f.write(f"Score: {score}\nSq: {sq}\nMsg: {text}\n\n")
            
            sys.stdout.write(f"\rCores: {cores} | Best: {best_overall} ")
            sys.stdout.flush()
    except KeyboardInterrupt:
        pool.terminate()
