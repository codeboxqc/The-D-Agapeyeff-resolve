#!/usr/bin/env python3
from collections import Counter

# Your 100k Peak Plaintext
plaintext = "DOOILDMDESAOMZOTOIRIOEOOODLTMEADASLMATNIONLACEIITCSAIMTTMENDTLTTRSNILLAEOZZZMCDSNSIMZTRLINDTTTALONALCRRDAONRRISEMDDZSCSMZTZTMNAECSZMCLDLLNZENETMCNBTLONDTOBXAHSPLDMWRWBCOORDINATESLRDANETMMRDSSNMAZ"

def clean_and_show():
    # Removing the identified nulls/delimiters
    cleaned = plaintext
    for null in "MZB":
        cleaned = cleaned.replace(null, " ")
    
    print("==========================================================")
    print("   D'AGAPEYEFF SOLVE: CLEANED PLAINTEXT (RK3588) ")
    print("==========================================================")
    print(f"\nRAW MESSAGE:\n{plaintext}")
    print(f"\nCLEANED MESSAGE:\n{cleaned}")
    print("\n" + "="*58)

def frequency_check_coords(text, limit=60):
    print(f"\n--- Frequency Analysis: First {limit} Characters ---")
    print("Targeting potential numeric substitution for coordinates...")
    
    segment = text[:limit]
    counts = Counter(segment)
    
    # Sort by frequency
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Char':<6} | {'Count':<6} | {'Percentage'}")
    print("-" * 30)
    for char, count in sorted_counts:
        percentage = (count / len(segment)) * 100
        print(f"{char:<6} | {count:<6} | {percentage:>8.2f}%")

if __name__ == "__main__":
    clean_and_show()
    # Run frequency check on the first 60 characters where numbers likely hide
    frequency_check_coords(plaintext)
