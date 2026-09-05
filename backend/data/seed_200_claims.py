"""
seed_200_claims.py
Generates 200 realistic FRA claims near Madhya Pradesh forest boundaries
and upserts them into MongoDB Atlas and sample_fra_claims.json.
"""
import os
import json
import random
import math
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env from backend/.env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fra_guardian")

# Real MP Forest Reserves & Divisions with anchor coordinates & villages
MP_FOREST_ZONES = [
    {
        "district": "Mandla",
        "reserve": "Kanha Tiger Reserve Buffer",
        "division": "Mandla East Forest Division",
        "lat_range": (22.28, 22.45),
        "lng_range": (80.45, 80.85),
        "villages": ["Khatia", "Mocha", "Bamhni", "Chichrungpur", "Ghughri", "Bichhiya", "Mawai", "Nainpur"],
        "tribes": ["Gond", "Baiga (PVTG)"]
    },
    {
        "district": "Balaghat",
        "reserve": "Kanha-Pench Wildlife Corridor",
        "division": "Balaghat South Division",
        "lat_range": (21.85, 22.20),
        "lng_range": (80.20, 80.65),
        "villages": ["Baihar", "Birsa", "Garhi", "Ukwa", "Katangi", "Paraswada", "Lanji"],
        "tribes": ["Baiga (PVTG)", "Gond", "Halba"]
    },
    {
        "district": "Dindori",
        "reserve": "Achanakmar-Amarkantak Buffer Zone",
        "division": "Dindori Forest Division",
        "lat_range": (22.80, 23.05),
        "lng_range": (81.05, 81.65),
        "villages": ["Samnapur", "Bajag", "Karanjiya", "Mehandwani", "Shahpura", "Chada", "Gadasarani"],
        "tribes": ["Baiga (PVTG)", "Gond"]
    },
    {
        "district": "Seoni",
        "reserve": "Pench Tiger Reserve Buffer",
        "division": "Seoni Forest Division",
        "lat_range": (21.70, 22.05),
        "lng_range": (79.30, 79.70),
        "villages": ["Turia", "Kurai", "Barghat", "Karmajhiri", "Amanala", "Rukhad", "Chhapara"],
        "tribes": ["Gond", "Korku"]
    },
    {
        "district": "Chhindwara",
        "reserve": "Patalkot Valley & Pench Corridor",
        "division": "Chhindwara South Division",
        "lat_range": (22.15, 22.45),
        "lng_range": (78.50, 78.95),
        "villages": ["Tamia", "Harrai", "Bichhua", "Amarwara", "Patalkot", "Junnardeo", "Parasia"],
        "tribes": ["Bharia (PVTG)", "Gond"]
    },
    {
        "district": "Betul",
        "reserve": "Satpura-Melghat Wildlife Corridor",
        "division": "Betul South Division",
        "lat_range": (21.85, 22.15),
        "lng_range": (77.65, 78.10),
        "villages": ["Shahpur", "Chicholi", "Bhainsdehi", "Athner", "Ghoradongri", "Sarni"],
        "tribes": ["Korku", "Gond"]
    },
    {
        "district": "Umaria",
        "reserve": "Bandhavgarh Tiger Reserve Buffer",
        "division": "Umaria Forest Division",
        "lat_range": (23.55, 23.75),
        "lng_range": (80.90, 81.25),
        "villages": ["Tala", "Magdhi", "Khitauli", "Dhamokhar", "Manpur", "Pali", "Chandia"],
        "tribes": ["Gond", "Kol", "Baiga (PVTG)"]
    },
    {
        "district": "Shahdol",
        "reserve": "Son Chhatar & Sanjay Buffer",
        "division": "Shahdol Forest Division",
        "lat_range": (23.10, 23.40),
        "lng_range": (81.25, 81.65),
        "villages": ["Sohagpur", "Beohari", "Jaisinghnagar", "Burhar", "Gohparu"],
        "tribes": ["Kol", "Gond", "Baiga (PVTG)"]
    },
    {
        "district": "Anuppur",
        "reserve": "Amarkantak Sacred Groves & Buffer",
        "division": "Anuppur Forest Division",
        "lat_range": (22.65, 22.90),
        "lng_range": (81.60, 81.90),
        "villages": ["Pushprajgarh", "Jaithari", "Kotma", "Amarkantak", "Venkatnagar"],
        "tribes": ["Baiga (PVTG)", "Gond", "Kol"]
    },
    {
        "district": "Narmadapuram",
        "reserve": "Satpura Tiger Reserve & Bori Sanctuary",
        "division": "Hoshangabad Forest Division",
        "lat_range": (22.40, 22.65),
        "lng_range": (77.95, 78.40),
        "villages": ["Madhai", "Matkuli", "Kesla", "Sukhtawa", "Pachmarhi Buffer", "Pipariya Edge"],
        "tribes": ["Korku", "Gond"]
    },
    {
        "district": "Sheopur",
        "reserve": "Kuno National Park Buffer",
        "division": "Sheopur Forest Division",
        "lat_range": (25.45, 25.80),
        "lng_range": (77.10, 77.40),
        "villages": ["Palpur", "Sesaipura", "Karahal", "Ochhapura", "Morawan", "Agra"],
        "tribes": ["Sahariya (PVTG)"]
    },
    {
        "district": "Panna",
        "reserve": "Panna Tiger Reserve Corridor",
        "division": "Panna Forest Division",
        "lat_range": (24.60, 24.80),
        "lng_range": (80.05, 80.35),
        "villages": ["Madla", "Hinouta", "Amanganj", "Ajaigarh", "Gunnor", "Dharampur"],
        "tribes": ["Gond", "Kol"]
    },
    {
        "district": "Sidhi",
        "reserve": "Sanjay-Dubri Tiger Reserve Buffer",
        "division": "Sidhi Forest Division",
        "lat_range": (24.05, 24.30),
        "lng_range": (81.85, 82.20),
        "villages": ["Dubri", "Bastua", "Kusmi", "Majhauli", "Sihawal", "Rampur Naikin"],
        "tribes": ["Kol", "Gond"]
    },
    {
        "district": "Raisen",
        "reserve": "Ratapani Wildlife Sanctuary Corridor",
        "division": "Raisen Forest Division",
        "lat_range": (22.80, 23.05),
        "lng_range": (77.55, 77.85),
        "villages": ["Obedullaganj", "Dahod", "Delawadi", "Barkheda", "Bhimbetka Buffer"],
        "tribes": ["Gond", "Bhil"]
    },
    {
        "district": "Damoh",
        "reserve": "Nauradehi Wildlife Sanctuary Buffer",
        "division": "Damoh Forest Division",
        "lat_range": (23.45, 23.70),
        "lng_range": (79.15, 79.45),
        "villages": ["Mohli", "Jhapan", "Tendukheda", "Jabera", "Tejgarh"],
        "tribes": ["Gond", "Kol"]
    }
]

