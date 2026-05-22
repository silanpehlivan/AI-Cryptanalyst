import base64
import string
import itertools
from utils import clean_text, ALPHABET_EN, ALPHABET_TR, TURKISH_FREQ, calculate_ic

# English Letter Frequency (approximate)
ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def score_text(text, frequency_dict=ENGLISH_FREQ, alphabet=ALPHABET_EN):
    """
    Scores a text based on how well it matches letter frequencies.
    Lower score is better (Chi-squared statistic).
    """
    # Clean text to just valid alphabet chars for scoring
    # But clean_text usually only does A-Z. 
    # For scoring, we need to count whatever is in the alphabet.
    
    n = 0
    counts = dict.fromkeys(alphabet, 0)
    
    for char in text:
        # Normalize char to upper for scoring
        c_upper = char.upper()
        if char == 'i': c_upper = 'İ'
        if char == 'ı': c_upper = 'I'
        if c_upper == 'i': c_upper = 'İ' # Catch 'i' if in text
        
        if c_upper in counts:
            counts[c_upper] += 1
            n += 1
            
    if n == 0: return float('inf')
            
    # Common English words to boost score for short text
    COMMON_WORDS = ["THE", "AND", "IS", "OF", "TO", "IN", "IT", "YOU", "THAT", "KEEP", "CODE", "SAFE", "MAKE", "LIKE"]
    
    score = 0
    text_upper = text.upper()
    
    # Frequency Score
    for char in alphabet:
        observed = counts[char]
        expected = n * frequency_dict.get(char, 0)
        if expected > 0:
            score += ((observed - expected) ** 2) / expected
        else:
            if observed > 0:
                score += 100 # Penalty for unexpected char
                
    # Bonus for common words (Negative score is good)
    for word in COMMON_WORDS:
        if word in text_upper:
            score -= 50 # Significant bonus
            
    return score

def solve_caesar(ciphertext):
    """
    Brute-forces Caesar cipher for both English and Turkish.
    Returns the best candidate.
    """
    # Try English
    best_en, info_en, score_en = _solve_caesar_lang(ciphertext, ALPHABET_EN, ENGLISH_FREQ, "EN")
    
    # Try Turkish
    best_tr, info_tr, score_tr = _solve_caesar_lang(ciphertext, ALPHABET_TR, TURKISH_FREQ, "TR")
    
    # Apply a small bias/penalty? No, chi-square should handle it.
    # However, if text is short, it might be ambiguous. 
    
    if score_tr < score_en:
        return best_tr, info_tr
    else:
        return best_en, info_en

def _solve_caesar_lang(ciphertext, alphabet, freq_dict, lang_name):
    best_score = float('inf')
    best_plaintext = ""
    best_shift = 0
    
    limit = len(alphabet)
    
    for shift in range(limit):
        plaintext = ""
        for char in ciphertext:
            # Handle Case 
            is_lower = char.islower()
            c_upper = char.upper()
            
            # Manual Mapping for TR
            if lang_name == 'TR':
                if char == 'i': 
                    c_upper = 'İ'
                    is_lower = True
                elif char == 'ı': 
                    c_upper = 'I'
                    is_lower = True
                elif char == 'İ':
                    c_upper = 'İ'
                    is_lower = False
                elif char == 'I':
                    c_upper = 'I'
                    is_lower = False
            
            if c_upper in alphabet:
                idx = alphabet.find(c_upper)
                new_idx = (idx - shift) % limit
                new_char = alphabet[new_idx]
                
                if is_lower:
                    if lang_name == 'TR':
                        if new_char == 'I': 
                            plaintext += 'ı'
                        elif new_char == 'İ': 
                            plaintext += 'i'
                        else:
                            plaintext += new_char.lower()
                    else:
                        plaintext += new_char.lower()
                else:
                    plaintext += new_char
            else:
                plaintext += char
        
        current_score = score_text(plaintext, freq_dict, alphabet)
        if current_score < best_score:
            best_score = current_score
            best_plaintext = plaintext
            best_shift = shift
            
    return best_plaintext, f"Shift: {best_shift} ({lang_name})", best_score

def solve_base64(ciphertext):
    try:
        decoded_bytes = base64.b64decode(ciphertext)
        return decoded_bytes.decode('utf-8', errors='ignore'), "Base64"
    except Exception as e:
        return f"Error decoding Base64: {e}", "Error"

