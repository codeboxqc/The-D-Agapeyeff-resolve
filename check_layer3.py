 #!/usr/bin/env python3
import itertools

# The best output from your FINAL_SOLVE.log
CIPHERTEXT = "DOOILDKDESAOKPOTOIRIOEOOODLTKEADASLKATNIONLACEIITCSAIKTTKENDTLTTRSNILLAEOPPPKCDSNSIKPTRLINDTTTALONALCRRDAONRRISEKDDPSCSKPTPTKNAECSPKCLDLLNPENETKCNYTLONDTOYQAHSVLDKURUYCOORDINATESLRDANETKKRDSSNKAP"

# High-value targets for the RK3588 to hunt
ANCHORS = ["NORTH", "SOUTH", "EAST", "WEST", "LONDON", "MILES", "DEGREES", "COORDINATES"]

def score_decryption(text):
    """Calculates how many geographical keywords are found in the string."""
    score = 0
    for word in ANCHORS:
        if word in text:
            score += 1
    return score

def columnar_transposition(data, width):
    """Simulates reading the grid column by column."""
    # Create the grid based on the specified width
    rows = [data[i:i + width] for i in range(0, len(data), width)]
    
    decrypted = ""
    for col in range(width):
        for row in rows:
            if col < len(row):
                decrypted += row[col]
    return decrypted

def run_analysis():
    print(f"--- Layer 2 Analysis: Orange Pi 5 Max (8-Core Mode) ---")
    print(f"Testing Columnar Transposition widths 2 through 20...\n")
    
    best_width = 0
    max_matches = 0
    
    # Brute force the width of the transposition grid
    for w in range(2, 21):
        candidate = columnar_transposition(CIPHERTEXT, w)
        current_score = score_decryption(candidate)
        
        if current_score > 0:
            print(f"[!] Match Found (Width {w:2d}): {candidate[:60]}...")
            if current_score > max_matches:
                max_matches = current_score
                best_width = w
                
    if max_matches == 0:
        print("\n[?] No direct columnar matches found. The 'gibberish' might be a complex Vigenère shift.")
    else:
        print(f"\n[***] Best candidate found at width {best_width} with {max_matches} keyword matches.")

if __name__ == "__main__":
    run_analysis()
