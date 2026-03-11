#!/usr/bin/env python3
import math
import random
import time
import sys
import os
import multiprocessing as mp
import requests
import json
import signal

# ============================================================================
# CONFIGURATION: THE 1939 MONSTER
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
ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # J is omitted per standard
ROWS, COLS = ['6', '7', '8', '9', '0'], ['1', '2', '3', '4', '5']

# ============================================================================
# THE "GRAVITY WELL" (HARD-LOCKS) 
# Derived from your Gen 1917 Breakthrough Logs
# ============================================================================
HARD_LOCKED_CRIBS = {
    "GEOGRAPHY": 8000.0,  # Based on "ROMAPHY"
    "RUSSIAN":   7000.0,  # Based on "URSSIAN"
    "FINALLY":   6000.0,  # Based on "YIYYNALY"
    "COMMITTEE": 6000.0,  # Based on "MITTEE"
    "REDUCED":   5000.0,  # Based on "REDICD"
    "LONDON":    4000.0,
    "MAPMAKING": 4000.0,
    "SECTION":   3000.0
}

# ============================================================================
# LLM BRIDGE (Ollama API)
# ============================================================================
USE_LLM = True
LLM_URL = "http://localhost:11434/api/generate"

def ask_llm_for_cribs(text):
    if not USE_LLM: return []
    prompt = f"Analyze this ciphertext fragment: '{text}'. List 3 English or French words that seem to be forming. Return only words."
    try:
        r = requests.post(LLM_URL, json={"model": "phi3", "prompt": prompt, "stream": False}, timeout=5)
        res = r.json().get('response', "").upper()
        return [w.strip() for w in res.split(',') if len(w.strip()) > 3]
    except: return []

# ============================================================================
# CORE MATH ENGINE (Optimized)
# ============================================================================
def load_quadgrams():
    # Hardcoded top quadgrams for speed if file is missing
    return {
        'TION': -2.1, 'NTHE': -2.2, 'THER': -2.3, 'THAT': -2.3,
        'ETTE': -2.4, 'MENT': -2.5, 'IONS': -2.6, 'WITH': -2.5,
        'ATIO': -2.6, 'OFTH': -2.4, 'THEM': -2.5, 'FROM': -3.1
    }, -5.5

def monster_score(text, quadgrams, floor):
    score = 0.0
    # 1. Linguistic N-Grams
    for i in range(len(text) - 3):
        score += quadgrams.get(text[i:i+4], floor)

    # 2. Hard-Lock Gravity (Anchor logic)
    for crib, weight in HARD_LOCKED_CRIBS.items():
        if crib in text:
            score += weight
        else:
            # Partial match trail (helps hill-climbing)
            if crib[:5] in text: score += (weight * 0.4)
            if crib[:4] in text: score += (weight * 0.2)

    # 3. Structural Sanity
    bad_combos = ["VXV", "ZQX", "JKQ", "VWG", "HHH", "YYY", "XXX"]
    for bc in bad_combos:
        if bc in text: score -= 1000.0
        
    return score

def prepare_cipher(raw_text):
    clean = raw_text.replace(" ", "").replace("000", "")
    indices = []
    for i in range(0, len(clean), 2):
        try:
            r, c = ROWS.index(clean[i]), COLS.index(clean[i+1])
            indices.append(r * 5 + c)
        except: continue
    return indices

# ============================================================================
# WORKER PROCESS
# ============================================================================
def init_worker(): signal.signal(signal.SIGINT, signal.SIG_IGN)

def worker_task(args):
    indices, quadgrams, floor, iterations = args
    
    # Initialize Random Keys
    curr_rk = list(range(GRID_SIZE)); random.shuffle(curr_rk)
    curr_ck = list(range(GRID_SIZE)); random.shuffle(curr_ck)
    curr_sq = list(ALPHABET); random.shuffle(curr_sq)
    
    best_state = (-99999, [], [], [], "")
    temp = 50.0

    for _ in range(iterations):
        new_rk, new_ck, new_sq = curr_rk[:], curr_ck[:], curr_sq[:]
        
        # Mutation Logic
        mode = random.random()
        if mode < 0.4:
            a, b = random.sample(range(GRID_SIZE), 2); new_rk[a], new_rk[b] = new_rk[b], new_rk[a]
        elif mode < 0.8:
            a, b = random.sample(range(GRID_SIZE), 2); new_ck[a], new_ck[b] = new_ck[b], new_ck[a]
        else:
            a, b = random.sample(range(25), 2); new_sq[a], new_sq[b] = new_sq[b], new_sq[a]

        # Fast Transposition
        text_chars = []
        for c in new_ck:
            for r in new_rk:
                pos = r * GRID_SIZE + c
                if pos < len(indices):
                    text_chars.append(new_sq[indices[pos]])
        
        text = "".join(text_chars)
        score = monster_score(text, quadgrams, floor)

        # Acceptance (Simulated Annealing)
        if score > best_state[0] or (temp > 0.1 and random.random() < math.exp((score - best_state[0]) / temp)):
            curr_rk, curr_ck, curr_sq = new_rk, new_ck, new_sq
            if score > best_state[0]:
                best_state = (score, curr_rk[:], curr_ck[:], curr_sq[:], text)

        temp *= 0.9998

    return best_state

# ============================================================================
# ORCHESTRATOR
# ============================================================================
def run_cracker():
    print("==========================================================")
    print("  D'AGAPEYEFF MONSTER CRACKER V5 - HARD LOCK EDITION")
    print("  OPTIMIZED FOR RK3588 (ORANGE PI 5 MAX)")
    print("==========================================================")

    indices = prepare_cipher(RAW_CIPHER)
    quads, floor = load_quadgrams()
    
    # Use 7 cores for math, reserve 1 for LLM/System
    cores = max(1, mp.cpu_count() - 1)
    pool = mp.Pool(cores, initializer=init_worker)
    
    best_overall = -float('inf')
    gen = 1
    start_time = time.time()

    try:
        while True:
            jobs = [(indices, quads, floor, 50000) for _ in range(cores)]
            results = pool.map(worker_task, jobs)

            for score, rk, ck, sq, text in results:
                if score > best_overall:
                    best_overall = score
                    print(f"\n\n[!!!] NEW BEST SCORE: {score:.2f} (Gen {gen})")
                    print(f"R: {rk}\nC: {ck}\nS: {''.join(sq)}")
                    print(f"TEXT: {text[:140]}...") # Print first 140 chars
                    
                    # LOG TO FILE
                    with open("crack_v5.log", "a") as f:
                        f.write(f"\nScore: {score} | Time: {int(time.time()-start_time)}s\n{text}\n")

                    # LLM ADVICE
                    if score > -800:
                        new_cribs = ask_llm_for_cribs(text)
                        for c in new_cribs:
                            if c not in HARD_LOCKED_CRIBS:
                                print(f"[AI INFO] Adding new crib to gravity list: {c}")
                                HARD_LOCKED_CRIBS[c] = 2000.0

            sys.stdout.write(f"\rGen {gen} | Searching... Best: {best_overall:.2f}  ")
            sys.stdout.flush()
            gen += 1

    except KeyboardInterrupt:
        pool.terminate(); pool.join()
        print("\n[!] Cracking Paused. Progress saved in crack_v5.log")

if __name__ == "__main__":
    run_cracker()
