import 'dart:convert';
import 'package:http/http.dart' as http;

class CamberAgentService {
  static const _agentTag = 'manasi17.kumbh_mela_nashik';
  // Replace with your Camber API base URL
  static const _baseUrl = 'https://api.cambercloud.com/v1';

  static Future<String?> chat(String message, {String? apiKey}) async {
    try {
      final resp = await http.post(
        Uri.parse('$_baseUrl/agents/$_agentTag/chat'),
        headers: {
          'Content-Type': 'application/json',
          if (apiKey != null) 'Authorization': 'Bearer $apiKey',
        },
        body: json.encode({'message': message}),
      ).timeout(const Duration(seconds: 10));

      if (resp.statusCode == 200) {
        final data = json.decode(utf8.decode(resp.bodyBytes));
        return data['response'] ?? data['message'] ?? data['content'];
      }
      return null;
    } catch (_) {
      return null; // fallback to offline
    }
  }
}
