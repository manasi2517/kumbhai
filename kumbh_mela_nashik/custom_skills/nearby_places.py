#!/usr/bin/env python3
"""
Skill: Kumbh Mela Nashik — GPS-Based Nearby Places Finder
Finds nearest ghats, hospitals, food, accommodation, police, transport
Usage: python nearby_places.py --lat 20.0059 --lon 73.7898 --category all --radius 2.0
"""
import math, json, argparse

LOCATIONS = {"ghats": [{"name": "Ramkund Ghat", "lat": 20.0059, "lon": 73.7898, "info": "Most sacred ghat — where Lord Ram bathed. Main Kumbh bathing point."}, {"name": "Sita Gufa Ghat", "lat": 20.0061, "lon": 73.7885, "info": "Cave where Sita stayed during exile. Very peaceful ghat."}, {"name": "Panchvati Ghat", "lat": 20.0065, "lon": 73.788, "info": "5 sacred peepal trees site. Ram-Sita-Lakshman exile location."}, {"name": "Holkar Bridge Ghat", "lat": 20.0045, "lon": 73.791, "info": "Wide ghat near Holkar Bridge. Good for families."}, {"name": "Tapkeshwar Ghat", "lat": 20.007, "lon": 73.787, "info": "Shiva temple ghat. Dripping Shivlinga inside cave."}, {"name": "Makhmalabad Ghat", "lat": 20.003, "lon": 73.795, "info": "Quieter ghat. Good for early morning dip."}], "hospitals": [{"name": "District Civil Hospital", "lat": 20.012, "lon": 73.789, "info": "Main govt hospital. 24x7 emergency. Ph: 0253-2453011"}, {"name": "Nashik Road Hospital", "lat": 19.995, "lon": 73.82, "info": "Near railway station. Good for emergencies."}, {"name": "Kumbh Medical Camp (Ramkund)", "lat": 20.0058, "lon": 73.79, "info": "Free camp during Kumbh. Basic first aid, ORS available."}, {"name": "Kumbh Medical Camp (Panchvati)", "lat": 20.0064, "lon": 73.7882, "info": "Free camp during Kumbh. Doctor on duty 6am-10pm."}], "accommodation": [{"name": "Ram Mandir Dharamshala", "lat": 20.0057, "lon": 73.7895, "info": "Free/₹100 per night. Near Ramkund. Book early."}, {"name": "Panchvati Lodge", "lat": 20.0062, "lon": 73.7878, "info": "₹200-500/night. Clean rooms. Near ghats."}, {"name": "MTDC Resort Nashik", "lat": 20.015, "lon": 73.78, "info": "Premium govt resort. ₹2000+/night. Book via MTDC website."}, {"name": "Govt Tent City (Kumbh)", "lat": 20.004, "lon": 73.792, "info": "Setup during Kumbh. ₹300-800/night. Book via Maharashtra Tourism."}, {"name": "Hotel Panchavati Yatri", "lat": 20.0068, "lon": 73.7875, "info": "₹800-2000/night. AC rooms. Near Panchvati."}], "food": [{"name": "Langar (Ramkund Akhara)", "lat": 20.0055, "lon": 73.7902, "info": "FREE meals by akhara. Breakfast 7-10am, Lunch 12-3pm, Dinner 7-9pm."}, {"name": "Misal Pav Corner", "lat": 20.006, "lon": 73.7888, "info": "Famous Nashik Misal Pav. ₹50-80. Must try!"}, {"name": "Gurudwara Langar", "lat": 20.0075, "lon": 73.7865, "info": "FREE Sikh community meals. All welcome. 24 hours."}, {"name": "Panchvati Dhaba Row", "lat": 20.0063, "lon": 73.7879, "info": "Multiple dhabas. ₹60-200/meal. Veg Maharashtrian food."}], "police": [{"name": "Ramkund Police Chowky", "lat": 20.0056, "lon": 73.7896, "info": "24x7 during Kumbh. Lost & found. Emergency: 100"}, {"name": "Panchvati Police Post", "lat": 20.0066, "lon": 73.7877, "info": "Kumbh special post. Women's helpline: 1091"}, {"name": "Kumbh Control Room", "lat": 20.005, "lon": 73.7905, "info": "Central coordination. Missing persons, emergencies."}], "transport": [{"name": "Nashik Road Railway Station", "lat": 19.996, "lon": 73.819, "info": "8km from Ramkund. Trains to Mumbai/Pune/Delhi. Shuttle buses every 15 mins."}, {"name": "CBS Bus Stand", "lat": 20.01, "lon": 73.783, "info": "Central Bus Stand. MSRTC to all Maharashtra cities."}, {"name": "Kumbh Shuttle Stop (Ramkund)", "lat": 20.0053, "lon": 73.7907, "info": "Free/cheap shuttles during Kumbh. Every 15 mins to railway station."}]}

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def find_nearby(user_lat, user_lon, category="all", radius_km=2.0, top_n=3):
    results = {}
    cats = list(LOCATIONS.keys()) if category == "all" else [category]
    for cat in cats:
        if cat not in LOCATIONS: continue
        items = []
        for place in LOCATIONS[cat]:
            dist = haversine_km(user_lat, user_lon, place["lat"], place["lon"])
            if dist <= radius_km:
                items.append({**place, "distance_km": round(dist, 2)})
        items.sort(key=lambda x: x["distance_km"])
        if items: results[cat] = items[:top_n]
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--category", default="all", choices=["all","ghats","hospitals","accommodation","food","police","transport"])
    parser.add_argument("--radius", type=float, default=2.0)
    args = parser.parse_args()
    result = find_nearby(args.lat, args.lon, args.category, args.radius)
    print(json.dumps(result, ensure_ascii=False, indent=2))
