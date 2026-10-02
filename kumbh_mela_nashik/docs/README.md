# 🕉️ Kumbh Mela Nashik — AI Voice & Chat Assistant

## 📌 Agent Tag
`@manasi17.kumbh_mela_nashik`

## 🗂️ Project Structure
```
kumbh_mela_nashik/
├── agent/
│   ├── instruction.md          ← Paste this in Camber UI → Prompt field
│   └── agent_config.json       ← Agent metadata & skill registry
├── custom_skills/
│   ├── language_detector.py    ← Skill 1: 10-language auto-detect
│   ├── kumbh_info.py           ← Skill 2: Ghats, transport, emergency info
│   └── nearby_places.py        ← Skill 3: GPS-based nearby finder
├── offline_model/
│   └── kumbh_offline_assistant.py  ← 100% offline, no internet needed
├── map/
│   └── kumbh_live_map.html     ← Interactive live map with voice
├── outputs/                    ← Generated outputs
└── docs/
    └── README.md               ← This file
```

## 🚀 Quick Start

### Online Mode (Camber Agent)
```
@manasi17.kumbh_mela_nashik रामकुंड घाट कुठे आहे?
@manasi17.kumbh_mela_nashik emergency numbers
@manasi17.kumbh_mela_nashik नाशिकला कसे जायचे?
```

### Offline Mode (Python script)
```bash
python offline_model/kumbh_offline_assistant.py
```

### Skills Usage
```bash
python custom_skills/language_detector.py --text "नमस्ते"
python custom_skills/kumbh_info.py --query "emergency" --lang en
python custom_skills/nearby_places.py --lat 20.0059 --lon 73.7898 --category all
```

## ✅ Registered Skills
| Skill | File | Purpose |
|-------|------|---------|
| language-detector | language_detector.py | 10-language auto-detect |
| kumbh-info | kumbh_info.py | Complete Kumbh information |
| nearby-places | nearby_places.py | GPS-based nearby places |

## 🌐 Languages
Hindi · Marathi · English · Gujarati · Bengali · Tamil · Telugu · Kannada · Punjabi · Urdu

## 🗺️ Live Map
Open `map/kumbh_live_map.html` in browser — works offline with downloaded tiles.
