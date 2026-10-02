import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'services/offline_kumbh_service.dart';
import 'screens/chat_screen.dart';
import 'screens/map_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await OfflineKumbhService.init();
  runApp(const KumbhApp());
}

class KumbhApp extends StatelessWidget {
  const KumbhApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Kumbh Mela Nashik',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        textTheme: GoogleFonts.notoSansDevanagariTextTheme(ThemeData.dark().textTheme),
        colorScheme: const ColorScheme.dark(primary: Color(0xFFFF6B35), secondary: Colors.amber),
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _tab = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(index: _tab, children: const [ChatScreen(), MapScreen()]),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _tab,
        onTap: (i) => setState(() => _tab = i),
        backgroundColor: const Color(0xFF1a0a00),
        selectedItemColor: Colors.orange,
        unselectedItemColor: Colors.white38,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.chat_bubble_outline), activeIcon: Icon(Icons.chat_bubble), label: 'Assistant'),
          BottomNavigationBarItem(icon: Icon(Icons.map_outlined), activeIcon: Icon(Icons.map), label: 'Live Map'),
        ],
      ),
    );
  }
}
