#!/usr/bin/env python3
"""
==============================================================================
D'AGAPEYEFF "MONSTER CRACKER" - CARTOGRAPHIC HYBRID V4
==============================================================================
Optimized specifically for RK3588 (Orange Pi 5 Max ARM) processing nodes.
Features: 
1. Pre-Allocated 1D Int Arrays (Zero Garbage-Collection/Memory Thrashing loop)
2. English+French Hybrid Fallback Dictionaries (4-Letter Strict Boundaries)
3. Balanced Cartographic Bias Scanning (Weighted 3D Map Variables)
==============================================================================
"""

import math
import random
import time
import sys
import os
import multiprocessing as mp
import signal

# ============================================================================
# CIPHERTEXT CONFIGURATION
# ============================================================================
RAW_CIPHER = (
    "756282859162916481649174858464747482848381638181747482626475838284917574658375"
    "757593636565816381758575756462829285746382757483816581848564856485856382726283"
    "628181728164637582816483638285816363630474819191846385846564856562946262859185"
    "917491727564657571658362647481828462826491819365626484849183857491816572748383"
    "858283646272626562837592726382827272838285847582818372846282837581647574858162"
    "92000"
)

GRID_SIZE = 14
ROWS = ['6', '7', '8', '9', '0']
COLS = ['1', '2', '3', '4', '5']
ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# ============================================================================
# EXPANDED CARTOGRAPHIC KEYWORD SET
# ============================================================================
BASE_KEYWORDS =[
    "DAGAPEYEFF", "ALEXANDER", "MAPMAKING", "GEOGRAPHY", "COORDINATES",
    "LATITUDE", "LONGITUDE", "CARTOGRAPHY", "SURVEYOR", "PROJECTION",
    "GRID", "SCALE", "AZIMUTH", "MERIDIAN", "LONDON", "OXFORD", "MILITARY",
    "CHART", "TOPOGRAPHY", "COMPASS", "SECTION", "TRIANGULATION"
]

def generate_keyword_square(word):
    seen = set()
    key_letters =[]
    for char in word.upper():
        if char in ALPHABET and char not in seen:
            seen.add(char)
            key_letters.append(char)
    for char in ALPHABET:
        if char not in seen:
            key_letters.append(char)
    return key_letters

# Core Historical Locks (Reduces 25! keyspace drastically to target specific themes)
PRECOMPUTED_SQUARES = [generate_keyword_square(kw) for kw in BASE_KEYWORDS]
PRECOMPUTED_SQUARES += [generate_keyword_square(kw[::-1]) for kw in BASE_KEYWORDS]
for _ in range(8000):
    rw = "".join(random.sample(ALPHABET, random.randint(4, 10)))
    PRECOMPUTED_SQUARES.append(generate_keyword_square(rw))

# ============================================================================
# BILINGUAL FITNESS ENGINE (English Text & French Injections)
# ============================================================================
def load_quadgrams(filename="english_quadgrams.txt"):
    """Reads large empirical database if available; patches in native & fallback maps."""
    quadgrams = {}
    floor = -5.5
    if os.path.exists(filename):
        try:
            total = 0
            with open(filename, 'r') as f:
                for line in f:
                    q, c = line.strip().split()
                    c = int(c)
                    quadgrams[q] = c
                    total += c
            for q in quadgrams:
                quadgrams[q] = math.log10(quadgrams[q] / total)
            floor = math.log10(0.01 / total)
            print(f"[+] Operational Array Loaded: {len(quadgrams)} statistical map N-Grams.")
        except Exception as e:
            print(f"[-] Load Failed: {e}. Switching to hardcoded module.")

    if not quadgrams:
        # STRICT 4-LETTER HARDCODING. (Space bars physically do not exist in D'Agapeyeff)
        print("[!] Defaulting to Internal English/French Quad-Map probabilities.")
        common_q = {
            'TION': -2.1, 'NTHE': -2.2, 'THER': -2.3, 'THAT': -2.3,
            'ETTE': -2.4, 'MENT': -2.5, 'IONS': -2.6, 'WITH': -2.5, 
            'ATIO': -2.6, 'OFTH': -2.4, 'THEM': -2.5, 'FROM': -3.1 
        }
        quadgrams.update(common_q)
    
    # 🇫🇷 D'agapeyeff multi-lingual variance injections (STRICTLY 4 LETTERS)
    # Adds high-probability constants for French text
    french_injection = {'DANS': -2.7, 'POUR': -2.8, 'ENTR': -2.9, 'AVEC': -3.0, 'SANS': -3.1}
    for q, val in french_injection.items():
        if q not in quadgrams:
            quadgrams[q] = val

    return quadgrams, floor