# Tribal First Names and Surnames
FIRST_NAMES_MALE = [
    "Sukhram", "Mangal", "Budhram", "Jalam", "Chamru", "Birbal", "Nanhe", "Ramlal", 
    "Tulsiram", "Devsingh", "Shyamlal", "Ghasiram", "Bhagirath", "Mohanlal", "Chainku", 
    "Pyarelal", "Moti", "Rajkaran", "Shivprasad", "Munnalal", "Laxman", "Heeralal", 
    "Chhotelal", "Kalyan", "Gajraj", "Dharam", "Basant", "Babu", "Faguram", "Pardeshi"
]
FIRST_NAMES_FEMALE = [
    "Phulmati", "Radhika", "Sonmati", "Parvati", "Kamla", "Shakuntala", "Basanti", 
    "Kalawati", "Kunti", "Sukhmati", "Ganga", "Jamuna", "Sita", "Geeta", "Sumitra", 
    "Rukmani", "Bismati", "Laxmi", "Savitri", "Urmila", "Tulsi", "Champawati"
]
SURNAMES = [
    "Maravi", "Tekam", "Uikey", "Dhurve", "Netam", "Markam", "Portey", "Warkade", 
    "Pandram", "Kushram", "Shyam", "Korku", "Bharia", "Baiga", "Kol", "Sahariya"
]

