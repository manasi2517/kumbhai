import 'dart:core';

class LanguageDetectorService {
  static String detect(String text) {
    if (text.trim().isEmpty) return 'en';

    final marathiWords = ['आहे','मला','नाशिक','कुंभ','मेळा','येथे','कसे','आपले','महाराष्ट्र'];
    final hindiWords   = ['है','हूं','मुझे','कुंभ','मेला','नासिक','कैसे','मैं','हमें'];

    bool hasDevanagari = text.runes.any((r) => r >= 0x0900 && r <= 0x097F);
    bool hasGujarati   = text.runes.any((r) => r >= 0x0A80 && r <= 0x0AFF);
    bool hasBengali    = text.runes.any((r) => r >= 0x0980 && r <= 0x09FF);
    bool hasTamil      = text.runes.any((r) => r >= 0x0B80 && r <= 0x0BFF);
    bool hasTelugu     = text.runes.any((r) => r >= 0x0C00 && r <= 0x0C7F);
    bool hasKannada    = text.runes.any((r) => r >= 0x0C80 && r <= 0x0CFF);
    bool hasGurmukhi   = text.runes.any((r) => r >= 0x0A00 && r <= 0x0A7F);
    bool hasArabic     = text.runes.any((r) => r >= 0x0600 && r <= 0x06FF);

    if (hasDevanagari) {
      return marathiWords.any((w) => text.contains(w)) ? 'mr' : 'hi';
    }
    if (hasGujarati)  return 'gu';
    if (hasBengali)   return 'bn';
    if (hasTamil)     return 'ta';
    if (hasTelugu)    return 'te';
    if (hasKannada)   return 'kn';
    if (hasGurmukhi)  return 'pa';
    if (hasArabic)    return 'ur';
    return 'en';
  }

  static String getGreeting(String langCode) {
    const greetings = {
      'hi': '🙏 जय श्री राम! नासिक कुंभ मेला सहायक में आपका स्वागत!',
      'mr': '🙏 जय श्री राम! नाशिक कुंभ मेळा सहाय्यकात स्वागत!',
      'en': '🙏 Jai Shree Ram! Welcome to Kumbh Mela Nashik Assistant!',
      'gu': '🙏 જય શ્રી રામ! કુંભ મેળા નાશિક!',
      'bn': '🙏 জয় শ্রী রাম! কুম্ভ মেলা নাসিক!',
      'ta': '🙏 ஜெய் ஸ்ரீ ராம்! கும்ப மேளா நாசிக்!',
      'te': '🙏 జయ్ శ్రీ రామ్! కుంభ మేళా నాసిక్!',
      'kn': '🙏 ಜಯ ಶ್ರೀ ರಾಮ್! ಕುಂಭ ಮೇಳ ನಾಶಿಕ್!',
      'pa': '🙏 ਜੈ ਸ਼੍ਰੀ ਰਾਮ! ਕੁੰਭ ਮੇਲਾ ਨਾਸਿਕ!',
      'ur': '🙏 جے شری رام! کمبھ میلہ ناشک!',
    };
    return greetings[langCode] ?? greetings['en']!;
  }
}
