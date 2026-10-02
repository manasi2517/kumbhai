#!/usr/bin/env python3
"""
🕉️  Kumbh Mela Nashik — Offline Multilingual Voice & Chat Assistant
100% Offline | Auto Language Detection | Voice Output | All Topics
"""

import sys
import json

# ─────────────────────────────────────────────
# 1. LANGUAGE DETECTOR (Unicode-based, offline)
# ─────────────────────────────────────────────
def detect_language(text: str) -> str:
    if not text.strip():
        return "en"
    marathi_words = {"आहे","मला","नाशिक","कुंभ","मेळा","येथे","कसे","आपले","महाराष्ट्र"}
    hindi_words   = {"है","हूं","मुझे","कुंभ","मेला","नासिक","कैसे","मैं","हमें"}
    if any("\u0900" <= c <= "\u097F" for c in text):
        return "mr" if any(w in text for w in marathi_words) else "hi"
    if any("\u0A80" <= c <= "\u0AFF" for c in text): return "gu"
    if any("\u0980" <= c <= "\u09FF" for c in text): return "bn"
    if any("\u0B80" <= c <= "\u0BFF" for c in text): return "ta"
    if any("\u0C00" <= c <= "\u0C7F" for c in text): return "te"
    if any("\u0C80" <= c <= "\u0CFF" for c in text): return "kn"
    if any("\u0A00" <= c <= "\u0A7F" for c in text): return "pa"
    if any("\u0600" <= c <= "\u06FF" for c in text): return "ur"
    return "en"