OFFICERS = [
    {"id": "OFF-104", "name": "Rajesh Tiwari", "rate": 78, "biased": True},
    {"id": "OFF-108", "name": "Arvind Mishra", "rate": 82, "biased": True},
    {"id": "OFF-112", "name": "Pradeep Sharma", "rate": 74, "biased": True},
    {"id": "OFF-202", "name": "Sunita Patel", "rate": 21, "biased": False},
    {"id": "OFF-205", "name": "Vikram Rathore", "rate": 28, "biased": False},
    {"id": "OFF-209", "name": "Anita Verma", "rate": 24, "biased": False},
    {"id": "OFF-301", "name": "Dinesh Solanki", "rate": 35, "biased": False}
]

CROPS = [
    "Kodo-Kutki Millets & Mustard",
    "Maize & Arhar Pulses",
    "Paddy & Urad Dal",
    "Soybean & Jowar",
    "Traditional Stepped Mustard & Gram",
    "Niger (Ramtil) & Kodo Millet",
    "Sesame & Indigenous Paddy"
]

FOREST_TYPES = [
    "Dense Sal (Shorea robusta) Forest Canopy",
    "Mixed Moist Deciduous Teak Woodland",
    "Protected Wildlife Corridor Bamboo Thicket",
    "Sacred Forest Grove (Devsthan) Reserve",
    "Crown Sal Buffer with Perennial Understory",
    "Natural Teak & Mahua Wildlife Habitat"
]

REJECTION_REASONS_FARMLAND_BIAS = [
    "Field officer noted 'lack of traditional cultivation' without site visit. However, multi-temporal ISRO Bhuvan satellite imagery demonstrates continuous Kharif and Rabi crop tillage from 2019 to 2024. Officer exhibits an anomalous {rate}% rejection rate (+42% over district average). Recommended for immediate DLRC appellate review.",
    "Claim rejected on grounds of 'cultivation post-2005 cut-off'. Bhuvan LISS-III and Sentinel-2 multi-year phenological analysis definitively proves active furrow boundaries and regular seasonal NDVI cycle (ΔNDVI = {delta}) dating before December 2005. High probability of wrongful rejection due to officer bias.",
    "Rejected citing 'overlap with tiger corridor buffer compartment'. Satellite spectral verification confirms active settled 1-hectare homestead and millet plot existing continuously. Rights recognized under Section 3(1)(a) supersede arbitrary executive buffer evictions.",
    "Claim rejected for 'insufficient documentary evidence'. However, applicant submitted Gram Sabha resolution, voter slips, and elder affidavits. Multi-temporal Bhuvan maps establish continuous farming without ecological disturbance."
]

REJECTION_REASONS_GENUINE_FOREST = [
    "Claim lawfully rejected. Multi-spectral Bhuvan satellite inspection across 2019-2024 confirms 78%-88% contiguous canopy closure of mature Sal trees with zero agricultural tillage (seasonal ΔNDVI = {delta} < 0.12). Plot is virgin core forest.",
    "Lawfully rejected. High NIR canopy reflectance and minimal seasonal fluctuation prove plot is uncultivated forest woodland within notified reserve compartment. Recommended to evaluate under Community Forest Resource (CFR) Section 3(1)(i) rather than individual agricultural vesting.",
    "Lawfully rejected. Plot falls entirely within Critical Tiger Habitat core sanctuary with unbroken teak and bamboo crown cover. No historical tillage detected on satellite archives prior to 2005."
]

REJECTION_REASONS_TIME_TRAP = [
    "Procedural stalling: Claim pending for {days} days exceeding the 90-day statutory limit under FRA Rules. Satellite verification already confirms settled farmland with active seasonal cultivation. Officer has withheld DLRC dispatch.",
    "Administrative delay: Claim has remained pending at SDLC review for {days} days without reasoned communication. Satellite indices confirm legitimate 1-hectare farm plot."
]

def generate_1ha_coords(center_lat, center_lng):
    # 1 hectare = 10,000 sqm ≈ 100m x 100m box (or ~0.0009 degrees lat/lng)
    half_side = 0.00045 # approx 50m
    return [
        [round(center_lat - half_side, 6), round(center_lng - half_side, 6)],
        [round(center_lat - half_side, 6), round(center_lng + half_side, 6)],
        [round(center_lat + half_side, 6), round(center_lng + half_side, 6)],
        [round(center_lat + half_side, 6), round(center_lng - half_side, 6)]
    ]