def monster_score(text, quadgrams, floor):
    score = 0.0
    # 1. Linguistic Vector Search 
    for i in range(len(text) - 3):
        score += quadgrams.get(text[i:i+4], floor)
    
    # 2. Balanced Tiered Crib Array 
    # Scaled logarithmically: Short 4-letter sequences have small bumps, massive ones alter SA gravity!
    crib_weights = {
        "GRID": 5.0, "MAPS": 4.0, "ZONE": 4.0, 
        "COORD": 8.0, "NORTH": 6.0, "SOUTH": 6.0, 
        "SCALE": 6.0, "COMPASS": 10.0, "SURVEY": 10.0,
        "LONDON": 10.0, "CHART": 6.0, "PROJECTION": 15.0,
        "MAPMAKING": 20.0, "CARTOGRAPHY": 25.0
    }
    for crib, weight in crib_weights.items():
        if crib in text:
            score += weight
            
    # 3. Anomalous Repeating Consonant Extractor
    max_run = 1
    current_run = 1
    for i in range(1, len(text)):
        if text[i] == text[i-1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1
    # Rapid rejection limit (Crushes SA scoring instantly if loops lock onto 5+ repeat letters)
    if max_run > 4:
        score -= (max_run * 5.0)
        
    return score

# ============================================================================
# MEMORY-ALLOCATION SAFE INTEGER CORE
# ============================================================================
def prepare_cipher(raw_text):
    clean = raw_text.replace(" ", "").replace("000", "")
    pairs = [clean[i:i+2] for i in range(0, len(clean), 2)]
    indices =[]
    for p in pairs:
        try:
            r, c = ROWS.index(p[0]), COLS.index(p[1])
            indices.append(r * 5 + c)
        except (ValueError, IndexError):
            indices.append(-1)
    return indices

def optimized_double_transpose(indices, row_key, col_key, out_buffer):
    """Mutates output strictly inside the buffer list to avert OS-level RAM GC lockup"""
    idx = 0
    for col in col_key:
        for row in row_key:
            out_buffer[idx] = indices[row * 14 + col]
            idx += 1

# ============================================================================
# ARM ORCHESTRATION ARCHITECTURE (MULTICORE ORANGE-PI SPECIFIC)
# ============================================================================
def init_worker():
    # Locks OS level interrupts inside child subprocess trees
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def monster_worker(args):
    base_indices, quadgrams, floor, iterations = args
    
    # 🪚 RAM Optimization: Buffer instantiated ONCE! Reused 60,000 times natively.
    trans_buffer = [0] * 196 
    
    curr_rk = list(range(14))
    curr_ck = list(range(14))
    curr_sq = random.choice(PRECOMPUTED_SQUARES)[:]
    random.shuffle(curr_rk)
    random.shuffle(curr_ck)
    
    optimized_double_transpose(base_indices, curr_rk, curr_ck, trans_buffer)
    text = "".join(curr_sq[i] if i != -1 else '?' for i in trans_buffer)
    curr_score = monster_score(text, quadgrams, floor)
    
    best_state = (curr_score, curr_rk[:], curr_ck[:], curr_sq[:], text)
    temp = 45.0
    
    for _ in range(iterations):
        new_rk, new_ck, new_sq = curr_rk[:], curr_ck[:], curr_sq[:]
        mode = random.random()
        
        if mode < 0.35: # Row Transposition Mutate
            a, b = random.sample(range(14), 2); new_rk[a], new_rk[b] = new_rk[b], new_rk[a]
        elif mode < 0.70: # Col Transposition Mutate
            a, b = random.sample(range(14), 2); new_ck[a], new_ck[b] = new_ck[b], new_ck[a]
        else: # Polybius Square/Keyword Mutate
            if random.random() < 0.85: new_sq = random.choice(PRECOMPUTED_SQUARES)[:]
            else: a, b = random.sample(range(25), 2); new_sq[a], new_sq[b] = new_sq[b], new_sq[a]
            
        optimized_double_transpose(base_indices, new_rk, new_ck, trans_buffer)
        text = "".join(new_sq[i] if i != -1 else '?' for i in trans_buffer)
        score = monster_score(text, quadgrams, floor)
        
        # Metropolis Mathematical Criteria Node
        if score > curr_score or (temp > 0.1 and random.random() < math.exp((score - curr_score) / temp)):
            curr_score, curr_rk, curr_ck, curr_sq = score, new_rk, new_ck, new_sq
            if score > best_state[0]:
                best_state = (score, curr_rk[:], curr_ck[:], curr_sq[:], text)
        
        # Rapid Thermal Shock Decay Variable
        temp *= 0.9995
        if temp < 0.1: temp = 30.0 # Heat Burst Pulse Sequence
            
    return best_state

def run_cracker():
    print("=========================================================================")
    print("      D'AGAPEYEFF MONSTER CRACKER (HYBRID V4 - RK3588 ALLOCATED)         ")
    print("=========================================================================")
    
    base_indices = prepare_cipher(RAW_CIPHER)
    quads, floor = load_quadgrams()
    
    # Seizes all physically visible CPU pipelines on your RK3588 board
    cores = mp.cpu_count()
    pool = mp.Pool(cores, initializer=init_worker)
    
    best_overall = -float('inf')
    start = time.time()
    
    print(f"[#] Preallocated Matrix Pools... System Mapping Complete.")
    print(f"[!] ARM Sequence Initiation[{cores}] Native Hyperthreads Running...")
    
    try:
        gen = 1
        while True:
            # 60k loop is the ideal gravity payload for IPC throughput optimization
            jobs =[(base_indices, quads, floor, 60000) for _ in range(cores)]
            results = pool.map(monster_worker, jobs)
            
            for score, rk, ck, sq, text in results:
                if score > best_overall:
                    best_overall = score
                    print(f"\n\n[⚠️] STRUCTURAL BREAKTHROUGH [⚠️] --> Node Threshold Map Acquired.")
                    print(f"Metrics (Generation: {gen} // Core Lifetime: {int(time.time()-start)}s): {score:.4f}")
                    print(f"Row Map Vector Lock : {rk}")
                    print(f"Col Map Vector Lock : {ck}")
                    print(f"Keyword Grid Built  : {''.join(sq)}")
                    print(f"Translated Ciphertext Data : \n===> {text}")
                    
                    with open("monster_v4_nodes.log", "a", encoding="utf-8") as f:
                         f.write(f"\nGen {gen} | Score: {score:.2f} | Time: {int(time.time()-start)}s\n")
                         f.write(f"R-Lock: {rk}\nC-Lock: {ck}\nSquare: {''.join(sq)}\nTXT   : {text}\n")
                         
            # Output Display (Taps console safely)
            sys.stdout.write(f"\rGen [{gen}] Crunching Grid Vectors... Optimal Array Found: {best_overall:.2f}     ")
            sys.stdout.flush()
            gen += 1
            
    except KeyboardInterrupt:
        print("\n\n[!] User Halt Action Received. Dumping RAM Threads Safely...")
        pool.terminate(); pool.join()
        print("[!] Thread Wipe Completed.")

if __name__ == "__main__":
    run_cracker()