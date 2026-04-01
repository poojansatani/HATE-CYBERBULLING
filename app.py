import streamlit as st
import pickle
import re
import requests
from deep_translator import GoogleTranslator

# ---- Model ane Vectorizer Load ----
with open('best_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# ---- Language Names ----
lang_names = {
    'gu': 'Gujarati 🇮🇳', 'hi': 'Hindi 🇮🇳', 'en': 'English 🇬🇧',
    'mr': 'Marathi 🇮🇳', 'ta': 'Tamil 🇮🇳', 'te': 'Telugu 🇮🇳',
    'bn': 'Bengali 🇮🇳', 'ur': 'Urdu 🇵🇰', 'fr': 'French 🇫🇷',
    'de': 'German 🇩🇪', 'es': 'Spanish 🇪🇸', 'ar': 'Arabic 🇸🇦',
}

# ---- Keyword Lists ----
hate_keywords = [
    'should die', 'deserve to die', 'should not exist',
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
    'you are smart', 'you are talented', 'you are awesome',
    'my name is', 'i am from', 'nice to meet', 'my friend',
    'is my friend', 'meat is my', 'wise boy', 'good boy',
    'have to go', 'going home', 'i have to'
]

# ---- Text Clean ----
def clean_text(text):
    t = text.lower()
    t = re.sub(r'http\S+|www\S+', '', t)
    t = re.sub(r'@\w+', '', t)
    t = re.sub(r'\d+', '', t)
    t = re.sub(r'[^a-z\s]', '', t)
    return t.strip()

# ---- Romanized to Gujarati Script ----
def romanized_to_gujarati(text):
    """Google Input Tools thi Romanized Gujarati ne Script ma convert karo"""
    try:
        words = text.strip().split()
        result_words = []
        for word in words:
            url = "https://inputtools.google.com/request"
            params = {
                'text': word,
                'itc': 'gu-t-i0-und',
                'num': 1,
                'cp': 0,
                'cs': 1,
                'ie': 'utf-8',
                'oe': 'utf-8',
            }
            r = requests.get(url, params=params, timeout=5)
            d = r.json()
            if d[0] == 'SUCCESS' and d[1] and d[1][0][1]:
                result_words.append(d[1][0][1][0])
            else:
                result_words.append(word)
        return ' '.join(result_words)
    except Exception:
        return text

# ---- Detect and Translate ----
def detect_and_translate(text):
    try:
        # Check: Gujarati script che? (Unicode range)
        has_gujarati = any('\u0A80' <= c <= '\u0AFF' for c in text)
        # Check: Hindi/Devanagari script che?
        has_hindi = any('\u0900' <= c <= '\u097F' for c in text)
        # Check: Arabic/Urdu script che?
        has_arabic = any('\u0600' <= c <= '\u06FF' for c in text)

        if has_gujarati:
            # Gujarati script — seedhu translate karo
            translated = GoogleTranslator(source='gu', target='en').translate(text)
            return 'Gujarati 🇮🇳', translated

        elif has_hindi:
            # Hindi script — seedhu translate karo
            translated = GoogleTranslator(source='hi', target='en').translate(text)
            return 'Hindi 🇮🇳', translated

        elif has_arabic:
            translated = GoogleTranslator(source='ar', target='en').translate(text)
            return 'Arabic/Urdu 🌍', translated

        else:
            # Romanized text — pehla Gujarati script ma convert karo
            gujarati_script = romanized_to_gujarati(text)

            # Jо conversion thayelu hoy (original thi alag)
            if gujarati_script != text:
                st.caption(f"🔤 Gujarati script: *{gujarati_script}*")
                # Hve Gujarati script thi English ma translate karo
                translated = GoogleTranslator(
                    source='gu', target='en').translate(gujarati_script)
                return 'Gujarati (Romanized) 🇮🇳', translated
            else:
                # Pure English lage che
                return 'English 🇬🇧', text

    except Exception:
        # Fallback — auto detect thi translate
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(text)
            if translated.strip().lower() != text.strip().lower():
                return '🌐 Auto-detected', translated
            return 'English 🇬🇧', text
        except Exception:
            return 'English 🇬🇧', text

# ---- Predict Function ----
def predict(text):
    text_lower = text.lower()

    # Step 1: Normal keywords
    for kw in normal_keywords:
        if kw in text_lower:
            return 2

    # Step 2: Hate keywords
    for kw in hate_keywords:
        if kw in text_lower:
            return 0

    # Step 3: Offensive keywords
    for kw in offensive_keywords:
        if kw in text_lower:
            return 1

    # Step 4: ML Model
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    return model.predict(vectorized)[0]

# ---- Streamlit UI ----
st.set_page_config(page_title="Hate Speech Detector", page_icon="🛡️")
st.title("🛡️ Cyberbullying & Hate Speech Detector")
st.write("Koi pan text lakho **ગુજરાતી, हिंदी, English** — model detect karse!")
st.info("💡 Best results: ગુજરાતી લિપિ (ક, ખ, ગ...) ya English use karo. Romanized Gujarati pan chalse!")

user_input = st.text_area(
    "✍️ Text yahan lakho:",
    height=150,
    placeholder="ગુજરાતી, हिंदी, English, ya Romanized Gujarati ma lakho..."
)

if st.button("🔍 Detect karo"):
    if user_input.strip() == "":
        st.warning("⚠️ Pehla koi text lakho!")
    else:
        with st.spinner("🔄 Analyzing..."):
            lang_label, translated = detect_and_translate(user_input)

            # Language info show karo
            if 'English' not in lang_label:
                st.info(f"🌐 Language: **{lang_label}**")
                st.caption(f"📝 Translated to English: *{translated}*")

            result = predict(translated)

        if result == 0:
            st.error("🚨 Hate Speech detected!")
        elif result == 1:
            st.warning("⚠️ Offensive Language detected!")
        else:
            st.success("✅ Normal Message — koi problem nathi!")
