import pandas as pd
import scipy.sparse as sp
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

# ---- Original dataset load karo ----
df_original = pd.read_csv('cleaned_data.csv')
df_original = df_original[['cleaned_tweet', 'class']].dropna()

# ---- Custom dataset load ane clean karo ----
df_custom = pd.read_csv('custom_dataset.csv')

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return text.strip()

df_custom['cleaned_tweet'] = df_custom['tweet'].apply(clean_text)
df_custom = df_custom[['cleaned_tweet', 'class']].dropna()

# ---- Merge karo ----
df = pd.concat([df_original, df_custom], ignore_index=True)
df = df.drop_duplicates(subset=['cleaned_tweet'])
print(f"Total merged rows: {len(df)}")
print(f"\nClass distribution:")
print(df['class'].value_counts())

# ---- Features ----
X = df['cleaned_tweet']
y = df['class']

vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42, stratify=y
)

# ---- Models train karo ----
print("\nTraining Naive Bayes...")
nb = MultinomialNB()
nb.fit(X_train, y_train)
nb_acc = accuracy_score(y_test, nb.predict(X_test))
print(f"Naive Bayes: {nb_acc:.4f}")

print("Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42,
                        class_weight={0: 2, 1: 2, 2: 1})
lr.fit(X_train, y_train)
lr_acc = accuracy_score(y_test, lr.predict(X_test))
print(f"Logistic Regression: {lr_acc:.4f}")

print("Training SVM...")
svm = LinearSVC(random_state=42, max_iter=2000,
                class_weight={0: 2, 1: 2, 2: 1})
svm.fit(X_train, y_train)
svm_acc = accuracy_score(y_test, svm.predict(X_test))
print(f"SVM: {svm_acc:.4f}")

# ---- Best model ----
models = {
    'Naive Bayes': (nb, nb_acc),
    'Logistic Regression': (lr, lr_acc),
    'SVM': (svm, svm_acc)
}

best_name = max(models, key=lambda x: models[x][1])
best_model = models[best_name][0]
best_pred = best_model.predict(X_test)

print(f"\n🏆 Best Model: {best_name}")
print("\n=== Classification Report ===")
print(classification_report(y_test, best_pred,
      target_names=['Hate Speech', 'Offensive', 'Normal']))

# ---- Save karo ----
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("✅ Model ane vectorizer save thai gaya!")