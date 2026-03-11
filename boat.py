#!/usr/bin/env python3
import string

# Your best decrypted text from FINAL_SOLVE.log
CIPHERTEXT = "DOOILDKDESAOKPOTOIRIOEOOODLTKEADASLKATNIONLACEIITCSAIKTTKENDTLTTRSNILLAEOPPPKCDSNSIKPTRLINDTTTALONALCRRDAONRRISEKDDPSCSKPTPTKNAECSPKCLDLLNPENETKCNYTLONDTOYQAHSVLDKURUYCOORDINATESLRDANETKKRDSSNKAP"

# The confirmed word at the end of the text
PLAINTEXT_ANCHOR = "COORDINATES"

def find_vigenere_key(cipher_segment, plain_segment):
    key = ""
    for c, p in zip(cipher_segment, plain_segment):
        # Calculate the shift: (Cipher - Plain) % 26
        shift = (string.ascii_uppercase.find(c) - string.ascii_uppercase.find(p)) % 26
        key += string.ascii_uppercase[shift]
    return key

# Extract the segment where "COORDINATES" is located
# Based on your log, it is near the end but followed by 'LRDANET...'
start_pos = CIPHERTEXT.find("COORDINATES")
segment = CIPHERTEXT[start_pos:start_pos+len(PLAINTEXT_ANCHOR)]

print(f"--- Known-Plaintext Key Discovery: RK3588 ---")
if start_pos != -1:
    discovered_key = find_vigenere_key(segment, PLAINTEXT_ANCHOR)
    print(f"[!] Potential Key Fragment: {discovered_key}")
    print(f"[*] If this looks like a word (e.g., 'ABCABC'), your key is 'ABC'.")
else:
    print("[!] Could not find 'COORDINATES' in the ciphertext string.")