def generate_ndvi_trajectory(is_farmland, base_noise=0.0):
    trajectory = []
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    for y in years:
        yr_noise = (random.random() - 0.5) * 0.04 + base_noise
        if is_farmland:
            monsoon = round(max(0.48, min(0.72, 0.58 + yr_noise + (random.random() * 0.06))), 2)
            fallow = round(max(0.16, min(0.28, 0.22 + yr_noise)), 2)
            harvest = round((monsoon + fallow) / 2.0, 2)
            avg = round((monsoon * 0.5 + harvest * 0.3 + fallow * 0.2), 2)
            trajectory.append({
                "year": y, "avg": avg, "monsoon": monsoon, 
                "harvest": harvest, "fallow": fallow, "cls": "Cultivated"
            })
        else:
            monsoon = round(max(0.72, min(0.88, 0.82 + yr_noise)), 2)
            fallow = round(max(0.58, min(0.72, 0.66 + yr_noise)), 2)
            harvest = round(max(0.65, min(0.78, 0.74 + yr_noise)), 2)
            avg = round((monsoon + harvest + fallow) / 3.0, 2)
            trajectory.append({
                "year": y, "avg": avg, "monsoon": monsoon,
                "harvest": harvest, "fallow": fallow, "cls": "Forest Canopy"
            })
    return trajectory

