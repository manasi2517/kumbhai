import 'dart:convert';
import 'package:flutter/services.dart';

class OfflineKumbhService {
  static Map<String, dynamic>? _knowledge;

  static final _topicKeywords = <String, List<String>>{
    'ghats':         ['ghat','घाट','ramkund','रामकुंड','bathing','snan','स्नान'],
    'emergency':     ['emergency','help','police','ambulance','आपातकाल','मदत','108','100','hospital'],
    'transport':     ['transport','bus','train','reach','travel','कैसे','कसे','taxi','railway'],
    'accommodation': ['hotel','stay','dharamshala','accommodation','रहना','राहणे','camp','tent'],
    'food':          ['food','eat','khana','langar','भोजन','जेवण','misal','dhaba'],
    'rituals':       ['ritual','darshan','temple','mandir','मंदिर','pooja','trimbak','kalaram'],
  };

  static Future<void> init() async {
    final str = await rootBundle.loadString('assets/data/kumbh_knowledge.json');
    _knowledge = json.decode(str);
  }

  static String getResponse(String query, String langCode) {
    final q = query.toLowerCase();
    String topic = 'general';
    for (final entry in _topicKeywords.entries) {
      if (entry.value.any((kw) => q.contains(kw))) {
        topic = entry.key;
        break;
      }
    }
    if (topic == 'general') {
      const general = {
        'en': '🙏 Ask me about: Ghats | Transport | Food | Emergency | Rituals | Stay',
        'hi': '🙏 पूछें: घाट | परिवहन | भोजन | आपातकाल | अनुष्ठान | आवास',
        'mr': '🙏 विचारा: घाट | वाहतूक | जेवण | आणीबाणी | विधी | राहणे',
      };
      return general[langCode] ?? general['en']!;
    }
    final topicData = _knowledge?[topic] as Map<String, dynamic>?;
    return topicData?[langCode] ?? topicData?['en'] ?? 'Information not available.';
  }
}
