import streamlit as st
import pickle
import re
from langdetect import detect
from deep_translator import GoogleTranslator

# --- આ લાઈન હંમેશા સૌથી ઉપર હોવી જોઈએ ---
st.set_page_config(page_title="Cyberbullying Detector", page_icon="🛡️")

# ---- Model ane vectorizer load karo ----
@st.cache_resource
def load_models():
    try:
        with open('best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except Exception as e:
        return None, None

model, vectorizer = load_models()

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
    raw_text = text.strip()
    working_text = raw_text.lower()
    
    # Translation Logic
    try:
        # જો ટેક્સ્ટમાં ગુજરાતી/હિન્દી અક્ષરો હોય અથવા લાંબુ વાક્ય હોય
        translator = GoogleTranslator(source='auto', target='en')
        translated = translator.translate(raw_text)
        
        if translated.lower() != raw_text.lower():
            working_text = translated.lower()
            st.info(f"✨ Translated: {working_text}")
    except:
        pass

    # Step 1: Normal Keywords
    for kw in normal_keywords:
        if kw in working_text:
            return 2

    # Step 2: Hate Keywords
    for kw in hate_keywords:
        if kw in working_text:
            return 0

    # Step 3: Offensive Keywords
    for kw in offensive_keywords:
        if kw in working_text:
            return 1

    # Step 4: ML Model
    if model and vectorizer:
        cleaned = clean_text(working_text)
        vectorized = vectorizer.transform([cleaned])
        return model.predict(vectorized)[0]
    
    return 2 # Default

# ---- Streamlit UI ----
st.title("🛡️ Cyberbullying Detector")
st.write("લખો ગમે તે ભાષામાં, અમે શોધીશું સાયબર બુલિંગ!")

user_input = st.text_area("✍️ અહીં મેસેજ લખો:", height=100)

if st.button("🔍 Analyze"):
    if user_input.strip() == "":
        st.warning("પહેલા કંઈક લખો!")
    else:
        if model is None:
            st.error("Model file (best_model.pkl) મળી નથી. મહેરબાની કરીને ફાઈલ અપલોડ કરો.")
        else:
            with st.spinner('Checking...'):
                result = predict(user_input)
                
                st.subheader("Result:")
                if result == 0:
                    st.error("🚨 Hate Speech Detected!")
                elif result == 1:
                    st.warning("⚠️ Offensive Language Detected!")
                else:
                    st.success("✅ Normal Message")

st.markdown("---")
st.caption("Developed by Poojan Satani | AI Cyberbullying Detection Project")
