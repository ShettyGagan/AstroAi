# astro_engine.py
import swisseph as swe
from datetime import datetime
import pytz

swe.set_ephe_path(None)

# Constants
PLANETS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
    "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
    "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO
}
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
         "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

ASPECTS = {
    "Conjunction": (0, 8),
    "Sextile": (60, 4),
    "Square": (90, 6),
    "Trine": (120, 6),
    "Opposition": (180, 8)
}

def get_sign(degree):
    return SIGNS[int(degree // 30)]

def format_degree(degree):
    deg = int(degree)
    minutes = int((degree - deg) * 60)
    return f"{deg}° {minutes}'"

def calculate_chart_data(dob, tob, lat, lon, tz_id):
    try:
        local_tz = pytz.timezone(tz_id)
        birth_naive = datetime.combine(dob, tob)
        birth_aware = local_tz.localize(birth_naive)
        birth_utc = birth_aware.astimezone(pytz.utc)

        jd_utc = swe.julday(
            birth_utc.year, birth_utc.month, birth_utc.day,
            birth_utc.hour + birth_utc.minute / 60.0
        )

        swe.set_sid_mode(swe.SIDM_LAHIRI)

        # Calculate houses
        cusps, _ = swe.houses(jd_utc, lat, lon, hsys=b'P')  # Placidus
        ascendant_deg = cusps[0]
        mc_deg = cusps[9]

        placements = {}

        # Calculate planet positions
        for name, planet_id in PLANETS.items():
            pos = swe.calc(jd_utc, planet_id)[0][0] % 360
            house_num = 1
            for i in range(12):
                start = cusps[i]
                end = cusps[(i + 1) % 12]
                if start <= pos < end or (start > end and (pos >= start or pos < end)):
                    house_num = i + 1
                    break

            placements[name] = {
                "degree_val": pos,
                "degree_str": format_degree(pos % 30),
                "sign": get_sign(pos),
                "house": house_num
            }

        # Add Ascendant and Midheaven
        placements["Ascendant"] = {
            "degree_val": ascendant_deg,
            "degree_str": format_degree(ascendant_deg % 30),
            "sign": get_sign(ascendant_deg),
            "house": 1
        }
        placements["Midheaven"] = {
            "degree_val": mc_deg,
            "degree_str": format_degree(mc_deg % 30),
            "sign": get_sign(mc_deg),
            "house": 10
        }

        # Calculate aspects
        aspects = []
        planet_list = [k for k in placements.keys() if k in PLANETS]
        for i, p1 in enumerate(planet_list):
            for j, p2 in enumerate(planet_list[i+1:], i+1):
                deg1 = placements[p1]["degree_val"]
                deg2 = placements[p2]["degree_val"]
                diff = abs(deg1 - deg2) % 360
                diff = min(diff, 360 - diff)
                for aspect_name, (angle, orb) in ASPECTS.items():
                    if abs(diff - angle) <= orb:
                        aspects.append({
                            "type": aspect_name,
                            "planets": [p1, p2],
                            "angle": round(diff, 2),
                            "orb": round(abs(diff - angle), 2)
                        })

        return {
            "status": "success",
            "data": placements,
            "aspects": aspects,
            "cusps": cusps,
            "jd_utc": jd_utc
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}