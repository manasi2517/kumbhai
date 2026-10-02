import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:geolocator/geolocator.dart';
import 'package:url_launcher/url_launcher.dart';
import '../services/nearby_places_service.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});
  @override State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final _mapCtrl = MapController();
  LatLng? _userLoc;
  String _filter = 'all';
  List<Place> _nearbyList = [];

  static const _center = LatLng(20.0059, 73.7898);
  static const _catColors = {
    'ghats':'🏊','hospitals':'🏥','food':'🍱',
    'accommodation':'🏠','police':'👮','transport':'🚌',
  };

  Future<void> _locateMe() async {
    try {
      final pos = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
      final loc = LatLng(pos.latitude, pos.longitude);
      setState(() { _userLoc = loc; });
      _mapCtrl.move(loc, 16);
      _updateNearby(pos.latitude, pos.longitude);
    } catch (_) {
      _mapCtrl.move(_center, 16);
    }
  }

  void _updateNearby(double lat, double lon) {
    setState(() {
      _nearbyList = NearbyPlacesService.findNearby(lat, lon, category: _filter, topN: 5);
    });
  }

  void _navigate(Place p) async {
    final uri = Uri.parse('https://www.google.com/maps/dir/?api=1&destination=${p.lat},${p.lon}');
    if (await canLaunchUrl(uri)) launchUrl(uri, mode: LaunchMode.externalApplication);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0d1117),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1a0a00),
        title: const Text('🗺️ कुंभ मेळा नाशिक — Live Map', style: TextStyle(color: Colors.amber, fontSize: 15, fontWeight: FontWeight.bold)),
        actions: [
          IconButton(icon: const Icon(Icons.my_location, color: Colors.orange), onPressed: _locateMe, tooltip: 'माझं Location'),
        ],
      ),
      body: Column(children: [
        // Filter bar
        SizedBox(
          height: 44,
          child: ListView(
            scrollDirection: Axis.horizontal, padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
            children: ['all',..._catColors.keys].map((cat) {
              final active = _filter == cat;
              return GestureDetector(
                onTap: () { setState(() => _filter = cat); if (_userLoc != null) _updateNearby(_userLoc!.latitude, _userLoc!.longitude); },
                child: Container(
                  margin: const EdgeInsets.only(right: 8),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
                  decoration: BoxDecoration(
                    color: active ? Colors.orange.withOpacity(0.2) : const Color(0xFF21262d),
                    border: Border.all(color: active ? Colors.orange : const Color(0xFF30363d)),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    cat == 'all' ? '🗺️ All' : '${_catColors[cat]} ${cat[0].toUpperCase()}${cat.substring(1)}',
                    style: TextStyle(color: active ? Colors.orange : Colors.white70, fontSize: 12),
                  ),
                ),
              );
            }).toList(),
          ),
        ),
        // Map
        Expanded(
          flex: 3,
          child: FlutterMap(
            mapController: _mapCtrl,
            options: const MapOptions(initialCenter: _center, initialZoom: 15),
            children: [
              TileLayer(urlTemplate: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', subdomains: const ['a','b','c']),
              MarkerLayer(markers: [
                if (_userLoc != null) Marker(
                  point: _userLoc!, width: 36, height: 36,
                  child: const Text('📍', style: TextStyle(fontSize: 28)),
                ),
                ...NearbyPlacesService.findNearby(
                  _userLoc?.latitude ?? _center.latitude,
                  _userLoc?.longitude ?? _center.longitude,
                  category: _filter, radiusKm: 5, topN: 20,
                ).map((p) => Marker(
                  point: LatLng(p.lat, p.lon), width: 36, height: 36,
                  child: GestureDetector(
                    onTap: () => showModalBottomSheet(context: context,
                      backgroundColor: const Color(0xFF21262d),
                      builder: (_) => ListTile(
                        leading: Text(p.icon, style: const TextStyle(fontSize: 28)),
                        title: Text(p.name, style: const TextStyle(color: Colors.amber)),
                        subtitle: Text(p.info, style: const TextStyle(color: Colors.white70)),
                        trailing: ElevatedButton(
                          style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                          onPressed: () { Navigator.pop(context); _navigate(p); },
                          child: const Text('Navigate'),
                        ),
                      )),
                    child: Text(p.icon, style: const TextStyle(fontSize: 24)),
                  ),
                )),
              ]),
            ],
          ),
        ),
        // Nearby list
        if (_nearbyList.isNotEmpty) Expanded(
          flex: 2,
          child: Column(children: [
            const Divider(color: Color(0xFF30363d), height: 1),
            Padding(padding: const EdgeInsets.all(8),
              child: Text('📍 Nearby Places (${_nearbyList.length})', style: const TextStyle(color: Colors.amber, fontWeight: FontWeight.bold))),
            Expanded(child: ListView.builder(
              itemCount: _nearbyList.length,
              itemBuilder: (ctx, i) {
                final p = _nearbyList[i];
                return ListTile(
                  leading: Text(p.icon, style: const TextStyle(fontSize: 22)),
                  title: Text(p.name, style: const TextStyle(color: Colors.white, fontSize: 13)),
                  subtitle: Text('${p.distanceKm} km — ${p.info}', style: const TextStyle(color: Colors.grey, fontSize: 11)),
                  trailing: IconButton(icon: const Icon(Icons.navigation, color: Colors.orange), onPressed: () => _navigate(p)),
                  dense: true,
                );
              },
            )),
          ]),
        ),
      ]),
    );
  }
}
