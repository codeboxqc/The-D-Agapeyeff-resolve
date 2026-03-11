 #!/usr/bin/env python3
import math, random, time, sys, multiprocessing as mp

# ============================================================================
# DATA & CONSTRAINTS (GEN 69 + 60K BREAKTHROUGH)
# ============================================================================
RAW_CIPHER = "756282859162916481649174858464747482848381638181747482626475838284917574658375757593636565816381758575756462829285746382757483816581848564856485856382726283628181728164637582816483638285816363630474819191846385846564856562946262859185917491727564657571658362647481828462826491819365626484849183857491816572748383858283646272626562837592726382827272838285847582818372846282838164757485816292000"

LOCKED_ROW_KEY = [11, 6, 12, 7, 10, 8, 13, 5, 4, 1, 2, 0, 9, 3] #
LOCKED_COL_KEY = [2, 3, 6, 5, 10, 11, 9, 4, 8, 0, 12, 13, 7, 1] #
GRID_SIZE = 14

# ============================================================================
# PHASE 5 SCORING ENGINE
# ============================================================================
def monster_score(text):
    score = 0.0
    
    # Primary anchors with maximum weights to maintain stability
    targets = {
        "COORDINATES": 60000,
        "LONDON":      50000,
        "NORTH":       40000,
        "SOUTH":       40000,
        "CITY":        35000,
        "AREA":        30000,
        "COAST":       25000,
        "DEGREES":     25000,
        "POSITION":    20000
    }
    
    for word, weight in targets.items():
        if word in text:
            score += weight
        else:
            # High-reward fuzzy matching to guide the RK3588 toward corrections
            for length in range(len(word)-1, 3, -1):
                if word[:length] in text:
                    score += (length * 3500)
                    break

    # TARGETED PENALTY: Resolving the "V" and "M" errors
    # In your 60k peak, V often appeared where C or I should be (e.g., VLONDTO)
    if "VLOND" in text: score -= 20000
    if "NMAP" in text:  score -= 15000
    
    # Impossible clusters identified in recent snippets
    for cluster in ["MMM", "VVV", "VQA", "MRD", "LLLL"]:
        if cluster in text:
            score -= 15000
            
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
    # Starting from your 60,000.0 peak square
    curr_sq = list("GMELPYCXSNTOARDIVUWBKHZQF")
    
    # PROTECTED MUTATION: Lock confirmed letters to focus power on the errors
    # These letters are essential for "COORDINATES" and "LONDON"
    protected_letters = "COORDINATESLON"
    protected_indices = [curr_sq.index(c) for c in protected_letters if c in curr_sq]
    available_indices = [i for i in range(25) if i not in protected_indices]

    if len(available_indices) < 2:
        available_indices = list(range(25))

    curr_text = decrypt(curr_sq, indices)
    curr_score = monster_score(curr_text)
    best_state = (curr_score, "".join(curr_sq), curr_text)

    for _ in range(iterations):
        new_sq = curr_sq[:]
        # Only swap letters that are NOT part of our protected anchors
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
# MAIN RUNTIME
# ============================================================================
if __name__ == "__main__":
    rows, cols = ['6','7','8','9','0'], ['1','2','3','4','5']
    clean = RAW_CIPHER.replace(" ", "").replace("000", "")
    indices = [rows.index(clean[i])*5 + cols.index(clean[i+1]) for i in range(0, len(clean), 2)]
    
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    best_overall = -float('inf')
    
    print("==========================================================")
    print("  ORANGE PI 5 MAX: RK3588 PHASE 5 RECTIFIER")
    print("  TARGET: REMOVING V/M SUBSTITUTION GHOSTS")
    print("==========================================================")
    
    try:
        while True:
            # 100k iterations per core to balance thermal load and synchronization
            results = pool.map(worker_task, [(indices, 100000)] * cores)
            
            for score, sq, text in results:
                if score > best_overall:
                    best_overall = score
                    print(f"\n[!!!] NEW PEAK (Score: {score})")
                    print(f"Square: {sq}")
                    print(f"Snippet: ...{text[-80:]}")
                    
                    with open("FINAL_SOLVE.log", "a") as f:
                        f.write(f"Score: {score}\nSq: {sq}\nMsg: {text}\n\n")
            
            sys.stdout.write(f"\rRK3588 Cores: {cores} | Best Score: {best_overall} ")
            sys.stdout.flush()
    except KeyboardInterrupt:
        pool.terminate()
