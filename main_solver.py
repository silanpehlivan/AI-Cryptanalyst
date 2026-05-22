import numpy as np
import tensorflow as tf
from tensorflow import keras
import pickle
from solvers import solve_caesar, solve_vigenere, solve_base64, solve_xor
from utils import clean_text, ALPHABET_EN, calculate_frequencies, calculate_ic, calculate_entropy

class AICryptanalyst:
    def __init__(self):
        try:
            self.model = keras.models.load_model('crypto_classifier.keras')
            with open('label_encoder.pkl', 'rb') as f:
                self.label_encoder = pickle.load(f)
            self.loaded = True
        except Exception as e:
            print(f"Error loading model: {e}")
            self.loaded = False

    def predict(self, text):
        if not self.loaded:
            return "Model Error", 0.0
            
        freqs = calculate_frequencies(text)
        ic = calculate_ic(text)
        ent = calculate_entropy(text)
        features = np.array([freqs + [ic, ent]])
        
        prediction = self.model.predict(features, verbose=0)
        predicted_idx = np.argmax(prediction)
        predicted_label = self.label_encoder.inverse_transform([predicted_idx])[0]
        confidence = np.max(prediction)
        
        return predicted_label, confidence

    def solve(self, text):
        algo, conf = self.predict(text)
        print(f"Detected Algorithm: {algo} ({conf*100:.2f}%)")
        
        result = ""
        info = ""
        
        if algo == 'Caesar':
            result, info = solve_caesar(text)
        elif algo == 'Vigenere':
            result, info = solve_vigenere(text)
        elif algo == 'Base64':
            result, info = solve_base64(text)
        elif algo == 'XOR':
            result, info = solve_xor(text)
        else:
            result = text
            info = "Unknown Algorithm"
            
        return algo, conf, result, info

if __name__ == "__main__":
    solver = AICryptanalyst()
    
    # Test
    print("\n--- Test 1 (Caesar) ---")
    ct = "IFMMP XPSME"
    a, c, r, i = solver.solve(ct)
    print(f"Decrypted: {r} | Info: {i}")

    print("\n--- Test 2 (Base64) ---")
    ct = "SGVsbG8gV29ybGQ="
    a, c, r, i = solver.solve(ct)
    print(f"Decrypted: {r} | Info: {i}")
