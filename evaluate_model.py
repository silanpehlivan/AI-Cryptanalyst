import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pickle
from sklearn.metrics import accuracy_score
from utils import calculate_frequencies, calculate_ic, calculate_entropy

def preprocess_data(df):
    X = []
    for text in df['ciphertext']:
        try:
            freqs = calculate_frequencies(text)
            ic = calculate_ic(text)
            ent = calculate_entropy(text)
            features = freqs + [ic, ent]
            X.append(features)
        except Exception as e:
            print(f"Error processing: {text[:10]}... {e}")
            X.append([0]*28)
    return np.array(X)

def evaluate():
    print("Loading resources...")
    try:
        model = keras.models.load_model('crypto_classifier.keras')
        with open('label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
        df = pd.read_csv('crypto_dataset.csv').dropna()
    except Exception as e:
        print(f"Failed to load resources: {e}")
        return

    print(f"Evaluating on {len(df)} samples...")
    X = preprocess_data(df)
    y_true = df['label'].values
    
    # Predict
    y_pred_probs = model.predict(X, verbose=0)
    y_pred_indices = np.argmax(y_pred_probs, axis=1)
    y_pred_labels = label_encoder.inverse_transform(y_pred_indices)
    
    acc = accuracy_score(y_true, y_pred_labels)
    print(f"Overall Success Rate (Accuracy): {acc*100:.2f}%")
    
    # Per-class accuracy
    print("\nPer-class Accuracy:")
    for label in label_encoder.classes_:
        mask = y_true == label
        if np.sum(mask) > 0:
            class_acc = accuracy_score(y_true[mask], y_pred_labels[mask])
            print(f"{label}: {class_acc*100:.2f}%")

if __name__ == "__main__":
    evaluate()
