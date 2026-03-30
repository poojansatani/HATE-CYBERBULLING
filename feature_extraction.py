import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pickle

# Cleaned data load karo
df = pd.read_csv('cleaned_data.csv')

# Khali rows hatavo
df = df.dropna(subset=['cleaned_tweet'])

print("=== Dataset ready ===")
print(f"Total rows: {len(df)}")

# X = input (tweet text)
# y = output (class: 0, 1, 2)
X = df['cleaned_tweet']
y = df['class']

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    max_features=5000,   # Top 5000 words j laishu
    ngram_range=(1, 2)   # Single words + word pairs
)

# Text ne numbers ma convert karo
X_vectorized = vectorizer.fit_transform(X)

print(f"\n=== Vectorized Shape ===")
print(f"Rows: {X_vectorized.shape[0]}, Features: {X_vectorized.shape[1]}")

# Train/Test split — 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"\n=== Split Done ===")
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples:  {X_test.shape[0]}")

# Vectorizer save karo (future ma use karva)
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

# Train/Test data save karo
import scipy.sparse as sp
sp.save_npz('X_train.npz', X_train)
sp.save_npz('X_test.npz', X_test)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("\n✅ Badhu save thai gayu!")