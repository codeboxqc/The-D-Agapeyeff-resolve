#!/usr/bin/env python3
"""
==============================================================================
D'AGAPEYEFF ULTIMATE ASSAULT - MAXIMUM OPTIMIZATION 
==============================================================================
CRITICAL FIXES APPLIED:
✓ Fixed UnboundLocalError crash on early KeyboardInterrupt.
✓ Fixed multiprocessing module-level resource leak (Square generation).
✓ Massive Speed Optimization: C-level byte translation instead of string join.
✓ CPU Optimization: Early exit for garbage scores skips expensive crib checks.
==============================================================================
"""

import numpy as np
import math
import random
import time
import sys
import os
import multiprocessing as mp

# ============================================================================
# CONFIGURATION
# ============================================================================
RAW_CIPHER = (
    "756282859162916481649174858464747482848381638181747482626475838284917574658375"
    "757593636565816381758575756462829285746382757483816581848564856485856382726283"
    "628181728164637582816483638285816363630474819191846385846564856562946262859185"
    "917491727564657571658362647481828462826491819365626484849183857491816572748383"
    "858283646272626562837592726382827272838285847582818372846282837581647574858162"
    "92000"
)

ROWS = ['6', '7', '8', '9', '0']
COLS =['1', '2', '3', '4', '5']
ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

BASE_KEYWORDS =[
    # Cartography
    "DAGAPEYEFF", "ALEXANDER", "MAPMAKING", "CARTOGRAPHY", "GEOGRAPHY",
    "LATITUDE", "LONGITUDE", "SURVEYOR", "PROJECTION", "COORDINATES",
    "GRID", "SCALE", "AZIMUTH", "MERIDIAN", "TRIANGULATION", "TOPOGRAPHY",
    # Places
    "LONDON", "OXFORD", "CAMBRIDGE", "RUSSIA", "MOSCOW", "ENGLAND",
    "EUROPE", "BRITAIN", "SOVIET", "PARIS", "BERLIN", "ROME", "VIENNA",
    # Military/Intelligence
    "MILITARY", "CIPHER", "SECRET", "CODE", "MESSAGE", "SIGNAL",
    "COMMAND", "DEFENSE", "INTELLIGENCE", "CRYPTOGRAPHY", "ESPIONAGE",
    # Context
    "BEGINNER", "EXERCISE", "EXAMPLE", "SOLUTION", "PRACTICE",
    "STUDENT", "LEARNING", "SIMPLE", "BASIC", "CHAPTER",
    # Actions
    "ATTENTION", "IMPORTANT", "LETTER", "DOCUMENT", "DESTROY",
    "CONFIDENTIAL", "URGENT", "WARNING", "CAUTION", "READ",
    # French
    "CARTE", "GEOGRAPHIE", "COORDONNEES", "NORD", "SUD", "EST", "OUEST",
]

# Fast byte translation table for C-level string conversion (Massive Speedup)
TRANS_TABLE = bytes([c + 65 for c in range(25)] + [63] + [0]*230)

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
    return[ord(c) - ord('A') for c in key_letters]

def generate_all_squares():
    """Generates the keyword squares list (Moved here to prevent child process memory leaks)"""
    squares =[]
    for kw in BASE_KEYWORDS:
        squares.append(np.array(generate_keyword_square(kw), dtype=np.int8))
        squares.append(np.array(generate_keyword_square(kw[::-1]), dtype=np.int8))
        if len(kw) > 6:
            squares.append(np.array(generate_keyword_square(kw[:6]), dtype=np.int8))
            squares.append(np.array(generate_keyword_square(kw[-6:]), dtype=np.int8))
    
    # Add random variations
    for _ in range(12000):
        rw = "".join(random.sample(ALPHABET, random.randint(4, 14)))
        squares.append(np.array(generate_keyword_square(rw), dtype=np.int8))
    
    return np.array(squares, dtype=np.int8)

