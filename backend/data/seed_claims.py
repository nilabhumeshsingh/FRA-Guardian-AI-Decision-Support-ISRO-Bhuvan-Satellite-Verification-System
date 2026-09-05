import random
import json
from datetime import date, timedelta

# Realistic Chhattisgarh forest district data
DISTRICTS = {
    "Bastar": {"lat": 19.12, "lon": 81.95},
    "Dantewada": {"lat": 18.89, "lon": 81.35},
    "Narayanpur": {"lat": 19.69, "lon": 80.47},
    "Kondagaon": {"lat": 19.59, "lon": 81.66},
    "Bijapur": {"lat": 18.84, "lon": 80.80},
}

OFFICERS = [
    # (id, name, district, bias_profile)
    ("OFF001", "Ramesh Kumar Verma", "Bastar", "fair"),
    ("OFF002", "Suresh Patel", "Bastar", "biased"),       # High rejector
    ("OFF003", "Anita Sharma", "Dantewada", "fair"),
    ("OFF004", "Mukesh Yadav", "Dantewada", "biased"),    # High rejector
    ("OFF005", "Priya Nair", "Narayanpur", "fair"),
    ("OFF006", "Dinesh Gupta", "Narayanpur", "neutral"),
    ("OFF007", "Kavita Singh", "Kondagaon", "fair"),
    ("OFF008", "Rajesh Tiwari", "Kondagaon", "biased"),   # High rejector
    ("OFF009", "Sunita Dewangan", "Bijapur", "fair"),
    ("OFF010", "Arvind Kashyap", "Bijapur", "neutral"),
]

CLAIMANT_NAMES = [
    "Bhima Korram", "Sukki Bai Mandavi", "Raju Netam", "Phulo Bai Sori",
    "Gondi Ram Potai", "Savitri Markam", "Budhu Kawde", "Champa Bai Usendi",
    "Manga Ram Dhurwa", "Janki Bai Oyam", "Sonu Poyam", "Radha Bai Baghel",
    "Laxman Thakur", "Meena Bai Porte", "Birsa Kunjam", "Sarita Sahu",
    "Deva Nag", "Phulmati Bai Gota", "Sukh Ram Teta", "Kamla Bai Dhruw",
    "Manglu Kanhar", "Antu Bai Mandavi", "Ramu Netam", "Basanti Bai Darro",
    "Sukdev Poyam", "Lalita Bai Punem", "Hira Lal Potai", "Bhagmati Sori",
    "Tikam Das Markam", "Rukmani Bai Kawde", "Bhagat Ram Usendi", "Devki Dhurwa",
    "Motiram Oyam", "Padmini Bai Baghel", "Dilip Kunjam", "Sundar Bai Nag",
    "Ratan Teta", "Jamuna Bai Dhruw", "Budh Ram Kanhar", "Chanda Bai Darro",
    "Lalu Poyam", "Pushpa Bai Punem", "Sohan Potai", "Leela Bai Sori",
    "Bahadur Markam", "Droupadi Kawde", "Keval Ram Usendi", "Bhajan Bai Dhurwa",
    "Madan Oyam", "Ganga Bai Baghel"
]

VILLAGES = {
    "Bastar": ["Tokapal", "Lohandiguda", "Kutru", "Bade Bacheli", "Darbha"],
    "Dantewada": ["Katekalyan", "Geedam", "Barsur", "Aranpur", "Kuakonda"],
    "Narayanpur": ["Orchha", "Kohkameta", "Ranibolly", "Benur", "Chhote Bethia"],
    "Kondagaon": ["Farasgaon", "Makdi", "Keshkal", "Nagri", "Bade Rajpur"],
    "Bijapur": ["Usur", "Bhairamgarh", "Bhopalpatnam", "Gangalur", "Pamed"],
}

REQUIRED_DOCS = [
    "Village Sabha Resolution", "Land Survey Map", "Aadhaar Card",
    "Traditional Use Evidence", "Community Witness Affidavit"
]

