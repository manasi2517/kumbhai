#!/usr/bin/env python3
"""
Skill: Kumbh Mela Multilingual Language Detector & Translator
Detects language of user input and provides translated response in their language.
Supports: Hindi, Marathi, English, Gujarati, Bengali, Tamil, Telugu, Kannada, Punjabi, Urdu
"""

import sys
import json
import argparse

LANGUAGE_MAP = {
    "hindi":    {"code": "hi", "greeting": "नमस्ते! कुंभ मेला नासिक में आपका स्वागत है।"},
    "marathi":  {"code": "mr", "greeting": "नमस्कार! कुंभ मेळा नाशिक मध्ये आपले स्वागत आहे।"},
    "english":  {"code": "en", "greeting": "Welcome to Kumbh Mela Nashik! How can I assist you?"},
    "gujarati": {"code": "gu", "greeting": "કુંભ મેળા નાશિકમાં આપનું સ્વાગત છે!"},
    "bengali":  {"code": "bn", "greeting": "কুম্ভ মেলা নাসিকে আপনাকে স্বাগতম!"},
    "tamil":    {"code": "ta", "greeting": "கும்ப மேளா நாசிக்கிற்கு வரவேற்கிறோம்!"},
    "telugu":   {"code": "te", "greeting": "కుంభ మేళా నాసిక్‌కు స్వాగతం!"},
    "kannada":  {"code": "kn", "greeting": "ಕುಂಭ ಮೇಳ ನಾಶಿಕ್‌ಗೆ ಸ್ವಾಗತ!"},
    "punjabi":  {"code": "pa", "greeting": "ਕੁੰਭ ਮੇਲਾ ਨਾਸਿਕ ਵਿੱਚ ਜੀ ਆਇਆਂ ਨੂੰ!"},
    "urdu":     {"code": "ur", "greeting": "کمبھ میلہ ناشک میں خوش آمدید!"},
}

SCRIPT_PATTERNS = {
    "devanagari": ["hindi", "marathi"],
    "gujarati_script": ["gujarati"],
    "bengali_script": ["bengali"],
    "tamil_script": ["tamil"],
    "telugu_script": ["telugu"],
    "kannada_script": ["kannada"],
    "gurmukhi": ["punjabi"],
    "arabic": ["urdu"],
}

def detect_language(text: str) -> str:
    if not text:
        return "english"
    has_devanagari = any("\u0900" <= c <= "\u097F" for c in text)
    has_gujarati   = any("\u0A80" <= c <= "\u0AFF" for c in text)
    has_bengali    = any("\u0980" <= c <= "\u09FF" for c in text)
    has_tamil      = any("\u0B80" <= c <= "\u0BFF" for c in text)
    has_telugu     = any("\u0C00" <= c <= "\u0C7F" for c in text)
    has_kannada    = any("\u0C80" <= c <= "\u0CFF" for c in text)
    has_gurmukhi   = any("\u0A00" <= c <= "\u0A7F" for c in text)
    has_arabic     = any("\u0600" <= c <= "\u06FF" for c in text)

    marathi_words = ["आहे", "मला", "नाशिक", "कुंभ", "मेळा", "येथे", "कसे"]
    hindi_words   = ["है", "हूं", "मुझे", "कुंभ", "मेला", "नासिक", "कैसे"]

    if has_devanagari:
        return "marathi" if any(w in text for w in marathi_words) else "hindi"
    if has_gujarati:   return "gujarati"
    if has_bengali:    return "bengali"
    if has_tamil:      return "tamil"
    if has_telugu:     return "telugu"
    if has_kannada:    return "kannada"
    if has_gurmukhi:   return "punjabi"
    if has_arabic:     return "urdu"
    return "english"

def get_greeting(language: str) -> str:
    lang = LANGUAGE_MAP.get(language, LANGUAGE_MAP["english"])
    return lang["greeting"]

def main():
    parser = argparse.ArgumentParser(description="Kumbh Mela Language Detector")
    parser.add_argument("--text", type=str, required=True, help="User input text")
    parser.add_argument("--output", type=str, default="json", choices=["json","text"])
    args = parser.parse_args()

    detected = detect_language(args.text)
    greeting = get_greeting(detected)
    result = {
        "detected_language": detected,
        "language_code": LANGUAGE_MAP.get(detected, {}).get("code", "en"),
        "greeting": greeting,
        "input_text": args.text
    }

    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Detected: {detected}\nGreeting: {greeting}")

if __name__ == "__main__":
    main()
