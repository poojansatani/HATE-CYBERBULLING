import streamlit as st
import pickle
import re
from langdetect import detect
from deep_translator import GoogleTranslator

# --- આ લાઈન હવે સૌથી ઉપર છે, એટલે હવે એરર નહીં આવે ---
st.set_page_config(page_title="Hate Speech Detector", page_icon="🛡️")

# ---- Model ane vectorizer load karo ----
@st.cache_resource
def load_models():
    with open('best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

# મોડેલ લોડ કરવાનો પ્રયત્ન કરો
model = None
vectorizer = None
try:
    model, vectorizer = load_models()
except Exception as e:
    st.error(f"Error loading models: {e}")

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

# ---- Text Cleaning Function ----
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
    
    try:
        detected_lang = detect(raw_text)
        if detected_lang != 'en':
            working_text = GoogleTranslator(source='auto', target='en').translate(raw_text).lower()
            st.info(f"🌐 Detected Language: **{detected_lang}** | Translated: *{working_text}*")
    except:
        pass

    for kw in normal_keywords:
        if kw in working_text:
            return 2

    for kw in hate_keywords:
        if kw in working_text:
            return 0

    for kw in offensive_keywords:
        if kw in working_text:
            return 1

    if model and vectorizer:
        cleaned = clean_text(working_text)
        vectorized = vectorizer.transform([cleaned])
        return model.predict(vectorized)[0]
    return 2 # Default to normal if model fails

# ---- Streamlit UI ----
st.title("🛡️ Cyberbullying & Hate Speech Detector")
st.write("તમે કોઈ પણ ભાષામાં ટેક્સ્ટ લખી શકો છો (ગુજરાતી, હિન્દી, ઇંગ્લિશ).")

user_input = st.text_area("✍️ અહીં મેસેજ લખો:", height=150)

if st.button("🔍 Detect કરો"):
    if user_input.strip() == "":
        st.warning("પહેલા કંઈક ટેક્સ્ટ લખો!")
    else:
        with st.spinner('Checking...'):
            result = predict(user_input)
            
            st.subheader("Result:")
            if result == 0:
                st.error("🚨 **Hate Speech Detected!**")
                st.write("આ મેસેજમાં નફરત ફેલાવતા શબ્દો છે.")
            elif result == 1:
                st.warning("⚠️ **Offensive Language Detected!**")
                st.write("આ મેસેજ અપમાનજનક હોઈ શકે છે.")
            else:
                st.success("✅ **Normal Message**")
                st.write("આ મેસેજ સુરક્ષિત છે.")

st.markdown("---")
st.caption("AI Model for Cyberbullying Detection | Developed by Poojan Satani")
