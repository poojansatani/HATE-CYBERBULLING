import streamlit as st
import pickle
import re

# Model ane vectorizer load karo
with open('best_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
    
# ---- Keyword Lists ----
hate_keywords = [
    'hate you',' should die', 'deserve to die', 'should not exist',
    'wipe them out', 'wipe out', 'get rid of them',
    'eliminate them', 'exterminate', 'subhuman', 'sub-human',
    'vermin', 'parasite', 'filth', 'scum', 'they should all',
    'kill them', 'kill all', 'death to', 'hate all',
    'i hate all', 'hate every', 'should be destroyed',
    'should be eliminated', 'should be removed',
    'should all die', 'should all suffer', 'should all burn',
    'worthless creatures', 'worthless beings', 'not human',
    'are animals', 'are monsters', 'are demons', 'are vermin',
    'are cockroaches', 'are rats', 'are parasites',
    'cease to exist', 'should disappear forever',
    'deserve to suffer', 'deserve nothing', 'have no right to live'
]

offensive_keywords = [
    'you are idiot', 'you are an idiot', 'you idiot',
    'you are stupid', 'you stupid', 'you are dumb', 'you dumb',
    'you are moron', 'you moron', 'you are loser', 'you loser',
    'you are fool', 'you fool', 'you are pathetic',
    'you are worthless', 'you are useless', 'you are ugly',
    'shut up', 'shut your', 'go away', 'nobody likes you',
    'you are a failure', 'you are trash', 'you are garbage',
    'you are disgusting', 'you are annoying', 'you are horrible',
    'you are the worst', 'you are brain dead', 'you are a joke',
    'you are embarrassing', 'you are incompetent',
    'what a fool', 'what a loser', 'what an idiot',
    'what a moron', 'such a fool', 'complete idiot',
    'complete moron', 'absolute idiot', 'absolute moron',
    'dumb fool', 'brainless', 'mindless fool'
]

normal_keywords = [
    'good morning', 'good evening', 'good night', 'good afternoon',
    'have a great', 'have a good', 'have a nice', 'have a wonderful',
    'thank you', 'thanks so much', 'well done', 'congratulations',
    'i hope you', 'hope you are', 'take care', 'stay safe',
    'i love you', 'love you', 'i appreciate', 'so proud',
    'beautiful day', 'wonderful day', 'great day', 'lovely day',
    'feeling happy', 'feeling good', 'feeling great', 'feeling blessed',
    'i am grateful', 'so grateful', 'feeling lonely', 'feeling sad',
    'i miss you', 'looking forward', 'excited about', 'cant wait',
    'you are good', 'you are great', 'you are amazing',
    'you are wonderful', 'you are beautiful', 'you are kind',
    'you are smart', 'you are talented', 'you are awesome'
]

# ---- Text Cleaning ----
def clean_text(text):
    t = text.lower()
    t = re.sub(r'http\S+|www\S+', '', t)
    t = re.sub(r'@\w+', '', t)
    t = re.sub(r'\d+', '', t)
    t = re.sub(r'[^a-z\s]', '', t)
    return t.strip()

# ---- Smart Predict Function ----
def predict(text):
    text_lower = text.lower()

    # Step 1: Normal keywords check (pehla)
    for kw in normal_keywords:
        if kw in text_lower:
            return 2  # Normal

    # Step 2: Hate keywords check
    for kw in hate_keywords:
        if kw in text_lower:
            return 0  # Hate Speech

    # Step 3: Offensive keywords check
    for kw in offensive_keywords:
        if kw in text_lower:
            return 1  # Offensive

    # Step 4: ML Model (jyare koi keyword na male)
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    return model.predict(vectorized)[0]

# ---- Streamlit UI ----
st.title("🛡️ Cyberbullying & Hate Speech Detector")
st.write("Koi pan text lakho — model detect karse ke te "
         "Hate Speech che, Offensive che, ke Normal!")

user_input = st.text_area("✍️ Text yahan lakho:", height=150)

if st.button("🔍 Detect karo"):
    if user_input.strip() == "":
        st.warning("Pehla koi text lakho!")
    else:
        result = predict(user_input)
        if result == 0:
            st.error("🚨 Hate Speech detected!")
        elif result == 1:
            st.warning("⚠️ Offensive Language detected!")
        else:
            st.success("✅ Normal Message — koi problem nathi!")