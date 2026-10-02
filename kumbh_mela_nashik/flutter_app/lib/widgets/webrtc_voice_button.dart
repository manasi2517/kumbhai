import 'dart:async';
import 'package:flutter/material.dart';
import '../services/webrtc_voice_service.dart';
import '../services/language_detector_service.dart';
import '../services/offline_kumbh_service.dart';
import '../services/camber_agent_service.dart';
import 'package:connectivity_plus/connectivity_plus.dart';

typedef OnTranscript = void Function(String text, String lang);
typedef OnResponse   = void Function(String response);

/// Drop-in WebRTC voice button widget for any screen
class WebRTCVoiceButton extends StatefulWidget {
  final OnTranscript? onTranscript;
  final OnResponse?   onResponse;
  final double size;

  const WebRTCVoiceButton({
    super.key,
    this.onTranscript,
    this.onResponse,
    this.size = 60,
  });

  @override
  State<WebRTCVoiceButton> createState() => _WebRTCVoiceButtonState();
}

class _WebRTCVoiceButtonState extends State<WebRTCVoiceButton>
    with TickerProviderStateMixin {
  bool _recording = false;
  bool _processing = false;
  String _status = 'Tap to speak';
  late AnimationController _pulseCtrl;
  late Animation<double> _pulseAnim;

  @override
  void initState() {
    super.initState();
    _pulseCtrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 900))
      ..repeat(reverse: true);
    _pulseAnim = Tween<double>(begin: 1.0, end: 1.18).animate(
      CurvedAnimation(parent: _pulseCtrl, curve: Curves.easeInOut));
    WebRTCVoiceService.init();
  }

  @override
  void dispose() {
    _pulseCtrl.dispose();
    super.dispose();
  }

  Future<void> _toggle() async {
    if (_processing) return;
    if (!_recording) {
      // ── START ──────────────────────────────────────────
      final ok = await WebRTCVoiceService.startRecording();
      if (!ok) {
        setState(() => _status = '❌ Mic permission denied');
        return;
      }
      setState(() { _recording = true; _status = '🎙️ Bola... (Hindi/Marathi/English)'; });
    } else {
      // ── STOP + PROCESS ─────────────────────────────────
      setState(() { _recording = false; _processing = true; _status = '⏳ Processing...'; });
      final filePath = await WebRTCVoiceService.stopRecording();
      if (filePath == null) {
        setState(() { _processing = false; _status = 'Tap to speak'; });
        return;
      }

      // Try online STT first → fallback to offline knowledge match
      String? transcript;
      final conn = await Connectivity().checkConnectivity();
      if (conn != ConnectivityResult.none) {
        transcript = await WebRTCVoiceService.transcribeOnline(filePath, 'hi');
      }
      transcript ??= await WebRTCVoiceService.transcribeOffline(filePath, 'hi');

      if (transcript == null || transcript.isEmpty) {
        setState(() { _processing = false; _status = '❌ Audio samajla nahi, parat bola'; });
        return;
      }

      // Detect language + get response
      final lang = LanguageDetectorService.detect(transcript);
      widget.onTranscript?.call(transcript, lang);
      setState(() => _status = '🤖 Thinking...');

      String response;
      if (conn != ConnectivityResult.none) {
        response = await CamberAgentService.chat(transcript) ??
                   OfflineKumbhService.getResponse(transcript, lang);
      } else {
        response = OfflineKumbhService.getResponse(transcript, lang);
      }

      widget.onResponse?.call(response);
      setState(() { _processing = false; _status = 'Tap to speak'; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        GestureDetector(
          onTap: _toggle,
          child: AnimatedBuilder(
            animation: _pulseAnim,
            builder: (ctx, child) => Transform.scale(
              scale: _recording ? _pulseAnim.value : 1.0,
              child: child,
            ),
            child: Container(
              width: widget.size,
              height: widget.size,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  colors: _processing
                      ? [Colors.grey, Colors.grey.shade600]
                      : _recording
                          ? [Colors.red, Colors.redAccent]
                          : [const Color(0xFFFF6B35), Colors.amber],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                boxShadow: [
                  BoxShadow(
                    color: (_recording ? Colors.red : Colors.orange).withOpacity(0.5),
                    blurRadius: _recording ? 20 : 10,
                    spreadRadius: _recording ? 4 : 0,
                  )
                ],
              ),
              child: Icon(
                _processing ? Icons.hourglass_top :
                _recording  ? Icons.stop_rounded  : Icons.mic,
                color: Colors.white,
                size: widget.size * 0.4,
              ),
            ),
          ),
        ),
        const SizedBox(height: 6),
        Text(_status, style: const TextStyle(color: Colors.white70, fontSize: 11)),
      ],
    );
  }
}