# ─────────────────────────────────────────────
# 2. KNOWLEDGE BASE (fully offline)
# ─────────────────────────────────────────────
KB = {
    "ghats": {
        "en": "🏊 Main Ghats: Ramkund (holiest), Sita Gufa, Tapkeshwar, Panchvati, Holkar Bridge, Makhmalabad. Ramkund is where Lord Ram bathed.",
        "hi": "🏊 मुख्य घाट: रामकुंड (सबसे पवित्र), सीता गुफा, तपकेश्वर, पंचवटी, होलकर ब्रिज। रामकुंड में श्री राम ने स्नान किया था।",
        "mr": "🏊 मुख्य घाट: रामकुंड (सर्वात पवित्र), सीता गुफा, तपकेश्वर, पंचवटी, होळकर ब्रिज. रामकुंड हे सर्वात पवित्र आहे.",
        "gu": "🏊 મુખ્ય ઘાટ: રામકુંડ, સીતા ગુફા, તપકેશ્વર, પંચવટી, હોળકર બ્રિજ. રામકુંડ સૌથી પવિત્ર છે.",
    },
    "shahi_snan": {
        "en": "🎉 Shahi Snan 2027: Key dates — Purnima (Full Moon), Amavasya (New Moon), Ekadashi. Akharas take royal dip in order of seniority.",
        "hi": "🎉 शाही स्नान 2027: पूर्णिमा, अमावस्या, एकादशी। अखाड़े वरिष्ठता के क्रम में राजकीय स्नान करते हैं।",
        "mr": "🎉 शाही स्नान 2027: पौर्णिमा, अमावस्या, एकादशी. आखाडे ज्येष्ठतेनुसार राजकीय स्नान करतात.",
    },
    "transport": {
        "en": "🚂 Reach Nashik: Train→ Nashik Road Station (8km). Bus→ CBS Central Bus Stand. During Kumbh: shuttle buses every 15 mins to Ramkund.",
        "hi": "🚂 नासिक कैसे पहुँचें: ट्रेन→ नासिक रोड (8 किमी). बस→ CBS. कुंभ में हर 15 मिनट शटल बस।",
        "mr": "🚂 नाशिकला कसे: रेल्वे→ नाशिक रोड (8 किमी). बस→ CBS. कुंभ दरम्यान दर 15 मिनिटांनी शटल बस.",
    },
    "accommodation": {
        "en": "🏠 Stay: Dharamshalas near Ramkund (free/cheap). Govt. tent cities during Kumbh. Hotels on Trimbak Road. MTDC resorts available.",
        "hi": "🏠 आवास: रामकुंड के पास धर्मशालाएं. सरकारी टेंट शहर. होटल: त्र्यंबक रोड. MTDC रिसॉर्ट।",
        "mr": "🏠 राहणे: रामकुंडजवळ धर्मशाळा. सरकारी तंबू. त्र्यंबक रोडवर हॉटेल्स. MTDC रिसॉर्ट.",
    },
    "emergency": {
        "en": "🚨 Emergency: Police 100 | Ambulance 108 | Fire 101 | Municipal Corp: 0253-2222222 | Hospital: 0253-2453011",
        "hi": "🚨 आपातकाल: पुलिस 100 | एम्बुलेंस 108 | अग्निशमन 101 | नगर निगम: 0253-2222222 | अस्पताल: 0253-2453011",
        "mr": "🚨 आणीबाणी: पोलीस 100 | रुग्णवाहिका 108 | अग्निशमन 101 | महानगरपालिका: 0253-2222222",
    },
    "rituals": {
        "en": "🙏 Rituals: 1) Holy dip at Ramkund 2) Trimbakeshwar Jyotirlinga (28km) 3) Panchvati darshan 4) Kalaram Temple 5) Saptashringi Devi (60km)",
        "hi": "🙏 अनुष्ठान: 1) रामकुंड स्नान 2) त्र्यंबकेश्वर (28 किमी) 3) पंचवटी 4) कालाराम मंदिर 5) सप्तशृंगी देवी (60 किमी)",
        "mr": "🙏 विधी: 1) रामकुंड स्नान 2) त्र्यंबकेश्वर (28 किमी) 3) पंचवटी 4) काळाराम मंदिर 5) सप्तशृंगी देवी (60 किमी)",
    },
    "lost_found": {
        "en": "🔍 Lost & Found: Go to nearest Police Chowky or Kumbh Control Room. Missing child? Announce at Ramkund PA system.",
        "hi": "🔍 खोया-पाया: नजदीकी पुलिस चौकी या कुंभ कंट्रोल रूम जाएं। बच्चा खोया? रामकुंड PA सिस्टम पर घोषणा करें।",
        "mr": "🔍 हरवले: जवळच्या पोलीस चौकीत जा. मूल हरवले? रामकुंड PA सिस्टमवर घोषणा करा.",
    },
    "food": {
        "en": "🍱 Food: Free langar by akharas. Local food: Misal Pav, Sabudana Khichdi, Puran Poli, Poha. Many dhabas near Ramkund.",
        "hi": "🍱 भोजन: अखाड़ों का मुफ्त लंगर. स्थानीय: मिसल पाव, साबूदाना खिचड़ी, पुरण पोली।",
        "mr": "🍱 जेवण: आखाड्यांचे मोफत लंगर. स्थानिक: मिसळ पाव, साबुदाणा खिचडी, पुरण पोळी.",
    },
    "weather": {
        "en": "🌤️ Nashik weather during Kumbh (July-Sept): Monsoon season. Expect rain. Carry raincoat/umbrella. Temp: 20-30°C.",
        "hi": "🌤️ कुंभ के दौरान नासिक का मौसम (जुलाई-सितंबर): मानसून. वर्षा संभव. रेनकोट साथ रखें. तापमान: 20-30°C।",
        "mr": "🌤️ कुंभ दरम्यान (जुलै-सप्टें): मान्सून. पाऊस शक्य. रेनकोट घ्या. तापमान: 20-30°C.",
    },
}

TOPIC_KEYWORDS = {
    "ghats":       ["ghat","घाट","bathing","ramkund","रामकुंड","snap","snan","स्नान"],
    "shahi_snan":  ["shahi","शाही","royal","date","तिथि","तारीख","snan","2027"],
    "transport":   ["transport","bus","train","reach","travel","कैसे","कसे","taxi","auto","railway"],
    "accommodation":["hotel","stay","dharamshala","accommodation","रहना","राहणे","camp","tent"],
    "emergency":   ["emergency","help","police","ambulance","आपातकाल","मदत","hospital","108","100"],
    "rituals":     ["ritual","darshan","temple","mandir","मंदिर","pooja","पूजा","trimbak","kalaram"],
    "lost_found":  ["lost","found","missing","child","खोया","हरवले","गुम"],
    "food":        ["food","eat","khana","langar","भोजन","जेवण","misal","restaurant","dhaba"],
    "weather":     ["weather","rain","mausam","monsoon","मौसम","पाऊस","temperature","umbrella"],
}

