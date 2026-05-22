import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from utils import ALPHABET_EN, clean_text, calculate_frequencies, calculate_ic, calculate_entropy

def preprocess_data(df):
    X = []
    for text in df['ciphertext']:
        # Features: 26 frequencies + 1 IC + 1 Entropy
        freqs = calculate_frequencies(text)
        ic = calculate_ic(text)
        ent = calculate_entropy(text)
        
        features = freqs + [ic, ent]
        X.append(features)
        
    return np.array(X)

# --- Training ---
def train_model():
    print("Loading dataset...")
    df = pd.read_csv('crypto_dataset.csv')
    
    # Drop NaNs just in case
    df = df.dropna()
    
    print("Extracting features...")
    X = preprocess_data(df)
    
    y = df['label'].values
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    num_classes = len(label_encoder.classes_)
    
    # Save Label Encoder for later use
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
        
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    print(f"Training data shape: {X_train.shape}")
    
    # Model Definition
    model = keras.Sequential([
        layers.Input(shape=(28,)), # 26 chars + IC + Entropy
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(32, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    # Train
    print("Starting training...")
    history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))
    
    # Evaluate
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy*100:.2f}%")
    
    # Save Model
    model.save('crypto_classifier.keras')
    print("Model saved as crypto_classifier.keras")

if __name__ == "__main__":
    train_model()