def generate_200_claims():
    random.seed(42) # Reproducible high quality
    claims = []
    
    # We generate 200 claims: FRA-MP-0023 to FRA-MP-0222
    for i in range(23, 223):
        cid = f"FRA-MP-{str(i).zfill(4)}"
        zone = random.choice(MP_FOREST_ZONES)
        village = random.choice(zone["villages"])
        district = zone["district"]
        tribe = random.choice(zone["tribes"])
        reserve = zone["reserve"]
        division = zone["division"]
        
        is_female = random.random() < 0.35
        first_name = random.choice(FIRST_NAMES_FEMALE if is_female else FIRST_NAMES_MALE)
        surname = random.choice(SURNAMES)
        if "Baiga" in tribe and random.random() < 0.4:
            claimant_name = f"{first_name} Bai Baiga" if is_female else f"{first_name} Baiga"
        elif "Bharia" in tribe and random.random() < 0.4:
            claimant_name = f"{first_name} Bai Bharia" if is_female else f"{first_name} Bharia"
        elif "Sahariya" in tribe and random.random() < 0.4:
            claimant_name = f"{first_name} Sahariya"
        else:
            claimant_name = f"{first_name} {surname}"

        # Category: ~65% Farmland (130 claims), ~35% Forest (70 claims)
        is_farmland = random.random() < 0.65
        land_category = "Farmland" if is_farmland else "Forest"
        
        # 1 Hectare plot as requested by user
        # Allow slight realistic plot variation around 1 hectare (0.8 ha to 1.4 ha, ~2.0 to 3.5 acres)
        area_ha = round(random.choice([1.0, 0.9, 1.1, 1.0, 1.2, 0.85, 1.0]), 2)
        area_acres = round(area_ha * 2.47105, 2)

        # Base coordinates strictly within the selected forest zone
        lat = round(random.uniform(zone["lat_range"][0], zone["lat_range"][1]), 5)
        lng = round(random.uniform(zone["lng_range"][0], zone["lng_range"][1]), 5)
        coords = generate_1ha_coords(lat, lng)

        ndvi_traj = generate_ndvi_trajectory(is_farmland)
        officer = random.choice(OFFICERS)

        # Dates
        days_ago = random.randint(120, 650)
        filed_dt = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 400))
        filed_date = filed_dt.strftime("%Y-%m-%d")

        # Status & Reason determination
        if is_farmland:
            claimed_land_use = f"Agricultural ({random.choice(CROPS)})"
            actual_satellite = "Active Cultivated Field (1 Hectare)"
            
            # Farmland status: 40% Approved, 45% Wrongfully/Contested Rejected, 15% Pending
            rand_stat = random.random()
            if rand_stat < 0.40:
                status = "Approved"
                rejection_reason_given = None
                why_land_was_not_given = "Land WAS recognized. Title vested under Section 3(1)(a). Multi-temporal Bhuvan satellite observations confirmed continuous crop phenology matching 1-hectare agricultural plot pre-dating 2005 cut-off."
                satellite_match_pct = round(random.uniform(91.0, 97.5), 1)
                satellite_verdict = "AGREES"
                confidence_score = int(satellite_match_pct)
                anomaly_flags = ["VERIFIED"]
                decision_date = (filed_dt + timedelta(days=random.randint(45, 110))).strftime("%Y-%m-%d")
                days_pending = (datetime.strptime(decision_date, "%Y-%m-%d") - filed_dt).days
            elif rand_stat < 0.85:
                status = "Rejected"
                # Often associated with biased officers
                if officer["biased"]:
                    anomaly_flags = ["BIAS", "SAT_MISMATCH"]
                else:
                    anomaly_flags = ["SAT_MISMATCH"]
                rejection_reason_given = random.choice([
                    "Plot not under active pre-2005 cultivation / recorded as forest land",
                    "Compartment classified under buffer sanctuary / lacking traditional evidence",
                    "Gram Sabha resolution disputed by beat forest guard",
                    "Fallow land incorrectly marked as abandoned forest encroachment"
                ])
                delta_ndvi = round(ndvi_traj[0]["monsoon"] - ndvi_traj[0]["fallow"], 2)
                why_land_was_not_given = random.choice(REJECTION_REASONS_FARMLAND_BIAS).format(
                    rate=officer["rate"], delta=delta_ndvi
                )
                satellite_match_pct = round(random.uniform(84.0, 93.0), 1)
                satellite_verdict = "AGREES" # Satellite confirms it is farmland, so officer's rejection is MISMATCH
                confidence_score = int(satellite_match_pct)
                decision_date = (filed_dt + timedelta(days=random.randint(60, 180))).strftime("%Y-%m-%d")
                days_pending = (datetime.strptime(decision_date, "%Y-%m-%d") - filed_dt).days
            else:
                status = "Pending"
                rejection_reason_given = None
                days_pending = random.randint(185, 390)
                anomaly_flags = ["TIME_TRAP"]
                why_land_was_not_given = random.choice(REJECTION_REASONS_TIME_TRAP).format(days=days_pending)
                decision_date = None
                satellite_match_pct = round(random.uniform(88.0, 95.0), 1)
                satellite_verdict = "AGREES"
                confidence_score = int(satellite_match_pct)

        else: # Forest
            claimed_land_use = random.choice([
                f"Agricultural ({random.choice(CROPS)})",
                "Traditional Homestead & Agro-forestry",
                "Subsistence Tillage"
            ])
            actual_satellite = random.choice(FOREST_TYPES)
            
            # Forest status: 80% Lawfully Rejected, 10% Erroneously Approved, 10% Pending
            rand_stat = random.random()
            if rand_stat < 0.80:
                status = "Rejected"
                rejection_reason_given = "Land under dense natural forest canopy / Critical Tiger Habitat / Not pre-2005 farmland"
                delta_ndvi = round(ndvi_traj[0]["monsoon"] - ndvi_traj[0]["fallow"], 2)
                why_land_was_not_given = random.choice(REJECTION_REASONS_GENUINE_FOREST).format(delta=delta_ndvi)
                satellite_match_pct = round(random.uniform(89.0, 98.0), 1)
                satellite_verdict = "DISAGREES" # Claim says farm, satellite proves dense forest
                confidence_score = int(satellite_match_pct)
                anomaly_flags = ["SAT_MISMATCH"]
                decision_date = (filed_dt + timedelta(days=random.randint(40, 95))).strftime("%Y-%m-%d")
                days_pending = (datetime.strptime(decision_date, "%Y-%m-%d") - filed_dt).days
            elif rand_stat < 0.90:
                status = "Approved"
                rejection_reason_given = None
                why_land_was_not_given = "CRITICAL AUDIT ALERT: Land approved under Section 3(1)(a) despite satellite verification showing 82% uncultivated dense forest canopy. Potential illegal clearing or irregular title allotment. Flagged for State Level Monitoring Committee (SLMC) review."
                satellite_match_pct = round(random.uniform(82.0, 91.0), 1)
                satellite_verdict = "DISAGREES"
                confidence_score = int(satellite_match_pct)
                anomaly_flags = ["SAT_MISMATCH", "ANOMALY"]
                decision_date = (filed_dt + timedelta(days=random.randint(50, 100))).strftime("%Y-%m-%d")
                days_pending = (datetime.strptime(decision_date, "%Y-%m-%d") - filed_dt).days
            else:
                status = "Pending"
                rejection_reason_given = None
                days_pending = random.randint(190, 320)
                anomaly_flags = ["TIME_TRAP", "SAT_MISMATCH"]
                why_land_was_not_given = f"Application pending for {days_pending} days. Preliminary Bhuvan multispectral imagery detects intact tree canopy. Requires joint Gram Sabha ground inspection before DLC adjudication."
                decision_date = None
                satellite_match_pct = round(random.uniform(85.0, 94.0), 1)
                satellite_verdict = "DISAGREES"
                confidence_score = int(satellite_match_pct)

        docs = ["Village Sabha Resolution", "Land Survey Map", "Aadhaar Card"]
        if random.random() < 0.7:
            docs.append("Elder Witness Affidavit")
        if random.random() < 0.5:
            docs.append("Traditional Use Evidence (Pre-2005 Receipts)")
        if random.random() < 0.3:
            docs.append("Van Adhikar Samiti Recommendation")

        doc = {
            "claim_id": cid,
            "claimant_name": claimant_name,
            "tribe": tribe,
            "village": village,
            "district": district,
            "state": "Madhya Pradesh",
            "forest_reserve": reserve,
            "forest_division": division,
            "area_acres": area_acres,
            "area_ha": area_ha,
            "land_category": land_category,
            "claimed_land_use": claimed_land_use,
            "actual_satellite_land_use": actual_satellite,
            "status": status,
            "rejection_reason_given": rejection_reason_given,
            "why_land_was_not_given": why_land_was_not_given,
            "officer_id": officer["id"],
            "officer_name": officer["name"],
            "officer_rejection_rate": officer["rate"],
            "filed_date": filed_date,
            "decision_date": decision_date,
            "days_pending": days_pending,
            "satellite_match_pct": satellite_match_pct,
            "satellite_verdict": satellite_verdict,
            "confidence_score": confidence_score,
            "anomaly_flags": anomaly_flags,
            "documents_submitted": docs,
            "coords": coords,
            "ndvi_trajectory": ndvi_traj,
            "geojson": {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords + [coords[0]]]
                },
                "properties": {
                    "claim_id": cid,
                    "claimant_name": claimant_name,
                    "village": village,
                    "district": district,
                    "land_category": land_category,
                    "status": status,
                    "area_ha": area_ha
                }
            }
        }
        claims.append(doc)
        
    return claims

