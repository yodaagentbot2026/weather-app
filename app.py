#!/usr/bin/env python3
"""Minimal weather CLI backed by Open-Meteo (no API key required)."""
import argparse
import sys

import requests


def geocode(place):
    r = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                     params={"name": place, "count": 1}, timeout=15)
    r.raise_for_status()
    results = r.json().get("results") or []
    if not results:
        print("Place not found:", place, file=sys.stderr)
        sys.exit(1)
    return results[0]


def forecast(lat, lon):
    r = requests.get("https://api.open-meteo.com/v1/forecast",
                     params={"latitude": lat, "longitude": lon,
                             "current": "temperature_2m,wind_speed_10m,weather_code"},
                     timeout=15)
    r.raise_for_status()
    return r.json()["current"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("place", help="City name, e.g. 'Menlo Park'")
    args = p.parse_args()
    loc = geocode(args.place)
    cur = forecast(loc["latitude"], loc["longitude"])
    print("%s, %s: %.1f C, wind %.1f km/h, code %s" % (
        loc["name"], loc.get("country", ""), cur["temperature_2m"],
        cur["wind_speed_10m"], cur["weather_code"]))


if __name__ == "__main__":
    main()