def solve_xor(ciphertext, max_key_len=5):
    """
    Brute-force repeating key XOR up to max_key_len.
    Uses column-based frequency analysis to find candidate key bytes,
    then evaluates top combinations on the full text.
    """
    try:
        cipher_bytes = bytes.fromhex(ciphertext)
    except ValueError:
        cipher_bytes = ciphertext.encode('utf-8')

    best_overall_score = float('inf')
    best_overall_result = ""
    best_overall_key = ""

    limit = min(max_key_len, len(cipher_bytes))
    if limit < 1: limit = 1

    for k_len in range(1, limit + 1):
        col_candidates = []
        for i in range(k_len):
            column = cipher_bytes[i::k_len]
            scores = []
            for b in range(256):
                # Count valid English/Turkish letters and spaces
                letters = sum(1 for c in column if 65 <= (c^b) <= 90 or 97 <= (c^b) <= 122 or (c^b) == 32)
                # Count printable characters
                printable = sum(1 for c in column if 32 <= (c^b) <= 126 or (c^b) in (9,10,13))
                
                # We want mostly printable characters
                if printable == len(column):
                    scores.append((letters, b))
            
            # Sort by letter count descending
            scores.sort(key=lambda x: x[0], reverse=True)
            # Take top 3 candidate bytes for this column
            col_candidates.append([x[1] for x in scores[:3]])
        
        # If any column had zero valid candidates, skip this key length
        if not all(col_candidates): 
            continue
        
        # Test combinations of candidate bytes
        for key_tuple in itertools.product(*col_candidates):
            full_candidate = bytearray()
            for i, b in enumerate(cipher_bytes):
                full_candidate.append(b ^ key_tuple[i % k_len])
            
            try:
                text = full_candidate.decode('utf-8')
                s = score_text(text)
                
                # Small penalty for lowercase first letter (to prefer "ABC" over "abc" if scores tie)
                if text and text[0].islower():
                    s += 0.1

                if s < best_overall_score:
                    best_overall_score = s
                    best_overall_result = text
                    best_overall_key = bytes(key_tuple).decode('utf-8', errors='replace')
            except Exception:
                pass

    if best_overall_result:
        return best_overall_result, f"Key: {best_overall_key}"
    return "Could not solve XOR", "Unknown"

def solve_vigenere(ciphertext):
    """
    Attempts to solve Vigenere by trying multiple key lengths and scoring the result.
    This is much more robust for short text than IC-based key length estimation.
    """
    text_clean = clean_text(ciphertext)
    if not text_clean:
        return ciphertext, "No valid characters to analyze"

    best_overall_score = float('inf')
    best_overall_plaintext = ""
    best_overall_key = "A"
    
    # Try key lengths from 1 up to min(14, len(text))
    # For very short text, we can't estimate key length well, so we try all.
    max_len = min(14, len(text_clean))
    if max_len < 1: max_len = 1
    
    for k_len in range(1, max_len + 1):
        # Solve for this specific key length
        current_key = ""
        current_plaintext = "" # We'll reconstruct full plaintext after finding key
        
        # 1. Find the best key for this length
        for i in range(k_len):
            column = text_clean[i::k_len]
            if not column: 
                 current_key += 'A'
                 continue
                 
            best_col_score = float('inf')
            best_char = 'A'
            
            for k_char in ALPHABET_EN:
                shift = ALPHABET_EN.find(k_char)
                decrypted_col = ""
                for c in column:
                    idx = ALPHABET_EN.find(c)
                    decrypted_col += ALPHABET_EN[(idx - shift) % 26]
                
                # Score this column? 
                # No, scoring a column of "every 4th letter" against English Freq is noisy.
                # Standard Vigenere breakers score the DISTIBUTION of the column vs English.
                s = score_text(decrypted_col)
                if s < best_col_score:
                    best_col_score = s
                    best_char = k_char
            current_key += best_char
            
        # 2. Decrypt with this key and score the FULL text
        # (Scoring full text is better than average of column scores)
        full_plaintext = ""
        key_idx = 0
        for char in ciphertext:
            if char.upper() in ALPHABET_EN:
                shift = ALPHABET_EN.find(current_key[key_idx % len(current_key)])
                p_idx = ALPHABET_EN.find(char.upper()) 
                p_char = ALPHABET_EN[(p_idx - shift) % 26]
                if char.islower():
                    full_plaintext += p_char.lower()
                else:
                    full_plaintext += p_char
                key_idx += 1
            else:
                full_plaintext += char
        
        # Score the full plaintext
        final_score = score_text(full_plaintext)
        
        if final_score < best_overall_score:
            best_overall_score = final_score
            best_overall_plaintext = full_plaintext
            best_overall_key = current_key
            
    return best_overall_plaintext, f"Key: {best_overall_key}"