GREETINGS = {
    "en": "🙏 Jai Shree Ram! Welcome to Kumbh Mela Nashik Assistant!",
    "hi": "🙏 जय श्री राम! कुंभ मेला नासिक सहायक में आपका स्वागत है!",
    "mr": "🙏 जय श्री राम! कुंभ मेळा नाशिक सहाय्यकात स्वागत!",
    "gu": "🙏 જય શ્રી રામ! કુંભ મેળા નાશિકમાં સ્વાગત!",
    "bn": "🙏 জয় শ্রী রাম! কুম্ভ মেলায় স্বাগতম!",
    "ta": "🙏 ஜெய் ஸ்ரீ ராம்! கும்ப மேளாவிற்கு வரவேற்கிறோம்!",
    "te": "🙏 జయ్ శ్రీ రామ్! కుంభ మేళాకు స్వాగతం!",
    "kn": "🙏 ಜಯ ಶ್ರೀ ರಾಮ್! ಕುಂಭ ಮೇಳಕ್ಕೆ ಸ್ವಾಗತ!",
    "pa": "🙏 ਜੈ ਸ਼੍ਰੀ ਰਾਮ! ਕੁੰਭ ਮੇਲੇ ਵਿੱਚ ਜੀ ਆਇਆਂ!",
    "ur": "🙏 جے شری رام! کمبھ میلے میں خوش آمدید!",
}

FOLLOW_UP = {
    "en": "\n\nCan I help you with anything else? (ghats/transport/food/emergency/rituals/accommodation/weather)",
    "hi": "\n\nक्या मैं और कुछ बता सकता हूँ? (घाट/परिवहन/भोजन/आपातकाल/अनुष्ठान/आवास/मौसम)",
    "mr": "\n\nमी आणखी काही मदत करू का? (घाट/वाहतूक/जेवण/आणीबाणी/विधी/राहणे/हवामान)",
}

def get_topic(query: str) -> str:
    q = query.lower()
    for topic, kws in TOPIC_KEYWORDS.items():
        if any(k in q for k in kws):
            return topic
    return "general"

def get_response(query: str) -> dict:
    lang = detect_language(query)
    topic = get_topic(query)
    if topic == "general":
        keys = list(KB.keys())
        resp = GREETINGS.get(lang, GREETINGS["en"]) + "\n\nAsk about: " + " | ".join(keys)
    else:
        info = KB[topic]
        resp = info.get(lang, info.get("en", "Information not available."))
    resp += FOLLOW_UP.get(lang, FOLLOW_UP["en"])
    return {"lang": lang, "topic": topic, "response": resp}

# ─────────────────────────────────────────────
# 3. OPTIONAL: VOICE OUTPUT (pyttsx3 offline TTS)
# ─────────────────────────────────────────────
def speak(text: str, lang_code: str = "en"):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass  # TTS not available — text-only mode

# ─────────────────────────────────────────────
# 4. MAIN CHAT LOOP
# ─────────────────────────────────────────────
def run_chat():
    print("=" * 55)
    print("🕉️   KUMBH MELA NASHIK — OFFLINE AI ASSISTANT")
    print("=" * 55)
    print("Type your question in ANY language.")
    print("Type 'quit' or 'exit' to leave.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nJai Shree Ram! 🙏"); break
        if not user_input: continue
        if user_input.lower() in ["quit","exit","bye","alvida","बाय","निघतो"]:
            print("🙏 Jai Shree Ram! Safe journey!"); break
        result = get_response(user_input)
        print(f"\n[Detected: {result['lang']} | Topic: {result['topic']}]")
        print(f"Assistant: {result['response']}\n")
        speak(result["response"], result["lang"])

if __name__ == "__main__":
    run_chat()
