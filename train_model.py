import pandas as pd
import scipy.sparse as sp
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Data load karo
X_train = sp.load_npz('X_train.npz')
X_test = sp.load_npz('X_test.npz')
y_train = pd.read_csv('y_train.csv').values.ravel()
y_test = pd.read_csv('y_test.csv').values.ravel()

print("=== Data loaded! ===\n")

# ---- Model 1: Naive Bayes ----
print("Training Naive Bayes...")
nb = MultinomialNB()
nb.fit(X_train, y_train)
nb_pred = nb.predict(X_test)
nb_acc = accuracy_score(y_test, nb_pred)
print(f"Naive Bayes Accuracy: {nb_acc:.4f}")

# ---- Model 2: Logistic Regression ----
print("\nTraining Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
lr_acc = accuracy_score(y_test, lr_pred)
print(f"Logistic Regression Accuracy: {lr_acc:.4f}")

# ---- Model 3: SVM ----
print("\nTraining SVM...")
svm = LinearSVC(random_state=42, max_iter=2000)
svm.fit(X_train, y_train)
svm_pred = svm.predict(X_test)
svm_acc = accuracy_score(y_test, svm_pred)
print(f"SVM Accuracy: {svm_acc:.4f}")

# ---- Best model choose karo ----
print("\n=== Model Comparison ===")
models = {
    'Naive Bayes': (nb, nb_acc),
    'Logistic Regression': (lr, lr_acc),
    'SVM': (svm, svm_acc)
}

for name, (model, acc) in models.items():
    print(f"{name}: {acc:.4f}")

best_name = max(models, key=lambda x: models[x][1])
best_model = models[best_name][0]
print(f"\n🏆 Best Model: {best_name}")

# ---- Best model ni detail report ----
best_pred = best_model.predict(X_test)
print("\n=== Classification Report ===")
print(classification_report(y_test, best_pred,
      target_names=['Hate Speech', 'Offensive', 'Normal']))

# ---- Best model save karo ----
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

print("\n✅ best_model.pkl save thai gayu!")