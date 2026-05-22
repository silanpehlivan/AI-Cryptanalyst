import string
import re
import math

# Standard English Alphabet
# Standard English Alphabet
ALPHABET_EN = string.ascii_uppercase

# Turkish Alphabet (29 chars)
# Note: Python's upper() might not handle i/I/ı/İ correctly without locale, 
# but for this specific order we will map manually if needed.
ALPHABET_TR = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

# Turkish Letter Frequency (approximate)
TURKISH_FREQ = {
    'A': 0.1192, 'B': 0.0284, 'C': 0.0097, 'Ç': 0.0115, 'D': 0.0470, 'E': 0.0891,
    'F': 0.0046, 'G': 0.0125, 'Ğ': 0.0112, 'H': 0.0121, 'I': 0.0511, 'İ': 0.0960,
    'J': 0.0003, 'K': 0.0468, 'L': 0.0592, 'M': 0.0375, 'N': 0.0748, 'O': 0.0247,
    'Ö': 0.0077, 'P': 0.0088, 'R': 0.0672, 'S': 0.0301, 'Ş': 0.0178, 'T': 0.0301,
    'U': 0.0323, 'Ü': 0.0184, 'V': 0.0098, 'Y': 0.0333, 'Z': 0.0150
}


def clean_text(text):
    """
    Removes non-alphabetic characters and converts to uppercase.
    Keeps only A-Z.
    """
    text = text.upper()
    text = re.sub(r'[^A-Z]', '', text)
    return text

def clean_text_keep_spaces(text):
    """
    Removes non-alphabetic characters but keeps spaces.
    """
    text = text.upper()
    text = re.sub(r'[^A-Z\s]', '', text)
    return text

def calculate_frequencies(text):
    text = clean_text(text)
    counts = dict.fromkeys(ALPHABET_EN, 0)
    for char in text:
        if char in counts:
            counts[char] += 1
    total = len(text)
    if total == 0: return [0] * 26
    return [counts[char] / total for char in ALPHABET_EN]

def calculate_ic(text):
    text = clean_text(text)
    N = len(text)
    if N <= 1: return 0.0
    counts = dict.fromkeys(ALPHABET_EN, 0)
    for char in text:
        if char in counts: counts[char] += 1
    sum_n_n_minus_1 = sum([c * (c - 1) for c in counts.values()])
    return sum_n_n_minus_1 / (N * (N - 1))

def calculate_entropy(text):
    text = clean_text(text)
    N = len(text)
    if N == 0: return 0
    counts = dict.fromkeys(ALPHABET_EN, 0)
    for char in text:
        if char in counts: counts[char] += 1
    perplexity = 0
    for count in counts.values():
        if count > 0:
            p = count / N
            perplexity += -p * math.log2(p)
    return perplexity
