import json
import os
import time

STORAGE_FILE = "app_data.json"

def load_data():
    try:
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
    except:
        pass
    return {
        "competitor_channels": [],
        "hook_database": [],
        "trend_history": [],
        "viral_alerts": [],
        "predictions": []
    }

def save_data(data):
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Storage error: {e}")
        return False

def get_competitor_channels():
    return load_data().get("competitor_channels", [])

def add_competitor_channel(channel):
    data = load_data()
    channels = data.get("competitor_channels", [])
    if not any(c["id"] == channel["id"] for c in channels):
        channels.append(channel)
        data["competitor_channels"] = channels
        save_data(data)
    return channels

def remove_competitor_channel(channel_id):
    data = load_data()
    channels = [c for c in data.get("competitor_channels", []) if c["id"] != channel_id]
    data["competitor_channels"] = channels
    save_data(data)
    return channels

def save_hook(hook):
    data = load_data()
    hooks = data.get("hook_database", [])
    hooks.append({**hook, "saved_at": time.time()})
    data["hook_database"] = hooks[-200:]
    save_data(data)

def get_hooks(niche=None):
    hooks = load_data().get("hook_database", [])
    if niche:
        hooks = [h for h in hooks if niche.lower() in h.get("niche", "").lower()]
    return sorted(hooks, key=lambda x: x.get("score", 0), reverse=True)

def save_trend_history(trend):
    data = load_data()
    history = data.get("trend_history", [])
    history.append({**trend, "recorded_at": time.time()})
    data["trend_history"] = history[-500:]
    save_data(data)

def get_trend_history():
    return load_data().get("trend_history", [])

def save_viral_alert(alert):
    data = load_data()
    alerts = data.get("viral_alerts", [])
    alerts.append({**alert, "detected_at": time.time()})
    data["viral_alerts"] = alerts[-100:]
    save_data(data)

def get_viral_alerts():
    return load_data().get("viral_alerts", [])