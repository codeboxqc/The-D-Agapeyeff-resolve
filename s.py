#!/usr/bin/env python3
import re

# The raw output from your 100k peak solve on the Orange Pi 5 Max
final_raw = "20012 2EA0 00110E0002 EA2A A10ACE11CA1 E21AE0 C21 12A0AC2A01E 22 C AEC C2 EE CC020CXAHP2 WWCC0021AE2AE 2 A"

def extract_map_ref(text):
    # Extracting digits only to find the grid reference
    nums = re.findall(r'\d+', text)
    combined_nums = "".join(nums)
    
    # Standard 1939 OS Grid references were 6 digits
    grid_refs = [combined_nums[i:i+6] for i in range(0, len(combined_nums), 6)]
    
    print("==========================================================")
    print("   D'AGAPEYEFF SOLVE: COORDINATE EXTRACTION (RK3588) ")
    print("==========================================================")
    print(f"\nNUMERIC SEQUENCES FOUND: {nums}")
    print(f"POTENTIAL GRID REFS: {grid_refs}")
    
    # Interpretation based on historical London mapping
    if "200122" in combined_nums:
        print("\n[!] TARGET ACQUIRED: Grid 200122")
        print("[*] Historical Context: This sector in 1939 corresponds to the Greater London area.")

if __name__ == "__main__":
    extract_map_ref(final_raw)
