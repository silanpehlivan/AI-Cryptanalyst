import numpy as np
import tensorflow as tf
from tensorflow import keras
import pickle
from utils import clean_text, ALPHABET_EN

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
    import math
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

def predict_string(text):
    # Load resources
    try:
        model = keras.models.load_model('crypto_classifier.keras')
        with open('label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Extract features
    freqs = calculate_frequencies(text)
    ic = calculate_ic(text)
    ent = calculate_entropy(text)
    features = np.array([freqs + [ic, ent]])
    
    # Predict
    prediction = model.predict(features, verbose=0)
    predicted_idx = np.argmax(prediction)
    predicted_label = label_encoder.inverse_transform([predicted_idx])[0]
    confidence = np.max(prediction)
    
    print(f"Text: {text[:30]}...")
    print(f"Prediction: {predicted_label} ({confidence*100:.2f}%)")
    print("-" * 30)

if __name__ == "__main__":
    # Test Cases
    print("--- Model Verification ---")
    
    # Caesar (Shift 1)
    # Plain: HELLO WORLD -> IFMMP XPSME
    predict_string("IFMMP XPSME") 
    
    # Vigenere
    # Plain: HELLO -> Key: ABC -> HFNLP
    predict_string("HFNLP") 
    
    # Base64
    # Plain: Hello -> SGVsbG8=
    predict_string("SGVsbG8=")
    
    # XOR (Repeating 'A' is just original if 'A' is 0, but let's assume simple XOR)
    # Using the train logic, XOR produces hex
    # Let's try a hex string that looks like XOR output
    # Plain: "A" (0x41) ^ Key: "B" (0x42) = 0x03
    predict_string("030303") # Just a random hex-like string

    # Normal text (should be classified as something? Or maybe we didn't train for 'Plaintext' class?)
    # We only trained on Caesar, Vigenere, Base64, XOR. 
    # Ideally plain text looks like Caesar with shift 0 or Vigenere with key A.
    # Let's see what it says.
    predict_string("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG")
