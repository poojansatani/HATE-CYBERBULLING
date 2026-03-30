import pandas as pd
import nltk
import re

# NLTK data download karo (pehli vaar j karvu pade)
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Dataset load karo
df = pd.read_csv('labeled_data.csv')

# Faqt 2 columns j joie apne
df = df[['tweet', 'class']]

print("=== Before Cleaning ===")
print(df['tweet'][0])

# ---- Cleaning Function ----
def clean_text(text):
    # 1. Lowercase karo
    text = text.lower()
    
    # 2. URLs hatavo (http://... wali links)
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # 3. @mentions hatavo
    text = re.sub(r'@\w+', '', text)
    
    # 4. Numbers hatavo
    text = re.sub(r'\d+', '', text)
    
    # 5. Special characters hatavo (faqt letters rakho)
    text = re.sub(r'[^a-z\s]', '', text)
    
    # 6. Extra spaces hatavo
    text = text.strip()
    
    # 7. Stopwords hatavo (the, is, a, an...)
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [w for w in words if w not in stop_words]
    
    return ' '.join(words)

# Cleaning apply karo
df['cleaned_tweet'] = df['tweet'].apply(clean_text)

print("\n=== After Cleaning ===")
print(df['cleaned_tweet'][0])

print("\n=== Class Labels ===")
print(df['class'].value_counts())

# Cleaned data save karo
df.to_csv('cleaned_data.csv', index=False)
print("\n✅ cleaned_data.csv save thai gayu!")