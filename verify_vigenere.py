import sys
sys.path.append(r'.')
from solvers import solve_vigenere

def test():
    cipher = "Gvvp r fvkv nifv!"
    expected = "Keep a code safe!" # approximately
    
    print(f"Testing Cipher: {cipher}")
    result, info = solve_vigenere(cipher)
    print(f"Result: {result}")
    print(f"Info: {info}")
    
    if "Keep" in result or "keep" in result:
        print("SUCCESS: Found 'Keep'")
    else:
        print("FAILURE: Did not find 'Keep'")
        
    # Manual Key Test based on reverse engineering
    # Cipher: G V V P R F V K V N I F V
    # Key   : W R R A R D H H R V I A R
    # Plain : K E E P A C O D E S A F E
    print("\nManual Key Test (WRRARDHHRVIAR):")
    key = "WRRARDHHRVIAR"
    manual_plain = ""
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    idx = 0
    for char in cipher:
        if char.upper() in ALPHABET:
            c_idx = ALPHABET.find(char.upper())
            k_char = key[idx % len(key)]
            k_idx = ALPHABET.find(k_char)
            # Decrypt: P = (C - K) % 26
            p_idx = (c_idx - k_idx) % 26
            p_char = ALPHABET[p_idx]
            manual_plain += p_char.lower() if char.islower() else p_char
            idx += 1
        else:
            manual_plain += char
    print(f"Manual Decrypt: {manual_plain}")

if __name__ == "__main__":
    test()
