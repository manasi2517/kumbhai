import 'dart:math';

class Place {
  final String name, category, info, icon;
  final double lat, lon;
  double distanceKm;
  Place({required this.name, required this.category, required this.info,
         required this.icon, required this.lat, required this.lon, this.distanceKm = 0});
}

class NearbyPlacesService {
  static final _locations = <Place>[
    // Ghats
    Place(name:'Ramkund Ghat',         category:'ghats',         icon:'🏊', lat:20.0059, lon:73.7898, info:'Most sacred — Lord Ram bathed here'),
    Place(name:'Sita Gufa Ghat',       category:'ghats',         icon:'🕌', lat:20.0061, lon:73.7885, info:'Cave where Sita stayed during exile'),
    Place(name:'Panchvati Ghat',       category:'ghats',         icon:'🌳', lat:20.0065, lon:73.7880, info:'5 sacred peepal trees'),
    Place(name:'Holkar Bridge Ghat',   category:'ghats',         icon:'🏊', lat:20.0045, lon:73.7910, info:'Wide ghat, good for families'),
    Place(name:'Tapkeshwar Ghat',      category:'ghats',         icon:'🕍', lat:20.0070, lon:73.7870, info:'Shiva cave temple'),
    // Hospitals
    Place(name:'District Civil Hospital',         category:'hospitals', icon:'🏥', lat:20.0120, lon:73.7890, info:'24x7 Emergency — 0253-2453011'),
    Place(name:'Kumbh Medical Camp (Ramkund)',    category:'hospitals', icon:'⛺', lat:20.0058, lon:73.7900, info:'FREE camp — ORS, first aid'),
    Place(name:'Kumbh Medical Camp (Panchvati)',  category:'hospitals', icon:'⛺', lat:20.0064, lon:73.7882, info:'FREE — Doctor 6am-10pm'),
    // Food
    Place(name:'Langar (Ramkund Akhara)',  category:'food', icon:'🍱', lat:20.0055, lon:73.7902, info:'FREE meals all day'),
    Place(name:'Misal Pav Corner',         category:'food', icon:'🌶️', lat:20.0060, lon:73.7888, info:'Famous Nashik Misal ₹50-80'),
    Place(name:'Gurudwara Langar',         category:'food', icon:'🙏', lat:20.0075, lon:73.7865, info:'FREE Sikh langar 24 hours'),
    // Accommodation
    Place(name:'Ram Mandir Dharamshala',   category:'accommodation', icon:'🏠', lat:20.0057, lon:73.7895, info:'Free/₹100 per night'),
    Place(name:'Panchvati Lodge',          category:'accommodation', icon:'🏨', lat:20.0062, lon:73.7878, info:'₹200-500/night'),
    Place(name:'MTDC Resort',              category:'accommodation', icon:'🏩', lat:20.0150, lon:73.7800, info:'Premium ₹2000+/night'),
    // Police
    Place(name:'Ramkund Police Chowky',    category:'police', icon:'👮', lat:20.0056, lon:73.7896, info:'24x7 — Emergency: 100'),
    Place(name:'Kumbh Control Room',       category:'police', icon:'🎯', lat:20.0050, lon:73.7905, info:'Missing persons coordination'),
    // Transport
    Place(name:'Nashik Road Railway Station', category:'transport', icon:'🚂', lat:19.9960, lon:73.8190, info:'8km — Shuttle every 15 mins'),
    Place(name:'CBS Bus Stand',               category:'transport', icon:'🚌', lat:20.0100, lon:73.7830, info:'MSRTC all Maharashtra'),
    Place(name:'Kumbh Shuttle Stop',          category:'transport', icon:'🚐', lat:20.0053, lon:73.7907, info:'Free shuttle to railway station'),
  ];

  static double _haversine(double lat1, double lon1, double lat2, double lon2) {
    const R = 6371.0;
    final dLat = (lat2 - lat1) * pi / 180;
    final dLon = (lon2 - lon1) * pi / 180;
    final a = sin(dLat/2)*sin(dLat/2) +
              cos(lat1*pi/180)*cos(lat2*pi/180)*sin(dLon/2)*sin(dLon/2);
    return R * 2 * asin(sqrt(a));
  }

  static List<Place> findNearby(double lat, double lon,
      {String category = 'all', double radiusKm = 2.0, int topN = 3}) {
    final results = _locations
        .where((p) => category == 'all' || p.category == category)
        .map((p) => Place(
              name: p.name, category: p.category, info: p.info,
              icon: p.icon, lat: p.lat, lon: p.lon,
              distanceKm: double.parse(
                  _haversine(lat, lon, p.lat, p.lon).toStringAsFixed(2)),
            ))
        .where((p) => p.distanceKm <= radiusKm)
        .toList()
      ..sort((a, b) => a.distanceKm.compareTo(b.distanceKm));
    return results.take(topN).toList();
  }
}
