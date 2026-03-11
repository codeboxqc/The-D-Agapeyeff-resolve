#!/usr/bin/env python3
"""
==============================================================================
N-Gram Download Assistant (Anti-403 Forbidden Edition)
==============================================================================
"""

import urllib.request
import zipfile
import os

def download_quadgrams():
    url = "http://practicalcryptography.com/media/cryptanalysis/files/english_quadgrams.txt.zip"
    zip_path = "quadgrams.zip"
    
    print("=========================================================")
    print("  N-Gram Dependency Downloader")
    print("=========================================================")
    print("[1/3] Connecting to Practical Cryptography...")
    
    try:
        # Added Mozilla User-Agent. PracticalCryptography actively blocks Python's 
        # default urllib agent and will throw a '403 Forbidden' HTTP Error without this!
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
            print(f"[2/3] Download complete ({len(data)} bytes). Extracting ZIP...")
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
            
        os.remove(zip_path) # Clean up ZIP footprint
        print("[3/3] Success! 'english_quadgrams.txt' has been unpacked.")
        print("\n[+] The D'Agapeyeff Monster Cracker is now fully armed.")
        
    except Exception as e:
        print(f"\n[-] Critical Network Error: {e}")
        print("[!] Please download the file manually using your web browser here:")
        print("    http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/")
        if os.path.exists(zip_path):
            os.remove(zip_path) # Prevent bad corrupted zip artifacts

if __name__ == "__main__":
    download_quadgrams()