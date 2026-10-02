#!/usr/bin/env python3
"""
Skill: Kumbh Mela Nashik Complete Information & Support System
Provides multilingual information about: Ghats, Shahi Snan dates, transport,
accommodation, medical, lost & found, emergency contacts, rituals, and more.
"""

import json
import argparse

KUMBH_INFO = {
    "ghats": {
        "en": "Main bathing ghats: Ramkund (most sacred), Sita Gufa, Tapkeshwar, Panchvati, Holkar Bridge Ghat, Makhmalabad Ghat. Ramkund is the holiest where Lord Ram bathed.",
        "hi": "मुख्य स्नान घाट: रामकुंड (सबसे पवित्र), सीता गुफा, तपकेश्वर, पंचवटी, होलकर ब्रिज घाट। रामकुंड सबसे पवित्र है जहाँ श्री राम ने स्नान किया था।",
        "mr": "मुख्य स्नान घाट: रामकुंड (सर्वात पवित्र), सीता गुफा, तपकेश्वर, पंचवटी, होळकर ब्रिज घाट. रामकुंड हे सर्वात पवित्र आहे.",
    },
    "shahi_snan": {
        "en": "Shahi Snan (Royal Bath) dates for Nashik Kumbh 2027: Simhastha dates to be announced. Key bathing dates include Purnima (Full Moon), Amavasya (New Moon), and Ekadashi.",
        "hi": "शाही स्नान (राजकीय स्नान) तिथियाँ: सिंहस्थ 2027 की तिथियाँ शीघ्र घोषित होंगी। प्रमुख स्नान: पूर्णिमा, अमावस्या और एकादशी।",
        "mr": "शाही स्नान तारखा: सिंहस्थ 2027 च्या तारखा लवकरच जाहीर होतील. प्रमुख स्नान: पौर्णिमा, अमावस्या आणि एकादशी.",
    },
    "transport": {
        "en": "Getting to Nashik: Train (Nashik Road Station, 8km from city), Bus (CBS - Central Bus Stand), Auto/Taxi available. During Kumbh, special shuttle buses run to Ramkund every 15 mins.",
        "hi": "नासिक कैसे पहुँचें: ट्रेन (नासिक रोड स्टेशन, शहर से 8 किमी), बस (सीबीएस - सेंट्रल बस स्टैंड), ऑटो/टैक्सी उपलब्ध। कुंभ के दौरान हर 15 मिनट में रामकुंड के लिए शटल बसें।",
        "mr": "नाशिकला कसे पोहोचावे: रेल्वे (नाशिक रोड स्टेशन, शहरापासून 8 किमी), बस (CBS), ऑटो/टॅक्सी उपलब्ध. कुंभ दरम्यान दर 15 मिनिटांनी शटल बस.",
    },
    "accommodation": {
        "en": "Accommodation options: 1) Dharamshalas (free/low cost) near Ramkund. 2) Government camps setup during Kumbh. 3) Hotels in Nashik city (Trimbak Road, College Road). 4) MTDC (Maharashtra Tourism) resorts.",
        "hi": "आवास विकल्प: 1) रामकुंड के पास धर्मशालाएं (मुफ्त/सस्ती)। 2) कुंभ के दौरान सरकारी शिविर। 3) नासिक शहर के होटल। 4) एमटीडीसी रिसॉर्ट।",
        "mr": "राहण्याचे पर्याय: 1) रामकुंडजवळ धर्मशाळा. 2) कुंभ दरम्यान सरकारी शिबिरे. 3) नाशिक शहरातील हॉटेल्स. 4) MTDC रिसॉर्ट्स.",
    },
    "emergency": {
        "en": "Emergency Contacts Nashik: Police 100, Ambulance 108, Fire 101, Kumbh Control Room (to be set up), Nashik Municipal Corporation: 0253-2222222, District Hospital: 0253-2453011.",
        "hi": "आपातकालीन संपर्क: पुलिस 100, एम्बुलेंस 108, अग्निशमन 101, नासिक नगर निगम: 0253-2222222, जिला अस्पताल: 0253-2453011।",
        "mr": "आपत्कालीन संपर्क: पोलीस 100, रुग्णवाहिका 108, अग्निशमन 101, नाशिक महानगरपालिका: 0253-2222222, जिल्हा रुग्णालय: 0253-2453011.",
    },
    "rituals": {
        "en": "Key rituals at Nashik Kumbh: 1) Holy dip at Ramkund. 2) Visit Trimbakeshwar Jyotirlinga (28km). 3) Panchvati darshan (5 sacred trees). 4) Kalaram Temple visit. 5) Saptashringi Devi (60km).",
        "hi": "नासिक कुंभ में मुख्य अनुष्ठान: 1) रामकुंड में पवित्र स्नान। 2) त्र्यंबकेश्वर ज्योतिर्लिंग दर्शन (28 किमी)। 3) पंचवटी दर्शन। 4) कालाराम मंदिर। 5) सप्तशृंगी देवी (60 किमी)।",
        "mr": "नाशिक कुंभातील मुख्य विधी: 1) रामकुंडात पवित्र स्नान. 2) त्र्यंबकेश्वर ज्योतिर्लिंग (28 किमी). 3) पंचवटी दर्शन. 4) काळाराम मंदिर. 5) सप्तशृंगी देवी (60 किमी).",
    },
    "lost_found": {
        "en": "Lost & Found at Kumbh Mela: Go to nearest Police Chowky or Kumbh Control Room. Lost children: Announce at public address system near Ramkund. Helpline will be set up during event.",
        "hi": "खोया-पाया: नजदीकी पुलिस चौकी या कुंभ कंट्रोल रूम जाएं। खोए बच्चे: रामकुंड के पास पब्लिक एड्रेस सिस्टम पर घोषणा करें।",
        "mr": "हरवले-सापडले: जवळच्या पोलीस चौकीत किंवा कुंभ नियंत्रण कक्षात जा. हरवलेली मुले: रामकुंडजवळ पब्लिक अड्रेस सिस्टमवर घोषणा करा.",
    },
    "food": {
        "en": "Food at Nashik Kumbh: Free langar (community meals) by various akharas and organizations. Local specialties: Misal Pav, Sabudana Khichdi, Puran Poli. Many dhabas near Ramkund.",
        "hi": "नासिक कुंभ में भोजन: विभिन्न अखाड़ों द्वारा मुफ्त लंगर। स्थानीय व्यंजन: मिसल पाव, साबूदाना खिचड़ी, पुरण पोली।",
        "mr": "नाशिक कुंभात जेवण: विविध आखाड्यांकडून मोफत लंगर. स्थानिक पदार्थ: मिसळ पाव, साबुदाणा खिचडी, पुरण पोळी.",
    },
}