# ============================================================================
# ENHANCED SCORING SYSTEM
# ============================================================================
def load_quadgrams_optimized(filename="english_quadgrams.txt"):
    quadgrams = {}
    floor = -5.5
    if os.path.exists(filename):
        try:
            total = 0
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        q, c = parts
                        c = int(c)
                        quadgrams[q] = c
                        total += c
            for q in quadgrams:
                quadgrams[q] = math.log10(quadgrams[q] / total)
            floor = math.log10(0.01 / total)
        except:
            pass
    
    if not quadgrams:
        common_q = {
            'TION': -2.1, 'NTHE': -2.2, 'THER': -2.3, 'THAT': -2.3,
            'ETTE': -2.4, 'MENT': -2.5, 'IONS': -2.6, 'WITH': -2.5,
            'ATIO': -2.6, 'OFTH': -2.4, 'THEM': -2.5, 'FROM': -3.1,
            'OULD': -2.4, 'HAVE': -2.5, 'WERE': -2.6, 'BEEN': -2.6,
        }
        quadgrams.update(common_q)
    
    french = {
        'DANS': -2.7, 'POUR': -2.8, 'ENTR': -2.9, 'AVEC': -3.0,
        'SANS': -3.1, 'TOUT': -2.8, 'PLUS': -2.9, 'MAIS': -2.8,
    }
    quadgrams.update(french)
    return quadgrams, floor

def create_quadgram_lookup_array(quadgrams, floor):
    lookup = np.full(26**4, floor, dtype=np.float32)
    for quad, score in quadgrams.items():
        if len(quad) == 4 and all(c in ALPHABET for c in quad):
            idx = sum((ord(quad[i]) - ord('A')) * (26 ** (3-i)) for i in range(4))
            lookup[idx] = score
    return lookup

