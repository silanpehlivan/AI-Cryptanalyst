import random
import base64
import pandas as pd
import numpy as np
from utils import clean_text, ALPHABET_EN

# Sample Plaintexts (English and Turkish mixed for variety)
PLAINTEXTS = [
    "The quick brown fox jumps over the lazy dog.",
    "Cryptography is the practice and study of techniques for secure communication.",
    "Artificial intelligence is intelligence demonstrated by machines.",
    "Bugün hava çok güzel ve güneşli.",
    "Siber güvenlik, bilgisayar sistemlerini koruma sanatıdır.",
    "Şifreleme yöntemleri tarih boyunca kullanılmıştır.",
    "Attack at dawn on the verify field.",
    "We need to secure the perimeter immediately.",
    "The treasure is buried under the old oak tree.",
    "Hayat, bisiklete binmek gibidir. Dengede durmak için hareket etmelisiniz.",
    "Machine learning models require a lot of data.",
    "Network security involves many layers of protection."
]

# Expand corpus by mixing/concatenating
AUGMENTED_PLAINTEXTS = []
for _ in range(100):
    t1 = random.choice(PLAINTEXTS)
    t2 = random.choice(PLAINTEXTS)
    AUGMENTED_PLAINTEXTS.append(t1 + " " + t2)

def caesar_encrypt(text, shift):
    text = clean_text(text)
    result = ""
    for char in text:
        idx = ALPHABET_EN.find(char)
        if idx != -1:
            new_idx = (idx + shift) % 26
            result += ALPHABET_EN[new_idx]
        else:
            result += char
    return result

def vigenere_encrypt(text, key):
    text = clean_text(text)
    key = clean_text(key)
    if not key:
        return text
    result = ""
    key_idx = 0
    for char in text:
        idx = ALPHABET_EN.find(char)
        if idx != -1:
            k_char = key[key_idx % len(key)]
            k_shift = ALPHABET_EN.find(k_char)
            new_idx = (idx + k_shift) % 26
            result += ALPHABET_EN[new_idx]
            key_idx += 1
        else:
            result += char
    return result

def base64_encrypt(text):
    # Base64 works on bytes
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def xor_encrypt(text, key):
    # Repeating key XOR
    ciphertext = []
    key_bytes = key.encode('utf-8')
    text_bytes = text.encode('utf-8')
    for i, byte in enumerate(text_bytes):
        ciphertext.append(byte ^ key_bytes[i % len(key_bytes)])
    # Return hex string to be printable/viewable
    return bytes(ciphertext).hex()

def generate_dataset(num_samples=2000):
    data = []
    
    methods = ['Caesar', 'Vigenere', 'Base64', 'XOR']
    
    for _ in range(num_samples):
        method = random.choice(methods)
        plaintext = random.choice(AUGMENTED_PLAINTEXTS)
        
        ciphertext = ""
        
        if method == 'Caesar':
            shift = random.randint(1, 25)
            ciphertext = caesar_encrypt(plaintext, shift)
            
        elif method == 'Vigenere':
            keys = ['KEY', 'CRYPTO', 'SECRET', 'ALIEN', 'TURKEY']
            key = random.choice(keys)
            ciphertext = vigenere_encrypt(plaintext, key)
            
        elif method == 'Base64':
            ciphertext = base64_encrypt(plaintext)
            
        elif method == 'XOR':
            key = random.choice(['123', 'ABC', 'xyz', 'KEY'])
            ciphertext = xor_encrypt(plaintext, key)
        
        # Avoid empty ciphertexts
        if ciphertext:
            data.append({'ciphertext': ciphertext, 'label': method})
            
    df = pd.DataFrame(data)
    df.to_csv('crypto_dataset.csv', index=False)
    print(f"Dataset generated with {len(df)} samples.")
    print(df['label'].value_counts())

if __name__ == "__main__":
    generate_dataset()