def run_seed():
    print(f"Connecting to MongoDB Atlas: {DATABASE_NAME}...")
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=8000)
        db = client[DATABASE_NAME]
        collection = db["claims"]

        # Read existing 22 claims from MongoDB or sample_fra_claims.json to keep them
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'sample_fra_claims.json')
        existing_claims = []
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                existing_claims = json.load(f)
            print(f"Loaded {len(existing_claims)} existing initial claims from {json_path}")

        # Keep initial claims (up to FRA-MP-0022)
        initial_claims = [c for c in existing_claims if int(c.get("claim_id", "FRA-MP-9999").split("-")[-1]) <= 22]
        print(f"Preserving {len(initial_claims)} base baseline claims.")

        new_200 = generate_200_claims()
        print(f"Generated {len(new_200)} new Madhya Pradesh forest-edge claims.")

        all_claims = initial_claims + new_200
        print(f"Total unified claim set: {len(all_claims)} claims.")

        # Clean collection and insert
        collection.delete_many({})
        # Prepare for Mongo insertion (remove _id if present in initial)
        mongo_docs = []
        for c in all_claims:
            cd = dict(c)
            cd.pop("_id", None)
            mongo_docs.append(cd)

        res = collection.insert_many(mongo_docs)
        print(f"Successfully inserted {len(res.inserted_ids)} claims into MongoDB Atlas!")

        # Indexes
        collection.create_index("claim_id", unique=True)
        collection.create_index("district")
        collection.create_index("status")
        collection.create_index("land_category")
        collection.create_index("village")
        print("MongoDB Atlas indexes ensured.")

        # Sync local sample_fra_claims.json (without _id)
        with open(json_path, 'w') as f:
            json.dump(mongo_docs, f, indent=2, default=str)
        print(f"Synchronized local JSON file: {json_path} ({os.path.getsize(json_path)} bytes)")

        return True
    except Exception as e:
        print(f"Error during seeding: {e}")
        return False

if __name__ == "__main__":
    run_seed()