def score_text_aggressive(text_arr, quad_lookup, floor):
    """Enhanced multi-level fitness function"""
    score = 0.0
    text_len = len(text_arr)
    
    # 1. Quadgram scoring (primary signal)
    for i in range(text_len - 3):
        idx = (int(text_arr[i]) * 17576 + int(text_arr[i+1]) * 676 +
               int(text_arr[i+2]) * 26 + int(text_arr[i+3]))
        if idx < len(quad_lookup):
            score += quad_lookup[idx]
        else:
            score += floor
            
    # EARLY EXIT CPU OPTIMIZATION:
    # If the score is completely garbage (<-950), checking cribs is a waste of CPU.
    if score < -950:
        return score
    
    # FAST STRING CONVERSION OPTIMIZATION
    text_str = text_arr.tobytes().translate(TRANS_TABLE).decode('ascii')
    
    # 2. Trigram & Bigram bonuses 
    trigrams = {'THE': 5, 'AND': 4, 'ING': 4, 'ION': 3, 'ENT': 3, 'MAP': 8, 'GEO': 8, 'LAT': 6, 'LON': 6, 'COR': 6}
    bigrams = {'TH': 2, 'HE': 2, 'IN': 2, 'ER': 2, 'AN': 2, 'RE': 2, 'ON': 2, 'AT': 2, 'EN': 2, 'ND': 2}
    
    for tri, weight in trigrams.items():
        score += text_str.count(tri) * weight
    for big, weight in bigrams.items():
        score += text_str.count(big) * weight
    
    # 4. Repeated character penalty (strict)
    max_run = 1
    current_run = 1
    for i in range(1, text_len):
        if text_arr[i] == text_arr[i-1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1
    
    if max_run > 3:
        score -= max_run * 10.0
    
    # 5. Vowel-consonant ratio (English is ~38-42% vowels)
    vowels = sum(1 for c in text_arr if c in[0, 4, 8, 14, 20])  # A,E,I,O,U
    ratio = vowels / text_len if text_len > 0 else 0
    if 0.30 < ratio < 0.50:
        score += 20.0
    else:
        score -= abs(ratio - 0.40) * 50.0
    
    # 6. MASSIVE cartographic cribs
    mega_cribs = {
        "MAP": 20, "MAPS": 25, "GRID": 20, "GRIDS": 25,
        "COORDINATE": 50, "COORDINATES": 60, "COORD": 40,
        "LATITUDE": 60, "LONGITUDE": 60, "LAT": 30, "LON": 30,
        "NORTH": 25, "SOUTH": 25, "EAST": 20, "WEST": 20,
        "LONDON": 35, "OXFORD": 35, "CAMBRIDGE": 40,
        "SCALE": 25, "PROJECTION": 70, "AZIMUTH": 50,
        "CARTOGRAPHY": 120, "MAPMAKING": 100, "GEOGRAPHY": 70,
        "SURVEY": 35, "SURVEYOR": 45, "TRIANGULATION": 90,
        "RUSSIA": 35, "SOVIET": 40, "ENGLAND": 35, "BRITAIN": 35,
        "SECRET": 30, "MESSAGE": 35, "CIPHER": 50, "CODE": 25,
        "ATTENTION": 40, "IMPORTANT": 40, "DESTROY": 35,
        "CHART": 25, "TOPOGRAPHY": 60, "COMPASS": 40,
    }
    
    for crib, weight in mega_cribs.items():
        if crib in text_str:
            score += weight
    
    # 7. No-Q-without-U rule
    for i in range(text_len - 1):
        if text_arr[i] == 16 and text_arr[i+1] != 20:
            score -= 20.0
    
    # 8. Unlikely letter combinations penalty
    bad_combos =['QZ', 'QX', 'QK', 'JZ', 'JQ', 'VQ', 'ZJ', 'ZQ']
    for combo in bad_combos:
        score -= text_str.count(combo) * 15.0
    
    return score

# ============================================================================
# CIPHER OPERATIONS
# ============================================================================
def prepare_cipher(raw_text):
    clean = raw_text.replace(" ", "").replace("000", "")
    pairs =[clean[i:i+2] for i in range(0, len(clean), 2)]
    indices =[]
    for p in pairs:
        try:
            r, c = ROWS.index(p[0]), COLS.index(p[1])
            indices.append(r * 5 + c)
        except:
            indices.append(-1)
    return np.array(indices, dtype=np.int8)

def apply_double_transpose(base_indices, row_key, col_key, out_buffer):
    idx = 0
    for col in col_key:
        for row in row_key:
            position = int(row) * 14 + int(col)
            out_buffer[idx] = base_indices[position]
            idx += 1

# ============================================================================
# STRATEGY 1: ADAPTIVE GENETIC ALGORITHM
# ============================================================================
def genetic_algorithm_worker(worker_id, queue, base_indices, quad_lookup, floor, squares):
    np.random.seed()
    random.seed()
    
    POPULATION_SIZE = 30
    ELITE_SIZE = 6
    
    population =[]
    for _ in range(POPULATION_SIZE):
        rk = np.arange(14, dtype=np.int8)
        ck = np.arange(14, dtype=np.int8)
        np.random.shuffle(rk)
        np.random.shuffle(ck)
        sq = squares[np.random.randint(0, len(squares))].copy()
        population.append((rk, ck, sq))
    
    best_ever_score = -float('inf')
    stagnation_counter = 0
    mutation_rate = 0.7
    gen = 0
    
    while True:
        scored =[]
        for rk, ck, sq in population:
            trans_buffer = np.zeros(196, dtype=np.int8)
            apply_double_transpose(base_indices, rk, ck, trans_buffer)
            text_arr = np.array([sq[i] if i != -1 else 25 for i in trans_buffer], dtype=np.int8)
            score = score_text_aggressive(text_arr, quad_lookup, floor)
            scored.append((score, rk, ck, sq, text_arr))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        
        if scored[0][0] > best_ever_score:
            best_ever_score = scored[0][0]
            stagnation_counter = 0
            mutation_rate = max(0.5, mutation_rate * 0.95)
            
            # Fast String conversion for queue
            text_str = scored[0][4].tobytes().translate(TRANS_TABLE).decode('ascii')
            queue.put(("GA", worker_id, gen, best_ever_score, scored[0][1], scored[0][2], scored[0][3], text_str))
        else:
            stagnation_counter += 1
            if stagnation_counter > 20:
                mutation_rate = min(0.95, mutation_rate * 1.1)
                stagnation_counter = 0
        
        new_population =[(rk.copy(), ck.copy(), sq.copy()) for _, rk, ck, sq, _ in scored[:ELITE_SIZE]]
        
        while len(new_population) < POPULATION_SIZE:
            tournament = random.sample(scored[:ELITE_SIZE*2], 2)
            parent1 = tournament[0] if tournament[0][0] > tournament[1][0] else tournament[1]
            parent2 = random.choice(scored[:ELITE_SIZE*2])
            
            child_rk = parent1[1].copy() if random.random() < 0.5 else parent2[1].copy()
            child_ck = parent1[2].copy() if random.random() < 0.5 else parent2[2].copy()
            child_sq = parent1[3].copy() if random.random() < 0.5 else parent2[3].copy()
            
            if random.random() < mutation_rate:
                a, b = np.random.randint(0, 14, 2)
                child_rk[a], child_rk[b] = child_rk[b], child_rk[a]
            if random.random() < mutation_rate:
                a, b = np.random.randint(0, 14, 2)
                child_ck[a], child_ck[b] = child_ck[b], child_ck[a]
            if random.random() < 0.4:
                if random.random() < 0.7:
                    child_sq = squares[np.random.randint(0, len(squares))].copy()
                else:
                    a, b = np.random.randint(0, 25, 2)
                    child_sq[a], child_sq[b] = child_sq[b], child_sq[a]
            
            new_population.append((child_rk, child_ck, child_sq))
        
        if gen % 50 == 0:
            diversity_count = POPULATION_SIZE // 10
            for i in range(diversity_count):
                rk = np.arange(14, dtype=np.int8)
                ck = np.arange(14, dtype=np.int8)
                np.random.shuffle(rk)
                np.random.shuffle(ck)
                sq = squares[np.random.randint(0, len(squares))].copy()
                new_population[-(i+1)] = (rk, ck, sq)
        
        population = new_population
        gen += 1

# ============================================================================
# STRATEGY 2: ENHANCED PARALLEL TEMPERING
# ============================================================================
def parallel_tempering_worker(worker_id, queue, base_indices, quad_lookup, floor, squares):
    np.random.seed()
    random.seed()
    
    N_CHAINS = 6
    temps =[100.0, 50.0, 25.0, 10.0, 5.0, 1.0]
    
    chains =[]
    for temp in temps:
        rk = np.arange(14, dtype=np.int8)
        ck = np.arange(14, dtype=np.int8)
        np.random.shuffle(rk)
        np.random.shuffle(ck)
        sq = squares[np.random.randint(0, len(squares))].copy()
        
        trans_buffer = np.zeros(196, dtype=np.int8)
        apply_double_transpose(base_indices, rk, ck, trans_buffer)
        text_arr = np.array([sq[i] if i != -1 else 25 for i in trans_buffer], dtype=np.int8)
        score = score_text_aggressive(text_arr, quad_lookup, floor)
        
        chains.append([score, rk, ck, sq, temp])
    
    best_ever_score = -float('inf')
    iteration = 0
    
    while True:
        for i in range(N_CHAINS):
            score, rk, ck, sq, temp = chains[i]
            
            new_rk, new_ck, new_sq = rk.copy(), ck.copy(), sq.copy()
            mutation_prob = min(0.8, 0.3 + (temp / 100.0) * 0.5)
            
            mode = np.random.random()
            if mode < 0.35:
                a, b = np.random.randint(0, 14, 2)
                new_rk[a], new_rk[b] = new_rk[b], new_rk[a]
            elif mode < 0.70:
                a, b = np.random.randint(0, 14, 2)
                new_ck[a], new_ck[b] = new_ck[b], new_ck[a]
            else:
                if np.random.random() < mutation_prob:
                    new_sq = squares[np.random.randint(0, len(squares))].copy()
                else:
                    a, b = np.random.randint(0, 25, 2)
                    new_sq[a], new_sq[b] = new_sq[b], new_sq[a]
            
            trans_buffer = np.zeros(196, dtype=np.int8)
            apply_double_transpose(base_indices, new_rk, new_ck, trans_buffer)
            text_arr = np.array([new_sq[x] if x != -1 else 25 for x in trans_buffer], dtype=np.int8)
            new_score = score_text_aggressive(text_arr, quad_lookup, floor)
            
            if new_score > score or random.random() < math.exp((new_score - score) / temp):
                chains[i] =[new_score, new_rk, new_ck, new_sq, temp]
                
                if new_score > best_ever_score:
                    best_ever_score = new_score
                    text_str = text_arr.tobytes().translate(TRANS_TABLE).decode('ascii')
                    queue.put(("PT", worker_id, iteration, new_score, new_rk, new_ck, new_sq, text_str))
        
        if iteration % 50 == 0:
            for _ in range(N_CHAINS // 2):
                i, j = random.sample(range(N_CHAINS), 2)
                if i > j:
                    i, j = j, i
                
                delta = (1.0/chains[i][4] - 1.0/chains[j][4]) * (chains[j][0] - chains[i][0])
                if delta >= 0 or random.random() < math.exp(delta):
                    chains[i][:4], chains[j][:4] = chains[j][:4], chains[i][:4]
        
        iteration += 1

# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================
def run_ultimate_assault():
    print("=" * 80)
    print("  D'AGAPEYEFF ULTIMATE ASSAULT - MAXIMUM OPTIMIZATION")
    print("  (Architecture Fixed - Continuous Evolution)")
    print("=" * 80)
    
    # 1. Generate heavy keyword matrix exactly once
    print("[+] Generating Keyword Matrices...")
    PRECOMPUTED_SQUARES = generate_all_squares()
    
    quadgrams, floor = load_quadgrams_optimized("english_quadgrams.txt")
    quad_lookup = create_quadgram_lookup_array(quadgrams, floor)
    base_indices = prepare_cipher(RAW_CIPHER)
    
    cores = mp.cpu_count()
    ga_cores = max(1, cores // 2)
    pt_cores = max(1, cores - ga_cores)
    
    print(f"[+] Using {cores} CPU cores")
    print(f"    • {ga_cores} Adaptive Genetic Algorithm workers")
    print(f"    • {pt_cores} Parallel Tempering workers")
    print(f"[+] Pre-computed {len(PRECOMPUTED_SQUARES)} keyword squares")
    print()
    print("[!] Workers will run continuously until Ctrl+C")
    print("[!] Check ultimate_assault_results.log for all improvements")
    print("-" * 80)
    
    manager = mp.Manager()
    results_queue = manager.Queue()
    processes =[]
    
    for i in range(ga_cores):
        p = mp.Process(target=genetic_algorithm_worker, 
                      args=(i, results_queue, base_indices, quad_lookup, floor, PRECOMPUTED_SQUARES))
        p.daemon = True
        p.start()
        processes.append(p)
    
    for i in range(pt_cores):
        p = mp.Process(target=parallel_tempering_worker,
                      args=(i, results_queue, base_indices, quad_lookup, floor, PRECOMPUTED_SQUARES))
        p.daemon = True
        p.start()
        processes.append(p)
    
    # Bugfix: Initialize variables outside try/except so early Ctrl+C doesn't crash
    elapsed = 0
    best_overall = -float('inf')
    start = time.time()
    result_count = 0
    
    try:
        while True:
            strat, w_id, cycles, score, rk, ck, sq, text = results_queue.get()
            
            result_count += 1
            elapsed = int(time.time() - start)
            
            if score > best_overall:
                best_overall = score
                
                print(f"\n{'='*80}")
                print(f"🔥 NEW BEST [{strat} Worker {w_id}] - Gen/Iter: {cycles} - Time: {elapsed}s")
                print(f"   Score: {score:.2f}")
                print(f"{'='*80}")
                print(f"Row Key : {list(rk)}")
                print(f"Col Key : {list(ck)}")
                print(f"Square  : {''.join(chr(ord('A')+c) for c in sq)}")
                print(f"\nDecrypted Text:")
                print(f"{text}")
                print(f"{'='*80}\n")
                
                if score > -300:
                    print("⚠️  Score above -300! Examine this carefully!\n")
                if score > -200:
                    print("🔥🔥🔥 BREAKTHROUGH! Score above -200! 🔥🔥🔥\n")
                
                with open("ultimate_assault_results.log", "a") as f:
                    f.write(f"\n[{strat} Worker {w_id}] Cycle {cycles} | Score: {score:.2f} | Time: {elapsed}s\n")
                    f.write(f"Row: {list(rk)}\nCol: {list(ck)}\n")
                    f.write(f"Square: {''.join(chr(ord('A')+c) for c in sq)}\n")
                    f.write(f"Text: {text}\n" + "-" * 80 + "\n")
            
            if result_count % 10 == 0:
                rate = result_count / elapsed if elapsed > 0 else 0
                print(f"[Status] Time: {elapsed}s | Queue hits: {result_count} | Best: {best_overall:.2f} | Local Bests/s: {rate:.2f}")
    
    except KeyboardInterrupt:
        print(f"\n\n[!] Stopping all workers...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
        print(f"[✓] Successfully terminated after {elapsed}s")
        print(f"[✓] Total results collected from queue: {result_count}")
        print(f"[✓] Best score achieved: {best_overall:.2f}")

if __name__ == "__main__":
    run_ultimate_assault()