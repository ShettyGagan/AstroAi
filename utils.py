# utils.py
import requests
import streamlit as st
from timezonefinder import TimezoneFinder # Import this

@st.cache_data(show_spinner=False, ttl=86400)
def get_geolocation(place_name: str):
    #Gets latitude, longitude, and timezone_id for a given place name.
    try:
       
        url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json&limit=1"
        headers = {"User-Agent": "AstroGuideAI/1.0 (your-email@example.com)"}
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        location_data = response.json()
        
        if not location_data:
            return {"status": "error", "message": f"📍 Location not found: '{place_name}'"}
            
        loc = location_data[0]
        lat, lon = float(loc["lat"]), float(loc["lon"])

        #  TimezoneFinder to get the timezone
        tf = TimezoneFinder()
        tz_id = tf.timezone_at(lng=lon, lat=lat)
        
        if not tz_id:
            return {"status": "error", "message": " Could not determine timezone for this location."}

        return {
            "status": "success",
            "latitude": lat,
            "longitude": lon,
            "timezone_id": tz_id 
        }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Network error: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {e}"}