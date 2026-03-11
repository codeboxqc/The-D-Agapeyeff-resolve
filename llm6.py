 #!/usr/bin/env python3
import math, random, time, sys, multiprocessing as mp

# ============================================================================
# DATA & CONSTRAINTS (74K BREAKTHROUGH)
# ============================================================================
RAW_CIPHER = "756282859162916481649174858464747482848381638181747482626475838284917574658375757593636565816381758575756462829285746382757483816581848564856485856382726283628181728164637582816483638285816363630474819191846385846564856562946262859185917491727564657571658362647481828462826491819365626484849183857491816572748383858283646272626562837592726382827272838285847582818372846282838164757485816292000"

LOCKED_ROW_KEY = [11, 6, 12, 7, 10, 8, 13, 5, 4, 1, 2, 0, 9, 3] #
LOCKED_COL_KEY = [2, 3, 6, 5, 10, 11, 9, 4, 8, 0, 12, 13, 7, 1] #
GRID_SIZE = 14

def monster_score(text):
    score = 0.0
    # Massive rewards for finally fixing the "Z" words
    targets = {
        "COORDINATES": 80000,
        "LONDON":      60000,
        "NORTH":       50000,
        "SOUTH":       50000,
        "CITY":        40000,
        "AREA":        35000,
    }
    
    for word, weight in targets.items():
        if word in text: score += weight
        else:
            for length in range(len(word)-1, 3, -1):
                if word[:length] in text:
                    score += (length * 4000)
                    break

    # THE Z-PENALTY: Aggressively punish 'Z' in high-frequency spots
    # In your 74k run, 'Z' is appearing in 'LRDANETZZ'
    if "Z" in text:
        score -= (text.count("Z") * 5000)
    
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
    # Starting from your 74,000.0 peak square
    curr_sq = list("UZELFVCQSNTOARDIPWHKBYMXG")
    
    # LOCK these - they are almost certainly correct
    protected_letters = "COORDINATESLON"
    protected_indices = [curr_sq.index(c) for c in protected_letters if c in curr_sq]
    
    # TARGET the 'Z' specifically for movement
    z_index = curr_sq.index("Z")
    available_indices = [i for i in range(25) if i not in protected_indices]

    curr_text = decrypt(curr_sq, indices)
    curr_score = monster_score(curr_text)
    best_state = (curr_score, "".join(curr_sq), curr_text)

    for _ in range(iterations):
        new_sq = curr_sq[:]
        # FORCE the 'Z' to swap more often to find its proper low-freq home
        if random.random() > 0.5:
            a, b = z_index, random.choice(available_indices)
        else:
            a, b = random.sample(available_indices, 2)
            
        new_sq[a], new_sq[b] = new_sq[b], new_sq[a]
        
        new_text = decrypt(new_sq, indices)
        score = monster_score(new_text)
        
        if score >= curr_score:
            curr_score, curr_sq = score, new_sq
            if score > best_state[0]:
                best_state = (score, "".join(new_sq), new_text)
                
    return best_state

if __name__ == "__main__":
    rows, cols = ['6','7','8','9','0'], ['1','2','3','4','5']
    clean = RAW_CIPHER.replace(" ", "").replace("000", "")
    indices = [rows.index(clean[i])*5 + cols.index(clean[i+1]) for i in range(0, len(clean), 2)]
    
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    best_overall = -float('inf')
    
    try:
        while True:
            # Short, intense bursts (50k) to allow more frequent global updates
            results = pool.map(worker_task, [(indices, 50000)] * cores)
            for score, sq, text in results:
                if score > best_overall:
                    best_overall = score
                    print(f"\n[!!!] 74K BREAKOUT (Score: {score})\nSquare: {sq}\nText: ...{text[-80:]}")
            sys.stdout.write(f"\rRK3588 Cracking... Best: {best_overall} ")
            sys.stdout.flush()
    except KeyboardInterrupt:
        pool.terminate()
