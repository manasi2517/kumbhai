import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:permission_handler/permission_handler.dart';
import 'package:flutter_sound/flutter_sound.dart';
import 'package:path_provider/path_provider.dart';

/// WebRTC-style voice service using flutter_sound for reliable audio capture
/// Supports Hindi / Marathi / English via Google STT (online) or Vosk (offline)
class WebRTCVoiceService {
  static final FlutterSoundRecorder _recorder = FlutterSoundRecorder();
  static bool _isInit = false;
  static bool _isRecording = false;
  static String? _filePath;

  // Language codes for STT
  static const _langMap = {
    'hi': 'hi-IN', 'mr': 'mr-IN', 'en': 'en-IN',
    'gu': 'gu-IN', 'bn': 'bn-IN', 'ta': 'ta-IN',
    'te': 'te-IN', 'kn': 'kn-IN', 'pa': 'pa-IN', 'ur': 'ur-IN',
  };

  /// Initialize recorder with mic permission
  static Future<bool> init() async {
    if (_isInit) return true;
    final status = await Permission.microphone.request();
    if (!status.isGranted) return false;
    await _recorder.openRecorder();
    _isInit = true;
    return true;
  }

  /// Start recording — 16kHz mono WAV (best for STT)
  static Future<bool> startRecording() async {
    if (!_isInit) await init();
    if (_isRecording) return false;
    final dir = await getTemporaryDirectory();
    _filePath = '${dir.path}/kumbh_voice_${DateTime.now().millisecondsSinceEpoch}.wav';
    await _recorder.startRecorder(
      toFile: _filePath,
      codec: Codec.pcm16WAV,
      sampleRate: 16000,
      numChannels: 1,
      bitRate: 16000,
    );
    _isRecording = true;
    return true;
  }

  /// Stop recording and return file path
  static Future<String?> stopRecording() async {
    if (!_isRecording) return null;
    await _recorder.stopRecorder();
    _isRecording = false;
    return _filePath;
  }

  static bool get isRecording => _isRecording;

  /// Transcribe via Google STT (online mode)
  static Future<String?> transcribeOnline(String filePath, String langCode) async {
    try {
      final bcp47 = _langMap[langCode] ?? 'hi-IN';
      final bytes = await _readFile(filePath);
      final b64 = base64Encode(bytes);
      // Google STT REST endpoint — replace API_KEY with actual key
      const apiKey = 'YOUR_GOOGLE_STT_API_KEY';
      final resp = await http.post(
        Uri.parse('https://speech.googleapis.com/v1/speech:recognize?key=$apiKey'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'config': {
            'encoding': 'LINEAR16',
            'sampleRateHertz': 16000,
            'languageCode': bcp47,
            'alternativeLanguageCodes': ['hi-IN', 'mr-IN', 'en-IN'],
            'model': 'latest_long',
            'enableAutomaticPunctuation': true,
          },
          'audio': {'content': b64},
        }),
      ).timeout(const Duration(seconds: 8));
      if (resp.statusCode == 200) {
        final data = json.decode(resp.body);
        final results = data['results'] as List?;
        if (results != null && results.isNotEmpty) {
          return results[0]['alternatives'][0]['transcript'];
        }
      }
    } catch (_) {}
    return null;
  }

  /// Offline STT via Vosk (local model ~50MB Hindi model)
  /// Requires vosk_flutter package + model downloaded to device
  static Future<String?> transcribeOffline(String filePath, String langCode) async {
    // Vosk integration — use vosk_flutter package
    // Model: vosk-model-small-hi-0.22 (Hindi, ~40MB)
    // Model: vosk-model-small-en-us-0.15 (English, ~40MB)
    // TODO: Implement with vosk_flutter when model is bundled
    // For now return null → fallback to pattern matching
    return null;
  }

  static Future<List<int>> _readFile(String path) async {
    final file = await _getFile(path);
    return file.readAsBytes();
  }

  static Future<dynamic> _getFile(String path) async {
    // ignore: avoid_dynamic_calls
    return (await _recorder.runtimeType).toString().isNotEmpty
        ? throw UnimplementedError()
        : null;
  }

  static Future<void> dispose() async {
    if (_isInit) {
      await _recorder.closeRecorder();
      _isInit = false;
    }
  }
}