LAND_USES = ["Agricultural", "Habitation", "Community Forest Resource", "Grazing Land"]
SAT_LAND_USES = ["Dense Forest", "Open Forest", "Scrubland", "Agricultural", "Degraded Forest"]


def make_geojson(lat, lon, area_ha):
    """Generate a realistic polygon near given coordinates"""
    offset = (area_ha ** 0.5) * 0.003
    return json.dumps({
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [lon - offset, lat - offset],
                [lon + offset, lat - offset],
                [lon + offset, lat + offset],
                [lon - offset, lat + offset],
                [lon - offset, lat - offset],
            ]]
        },
        "properties": {}
    })


def generate_claims():
    claims = []
    random.seed(42)
    today = date.today()

    for i, name in enumerate(CLAIMANT_NAMES):
        district = list(DISTRICTS.keys())[i % 5]
        center = DISTRICTS[district]

        # Pick officer for this district
        district_officers = [o for o in OFFICERS if o[2] == district]
        officer = random.choice(district_officers)
        off_id, off_name, _, bias = officer

        area_ha = round(random.uniform(0.5, 8.0), 2)
        lat = center["lat"] + random.uniform(-0.15, 0.15)
        lon = center["lon"] + random.uniform(-0.15, 0.15)

        # Filing date: 30–900 days ago
        days_ago_filed = random.randint(30, 900)
        filed = today - timedelta(days=days_ago_filed)

        # Status logic based on bias
        if bias == "biased":
            status_weights = ["Rejected"] * 7 + ["Approved"] * 2 + ["Pending"]
        elif bias == "neutral":
            status_weights = ["Rejected"] * 4 + ["Approved"] * 4 + ["Pending"] * 2
        else:
            status_weights = ["Rejected"] * 2 + ["Approved"] * 6 + ["Pending"] * 2

        status = random.choice(status_weights)

        if status == "Pending":
            decision_date = None
            days_pending = days_ago_filed
        else:
            days_to_decision = random.randint(15, min(days_ago_filed, 365))
            decision_date = (filed + timedelta(days=days_to_decision)).isoformat()
            days_pending = 0

        # Documents: biased officers tend to claim missing docs
        if bias == "biased":
            num_docs = random.randint(1, 4)
        else:
            num_docs = random.randint(3, 5)
        docs = random.sample(REQUIRED_DOCS, num_docs)

        # Satellite match
        if status == "Approved":
            sat_match = round(random.uniform(65, 98), 1)
        elif status == "Rejected":
            sat_match = round(random.uniform(20, 75), 1)
        else:
            sat_match = round(random.uniform(40, 90), 1)

        land_use = random.choice(LAND_USES)
        sat_use = random.choice(SAT_LAND_USES)

        # Anomaly flags
        flags = []
        if status == "Pending" and days_pending > 180:
            flags.append("TIME_TRAP")
        if num_docs < 3:
            flags.append("MISSING_DOCS")
        if sat_match < 60:
            flags.append("SAT_MISMATCH")

        # Health score (rough pre-calc)
        doc_score = (num_docs / 5) * 100
        bias_score = 100 if bias == "fair" else (60 if bias == "neutral" else 20)
        time_score = max(0, 100 - (days_pending / 365 * 100)) if status == "Pending" else 90
        health = round(
            doc_score * 0.25 + bias_score * 0.30 + sat_match * 0.25 + time_score * 0.20, 1
        )

        village = random.choice(VILLAGES[district])

        # ── NDVI Timeline (5-year satellite vegetation history) ──
        ndvi_timeline = []
        for yr in range(2019, 2025):
            if land_use in ("Agricultural", "Grazing Land"):
                # Crops: seasonal pattern — NDVI rises in monsoon, drops after harvest
                monsoon_ndvi = round(random.uniform(0.42, 0.62), 2)   # Jul-Oct peak
                winter_ndvi  = round(random.uniform(0.18, 0.32), 2)   # Nov-Feb low
                avg_ndvi     = round((monsoon_ndvi + winter_ndvi) / 2, 2)
                variance     = round(monsoon_ndvi - winter_ndvi, 2)
                classification = "Cultivated"
            elif sat_use in ("Dense Forest", "Open Forest"):
                # Forest: steady high NDVI year-round
                monsoon_ndvi = round(random.uniform(0.68, 0.85), 2)
                winter_ndvi  = round(random.uniform(0.62, 0.78), 2)
                avg_ndvi     = round((monsoon_ndvi + winter_ndvi) / 2, 2)
                variance     = round(monsoon_ndvi - winter_ndvi, 2)
                classification = "Forest"
            else:
                # Scrubland / degraded
                monsoon_ndvi = round(random.uniform(0.20, 0.38), 2)
                winter_ndvi  = round(random.uniform(0.10, 0.22), 2)
                avg_ndvi     = round((monsoon_ndvi + winter_ndvi) / 2, 2)
                variance     = round(monsoon_ndvi - winter_ndvi, 2)
                classification = "Scrubland"

            ndvi_timeline.append({
                "year": yr,
                "avg_ndvi": avg_ndvi,
                "monsoon_ndvi": monsoon_ndvi,
                "winter_ndvi": winter_ndvi,
                "seasonal_variance": variance,
                "classification": classification,
            })

        # Determine satellite verdict
        dominant = max(set(e["classification"] for e in ndvi_timeline),
                       key=lambda c: sum(1 for e in ndvi_timeline if e["classification"] == c))
        claim_matches = (
            (land_use in ("Agricultural", "Grazing Land") and dominant == "Cultivated") or
            (land_use == "Community Forest Resource" and dominant == "Forest") or
            (land_use == "Habitation" and dominant in ("Scrubland", "Cultivated"))
        )
        if claim_matches:
            sat_verdict = "AGREES"
            sat_confidence = round(random.uniform(72, 96), 1)
        elif dominant == "Forest" and land_use in ("Agricultural", "Grazing Land"):
            sat_verdict = "CONTRADICTS"
            sat_confidence = round(random.uniform(78, 98), 1)
        else:
            sat_verdict = "PARTIAL"
            sat_confidence = round(random.uniform(45, 70), 1)

        claims.append({
            "claimant_name": name,
            "village": village,
            "district": district,
            "state": "Chhattisgarh",
            "officer_id": off_id,
            "officer_name": off_name,
            "status": status,
            "filed_date": filed.isoformat(),
            "decision_date": decision_date,
            "area_ha": area_ha,
            "geojson": make_geojson(lat, lon, area_ha),
            "documents_submitted": docs,
            "health_score": health,
            "anomaly_flags": flags,
            "satellite_match_pct": sat_match,
            "land_use_claimed": land_use,
            "satellite_land_use": sat_use,
            "ndvi_timeline": ndvi_timeline,
            "satellite_verdict": sat_verdict,
            "satellite_confidence": sat_confidence,
        })

    # Ensure officer bias flags for biased officers
    # Add BIAS flag post-generation based on district averages
    district_rejection_rates = {}
    for d in DISTRICTS:
        d_claims = [c for c in claims if c["district"] == d]
        if d_claims:
            rej = sum(1 for c in d_claims if c["status"] == "Rejected")
            district_rejection_rates[d] = rej / len(d_claims)

    officer_rejection_rates = {}
    for off in OFFICERS:
        o_claims = [c for c in claims if c["officer_id"] == off[0]]
        if o_claims:
            rej = sum(1 for c in o_claims if c["status"] == "Rejected")
            officer_rejection_rates[off[0]] = rej / len(o_claims)

    for c in claims:
        dist_avg = district_rejection_rates.get(c["district"], 0)
        off_rate = officer_rejection_rates.get(c["officer_id"], 0)
        if off_rate > dist_avg + 0.2 and "BIAS" not in c["anomaly_flags"]:
            c["anomaly_flags"].append("BIAS")

    return claims


SEED_CLAIMS = generate_claims()