TOPIC_KEYWORDS = {
    "ghats": ["ghat", "घाट", "bathing", "स्नान", "ramkund", "रामकुंड"],
    "shahi_snan": ["shahi", "शाही", "royal bath", "snan", "date", "तिथि", "तारीख"],
    "transport": ["transport", "bus", "train", "reach", "travel", "कैसे पहुँचें", "कसे जायचे", "taxi"],
    "accommodation": ["hotel", "stay", "dharamshala", "accommodation", "रहना", "राहणे", "camp"],
    "emergency": ["emergency", "help", "police", "ambulance", "आपातकाल", "मदत", "अस्पताल"],
    "rituals": ["ritual", "darshan", "temple", "mandir", "मंदिर", "pooja", "पूजा", "trimbak"],
    "lost_found": ["lost", "found", "missing", "child", "खोया", "हरवले", "help"],
    "food": ["food", "eat", "khana", "langar", "भोजन", "जेवण", "restaurant"],
}

def detect_topic(query: str) -> str:
    query_lower = query.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            return topic
    return "general"

def get_info(topic: str, lang: str) -> str:
    if topic == "general":
        msgs = {
            "en": "Welcome to Kumbh Mela Nashik Assistant! Ask about: Ghats, Shahi Snan dates, Transport, Accommodation, Emergency, Rituals, Lost & Found, Food.",
            "hi": "कुंभ मेला नासिक सहायक में आपका स्वागत! पूछें: घाट, शाही स्नान, परिवहन, आवास, आपातकाल, अनुष्ठान, खोया-पाया, भोजन।",
            "mr": "कुंभ मेळा नाशिक सहाय्यकात स्वागत आहे! विचारा: घाट, शाही स्नान, वाहतूक, राहणे, आणीबाणी, विधी, हरवले-सापडले, जेवण.",
        }
        return msgs.get(lang, msgs["en"])
    info = KUMBH_INFO.get(topic, {})
    return info.get(lang, info.get("en", "Information not available."))

def main():
    parser = argparse.ArgumentParser(description="Kumbh Mela Nashik Info System")
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--lang", type=str, default="en", choices=["en","hi","mr","gu","bn","ta","te","kn","pa","ur"])
    args = parser.parse_args()

    topic = detect_topic(args.query)
    response = get_info(topic, args.lang)
    result = {"topic": topic, "language": args.lang, "query": args.query, "response": response}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
