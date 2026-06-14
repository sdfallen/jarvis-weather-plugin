"""
jarvis_plugin.py
Weather Plugin for JARVIS AI Assistant
Author: Ali Mehdi
Version: 1.0.0
"""

import requests

PLUGIN_INFO = {
    "name":        "JARVIS Weather Plugin",
    "version":     "1.0.0",
    "author":      "Ali Mehdi",
    "description": "Real-time weather for any city",
    "commands":    ["get_weather", "weather_forecast"],
}

# ── Register / Unregister ─────────────────────────────

def register():
    print("[Weather Plugin] Activated successfully!")

def unregister():
    print("[Weather Plugin] Deactivated.")

# ── Weather functions ─────────────────────────────────

def get_weather(city: str = "Istanbul") -> str:
    """
    Get current weather for any city.
    Uses wttr.in (no API key needed!)
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        resp = requests.get(url, timeout=8)

        if resp.status_code != 200:
            return _simple_weather(city)

        data    = resp.json()
        current = data["current_condition"][0]

        temp_c     = current["temp_C"]
        temp_f     = current["temp_F"]
        feels_c    = current["FeelsLikeC"]
        humidity   = current["humidity"]
        wind_kmph  = current["windspeedKmph"]
        wind_dir   = current["winddir16Point"]
        visibility = current["visibility"]
        pressure   = current["pressure"]
        desc       = current["weatherDesc"][0]["value"]
        uv_index   = current.get("uvIndex", "N/A")

        # Get location name
        area = data.get(
            "nearest_area", [{}])[0]
        city_name = area.get(
            "areaName", [{}])[0].get(
            "value", city)
        country = area.get(
            "country", [{}])[0].get(
            "value", "")

        return (
            f"🌍 Weather for {city_name}, {country}\n"
            f"─────────────────────────────\n"
            f"🌡️  Temperature : {temp_c}°C / {temp_f}°F\n"
            f"🤔 Feels Like  : {feels_c}°C\n"
            f"☁️  Condition   : {desc}\n"
            f"💧 Humidity    : {humidity}%\n"
            f"💨 Wind        : {wind_kmph} km/h {wind_dir}\n"
            f"👁️  Visibility  : {visibility} km\n"
            f"🔵 Pressure    : {pressure} hPa\n"
            f"☀️  UV Index    : {uv_index}\n"
        )

    except Exception as exc:
        return _simple_weather(city)


def weather_forecast(city: str = "Istanbul",
                     days: int = 3) -> str:
    """
    Get weather forecast for next days.
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        resp = requests.get(url, timeout=8)

        if resp.status_code != 200:
            return f"Could not get forecast for {city}"

        data = resp.json()
        weather_days = data.get(
            "weather", [])[:days]

        lines = [
            f"📅 {days}-Day Forecast for {city}\n"
            f"─────────────────────────────"
        ]

        day_names = [
            "Today", "Tomorrow",
            "Day After", "Day 4", "Day 5",
        ]

        for i, day in enumerate(weather_days):
            date      = day.get("date", "")
            max_c     = day.get("maxtempC", "?")
            min_c     = day.get("mintempC", "?")
            avg_c     = day.get("avgtempC", "?")
            sunrise   = day.get("astronomy",
                                [{}])[0].get(
                "sunrise", "?")
            sunset    = day.get("astronomy",
                                [{}])[0].get(
                "sunset", "?")

            # Get hourly descriptions
            hourly = day.get("hourly", [])
            descs  = []
            for h in hourly:
                d = h.get(
                    "weatherDesc",
                    [{}])[0].get("value", "")
                if d and d not in descs:
                    descs.append(d)

            day_label = (
                day_names[i]
                if i < len(day_names)
                else f"Day {i+1}"
            )
            condition = (
                ", ".join(descs[:2])
                if descs else "N/A"
            )

            lines.append(
                f"\n📆 {day_label} ({date})\n"
                f"   🌡️  {min_c}°C → {max_c}°C "
                f"(avg {avg_c}°C)\n"
                f"   ☁️  {condition}\n"
                f"   🌅 Sunrise: {sunrise}  "
                f"🌇 Sunset: {sunset}"
            )

        return "\n".join(lines)

    except Exception as exc:
        return f"Forecast error: {exc}"


def _simple_weather(city: str) -> str:
    """Simple fallback using wttr.in text format."""
    try:
        url = f"https://wttr.in/{city}?format=3"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return f"🌍 {resp.text.strip()}"
        return f"Could not get weather for: {city}"
    except Exception as exc:
        return f"Weather unavailable: {exc}"
