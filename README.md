# 🌿 FRA Guardian — AI Decision Support & ISRO Bhuvan Satellite Verification System
### *Forest Rights Act (FRA 2006) — Madhya Pradesh Pilot*

> **An end-to-end AI-powered platform that helps government officers make fast, evidence-based decisions on tribal land rights claims using satellite imagery, real-time data analytics, and multi-agent AI deliberation.**

---

## 📋 Table of Contents

1. [Why We Built This](#-why-we-built-this)
2. [How It Helps the Government](#-how-it-helps-the-government)
3. [System Architecture & Workflow](#-system-architecture--workflow)
4. [Features In Detail](#-features-in-detail)
5. [Technology Stack](#-technology-stack)
6. [Database](#-database)
7. [Data — Sources & How We Fetched It](#-data--sources--how-we-fetched-it)
8. [Running the Project Locally](#-running-the-project-locally)
9. [Future Potential & What We Can Add](#-future-potential--what-we-can-add)
10. [Limitations We Faced](#-limitations-we-faced)
11. [Dataset Statistics](#-dataset-statistics)

---

## 🎯 Why We Built This

India's **Forest Rights Act, 2006 (FRA)** was enacted to recognize and vest the forest land rights of tribal communities (*Scheduled Tribes*) and other traditional forest dwellers who have lived on and cultivated forest land for generations before December 13, 2005.

### The Problem

Despite a landmark law, implementation is deeply broken:

- **Over 1.9 million claims** are pending across India as of 2024
- **Madhya Pradesh alone** has hundreds of thousands of unresolved cases
- Decisions rely entirely on paper-based documentation, hand-drawn maps, and officer discretion — making them **slow, opaque, and prone to bias**
- Officers with high rejection rates face **zero accountability** — a single officer can reject thousands of rightful claims without written reasons
- Tribal claimants, many of them **illiterate and remote**, cannot challenge decisions effectively
- **Critical satellite data** from ISRO's Bhuvan platform exists but is **never systematically used** in the decision-making process

### The Solution

FRA Guardian bridges satellite science, AI reasoning, and government decision-making into a single unified platform. It turns raw ISRO Bhuvan imagery, NDVI time-series, and crop phenology data into **actionable, legally-grounded evidence** that any officer or tribunal can review in seconds — not weeks.

---

## 🏛️ How It Helps the Government

### 1. Speed — From Months to Minutes
A manual FRA review involves coordinating field surveys, getting satellite prints from ISRO, cross-referencing revenue records, and scheduling committee hearings. FRA Guardian collapses all of this into a **single dashboard screen**. An officer can review a full satellite-verified dossier in under 2 minutes.

### 2. Transparency & Accountability
Every decision in the system is backed by:
- 6-year multi-temporal NDVI trajectory (2019–2024)
- Phenological crop cycle identification (Kharif / Rabi / Zaid)
- Officer bias audit (rejection rate benchmarked against district average)
- Automatic anomaly flagging when satellite data contradicts officer decision

### 3. Legally Grounded AI
The AI Debate module frames every argument in the **exact statutory language** of FRA 2006:
- Section 3(1)(a) — individual forest rights
- Section 4(3) — process for recognition
- Rule 12A — procedure for Sub-Divisional Level Committee (SDLC)
- Gram Sabha resolutions as primary evidence

### 4. Standardisation of Evidence
Instead of each district using different formats, FRA Guardian creates a uniform **1-Hectare GIS-standard dossier** for every claim, making appeals, audits, and court submissions straightforward.

### 5. Scalability
The same workflow built for Madhya Pradesh's 220 pilot claims can be **scaled to any state and any number of claims** simply by loading new data into MongoDB Atlas.

---

## 🔧 System Architecture & Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRA GUARDIAN SYSTEM                         │
│                                                                     │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐  │
│  │   MongoDB     │    │  FastAPI Backend  │    │  Python Build    │  │
│  │   Atlas       │◄──►│  (Port 8000)      │    │  Script          │  │
│  │  fra_guardian │    │  main.py          │    │  build_unified_  │  │
│  │  .claims      │    │  /api/claims      │    │  index.py        │  │
│  └──────────────┘    └──────────────────┘    └────────┬─────────┘  │
│                                                        │             │
│                                              ┌─────────▼──────────┐ │
│                                              │   index.html        │ │
│                                              │   (Single-File App) │ │
│                                              │   ~897 KB           │ │
│                                              └─────────┬──────────┘ │
│                                                        │             │
│                               ┌────────────────────────▼──────────┐ │
│                               │        HTTP Server (Port 8088)     │ │
│                               │        python3 -m http.server      │ │
│                               └───────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Workflow

```
1. DATA SEEDING
   └── sample_fra_claims.json (220 realistic MP claims)
       └── Seeded into MongoDB Atlas via backend seed script

2. BACKEND STARTUP
   └── FastAPI runs on port 8000
       └── /api/claims → returns live claims from MongoDB Atlas
       └── /api/analyze-area → runs 1-ha algorithmic scan

3. FRONTEND BUILD
   └── build_unified_index.py reads sample_fra_claims.json
       └── Embeds all 220 claims as JS const FRA_CLAIMS = [...]
       └── Generates a fully self-contained index.html (~897 KB)

4. PAGE LOAD
   └── index.html loads in browser (port 8088)
       └── Attempts GET http://localhost:8000/api/claims
           ├── If MongoDB ONLINE → replaces embedded data with live Atlas data
           └── If MongoDB OFFLINE → uses embedded 220-claim fallback (works offline)

5. USER INTERACTION
   └── Officer opens Dashboard → reviews KPIs and anomaly feed
   └── Switches to ISRO Bhuvan → sees all 220 pins on satellite map
   └── Clicks any pin → views 1-Ha survey overlay + NDVI chart
   └── Changes Year/Month → map overlay updates with crop phenology
   └── Runs AI Debate → 4 agents deliberate and deliver verdict
   └── Uses Scan Request → submits new GPS scan to MongoDB
```

---

## 📱 Features In Detail

### Tab 1 — 📊 Dashboard

The command-center view for any reviewing officer.

#### KPI Cards (Live from MongoDB Atlas)
| Card | Description |
|------|-------------|
| **Total Claims** | Live count of all FRA claims in the database |
| **Approved** | Claims with title vested under Section 3(1)(a) |
| **Vesting Rate %** | (Approved / Total) × 100 — district-level benchmark |
| **Anomalies Flagged** | Claims where officer decision conflicts with satellite data |
| **Farmland / Forest** | Split by land category |
| **Pending** | Awaiting SDLC decision |

#### Anomaly Feed
- Automatically surfaces the most suspicious cases — claims where the **satellite verdict (SAT_MISMATCH) contradicts the officer's decision**
- Each card shows: Claim ID, claimant name, village, district, anomaly flag type, and quick-action buttons to jump to the Map or AI Debate

#### Global Search
- Searches across: Claim ID, claimant name, village, district, land category, status, officer name, **and month names / seasons**
- Typing "Kharif" or "July" returns all claims filed or active during monsoon season
- Typing "Baiga" returns all claims by that tribe

#### Claim Inspector / Dossier Panel
- Full legal dossier for any selected claim including:
  - Claimant identity, tribe, village, forest division
  - Land use (claimed vs satellite-observed)
  - Status pill (Approved / Rejected / Pending)
  - Why land was denied (full text of officer note)
  - Officer name, ID, and rejection rate audit
  - Quick links to ISRO Bhuvan Verification and AI Debate

#### AI Brief Generator (Typewriter Output)
Three one-click briefs generated in real time:
- **DLRC Memorandum** — formal submission to District Level Committee
- **Spatial Cross-Examination** — ISRO Bhuvan coordinates and NDVI evidence brief
- **Officer Bias Audit** — statistical analysis of officer rejection rate vs district average

#### Month/Season Selector Strip
- 12-month horizontal strip (Jan–Dec) with **Kharif / Rabi / Zaid** agro-ecological season badges
- Selecting a month updates the phenological profile across all views

#### Year Timeline Slider
- Slide from 2019 to 2025 to examine multi-year land use history
- Drives NDVI chart, crop stage badge, and Bhuvan map overlay

---

### Tab 2 — 🛰️ ISRO Bhuvan Map Verification

The core evidence layer of the platform — a live satellite GIS map showing all 220 FRA claims.

#### All 220 Pins Plotted by Default
From the moment the map loads, **all 220 FRA claim locations** across Madhya Pradesh are plotted as circular pins, color-coded by category:
- 🟡 **Amber** — Farmland claims (135)
- 🟢 **Green** — Forest claims (85)
- 🔴 **Red** — Anomaly/disputed claims (159)
- 🟢 **Emerald** — Approved/verified claims (61)

#### Interactive Pin Selection
- **Click any pin** → map smoothly zooms to that location (zoom 16)
- **1-Hectare circular boundary** (radius = 56.42 m, area = 10,000 m²) overlaid on the satellite imagery
- **Dossier panel** on the right instantly loads that claim's data
- Selected pin **pulses with a ring animation** to clearly identify focus

#### Map Filter Bar
Filter the 220 pins down by category:
```
[All (220)] [🌾 Farmland] [🌲 Forest] [🚨 Anomalies] [✅ Approved]
```
Filter button label dynamically updates from live data count.

#### Dynamic 1-Hectare Field Overlay (Changes with Year & Month!)
This is the most technically advanced feature — the 1-Ha boundary circle **changes its visual appearance** based on the selected year and month, simulating what ISRO's multi-spectral satellite would observe:

| Season | Months | Visual Rendering |
|--------|--------|-----------------|
| **Kharif (Monsoon)** | Jul–Oct | Vibrant emerald green crop canopy with parallel furrow rows (active millets/maize) |
| **Rabi (Winter)** | Nov–Feb | Golden amber harvest canopy (mustard/wheat/pulses) |
| **Zaid (Summer)** | Mar–Jun | Terracotta dry ploughed fallow soil texture |
| **Forest Canopy** | Year-round | Perennial deep emerald with tree crown stipples |

This directly answers the key legal question: *"Was this land cultivated continuously before 2005?"*

#### NDVI Multi-Temporal Chart
- Canvas-rendered chart showing the annual NDVI swing (2019–2024) for the selected claim
- Farmland shows a **distinct seasonal oscillation** (low in fallow, high in crop season)
- Forest shows **stable high NDVI** year-round
- This pattern is legally decisive — it distinguishes farmland from forest encroachment

#### Bottom Ribbon (Live Data Bar)
Constantly shows the current phenological state:
```
Crop Stage: Kharif Grain Filling (Active Cultivated)  |  NDVI: 0.68  |  Rainfall: 185mm  |  Soil Moisture: High (74%)
```

#### Expandable Map Mode
Clicking **⛶ Expand Map** collapses the sidebar and gives the map full-width view for detailed spatial inspection.

#### Preferred Pointer Color System
Officers can customise pin colors from 4 presets (Normal Standard, ISRO GIS, Forest Earth, High Contrast) or use custom color pickers. Preferences are saved in localStorage.

---

### Tab 3 — 🤖 AI Multi-Agent SDLC Hearing Debate

A fully simulated Sub-Divisional Level Committee (SDLC) hearing powered by 4 specialized AI agents who **actively argue with each other** about the claim, citing actual FRA sections, NDVI data, and Gram Sabha records.

#### The 4 Agents

| Agent | Role | Expertise |
|-------|------|-----------|
| **Arjun Mehta** | Tribal Rights Legal Counsel | Cites FRA Sec 3(1)(a), Sec 4(3), Rule 12A — advocates for claimant |
| **Priya Sharma** | Range Forest Officer (RFO) | Scrutinises forest compartment buffers, questions encroachment |
| **Sunita Patel** | Tribal Welfare Officer (TWO) | Cites Gram Sabha resolution, NDVI phenology, community evidence |
| **Vikram Rathore** | SDM / SDLC Chair | Weighs all arguments, delivers consensus verdict |

#### How the Debate Works
- 8 structured turns where agents **address each other by name**, challenge arguments, and present exhibits
- Each agent cites specific evidence: NDVI values, Gram Sabha resolutions, officer audit data
- Exhibit cards pop up mid-debate: satellite imagery evidence, historical NDVI chart
- **Speaking indicators** (typing animation) show which agent is currently active
- Ends with **unanimous SDLC consensus ruling** — a formal resolution awarding or denying title

#### Controls
- **▶️ Start Debate (Animated)** — watch the debate unfold turn by turn in real time
- **⚡ Show Full Hearing Immediately** — instantly reveals the complete transcript

---

### Tab 4 — 📡 Scan Request (New Claim Submission)

Portal for field officers to submit **new scan requests** from GPS coordinates.

- Enter GPS coordinates (Lat / Lng) for a new claim location
- Select 1-Ha radius (56.42 m standard) or custom area
- Mini preview map shows the scan circle on the coordinates
- **Run Area Analysis Algorithm** — calls FastAPI `/api/analyze-area` endpoint:
  1. Checks if coordinates fall within a known forest reserve buffer zone
  2. Calculates predicted NDVI for the month
  3. Returns a preliminary farmland vs forest classification
- **Submit to MongoDB** — stores the scan result as a new claim record in Atlas

---

## 🛠️ Technology Stack

### Frontend
| Technology | Version | Usage |
|-----------|---------|-------|
| **HTML5** | — | Semantic page structure |
| **Vanilla CSS** | — | All styling, animations, responsive layout |
| **Vanilla JavaScript (ES6+)** | — | All interactivity, map rendering, AI debate engine |
| **Leaflet.js** | 1.9.4 (CDN) | Interactive satellite map, pin markers, polygon overlays |
| **HTML5 Canvas API** | — | NDVI time-series chart rendering (no Chart.js dependency) |
| **Google Fonts** | — | Inter, JetBrains Mono, Outfit typefaces |

> **Zero npm. Zero React. Zero build tools.** The entire frontend is a single `index.html` file (~897 KB) that runs directly in any browser.

### Backend
| Technology | Version | Usage |
|-----------|---------|-------|
| **Python** | 3.10+ | Primary backend language |
| **FastAPI** | 0.111.0 | REST API framework |
| **Uvicorn** | 0.30.1 | ASGI server |
| **PyMongo** | — | MongoDB Atlas driver |
| **Pydantic** | — | Request/response data validation |
| **python-dotenv** | 1.0.1 | Environment variable management |
| **httpx** | 0.27.0 | Async HTTP client |

### Build Pipeline
| Technology | Usage |
|-----------|-------|
| **Python** | `build_unified_index.py` — reads `sample_fra_claims.json`, embeds 220 claims inline, generates `index.html` |
| **python3 http.server** | Static file server on port 8088 for local development |

---

## 🗄️ Database

### MongoDB Atlas (Cloud)
- **Provider**: MongoDB Atlas (Free Tier / M0 cluster)
- **Database**: `fra_guardian`
- **Collection**: `claims`
- **Records**: 220 FRA claim documents

#### Document Schema
```json
{
  "claim_id": "FRA-MP-0001",
  "claimant_name": "Phulmati Bai Baiga",
  "tribe": "Baiga (PVTG)",
  "village": "Samnapur",
  "district": "Dindori",
  "state": "Madhya Pradesh",
  "forest_division": "Dindori Forest Division",
  "forest_reserve": "Fossil National Park Buffer",
  "land_category": "Farmland",
  "area_ha": 0.61,
  "area_acres": 1.5,
  "claimed_land_use": "Agricultural (Kodo-Kutki Millets & Mustard)",
  "actual_satellite_land_use": "Active Cultivated Field",
  "status": "Approved",
  "anomaly_flags": ["VERIFIED"],
  "satellite_verdict": "AGREES",
  "satellite_match_pct": 94.0,
  "confidence_score": 94,
  "coords": [[22.95, 81.08], [22.958, 81.088]],
  "ndvi_trajectory": [
    { "year": 2019, "monsoon": 0.58, "harvest": 0.32, "fallow": 0.22, "avg": 0.40 }
  ],
  "officer_id": "OFF-202",
  "officer_name": "Sunita Patel",
  "officer_rejection_rate": 21,
  "why_land_was_not_given": "Land WAS granted. Title successfully recognized...",
  "filed_date": "2023-02-18",
  "decision_date": "2023-06-05",
  "days_pending": 107,
  "geojson": { "type": "Feature", "geometry": { "type": "Polygon", "coordinates": [[...]] } }
}
```

#### Fallback Mode
If MongoDB Atlas is offline, the frontend automatically falls back to its **embedded 220-claim dataset** — the app never goes blank. This is critical for rural government offices with unreliable connectivity.

---

## 📡 Data — Sources & How We Fetched It

### 1. Geographic Coordinates
- **Source**: Real GPS coordinates of forest reserve boundaries in Madhya Pradesh
- **Method**: ISRO Bhuvan Portal (bhuvan.nrsc.gov.in) GIS layers + Survey of India topographic maps (public domain)
- **Covered Areas**: Kanha, Bandhavgarh, Satpura, Pench, Panna National Parks and their buffer zones

### 2. NDVI Time-Series Data
- **Source**: ISRO Bhuvan Temporal NDVI Analysis Service (publicly accessible reports)
- **What it is**: Normalized Difference Vegetation Index = (NIR - Red) / (NIR + Red), ranging 0.0 to 1.0
- **How we modelled it**: Seasonal NDVI swing patterns from NRSC crop monitoring bulletins (2019–2024)
  - Farmland Kharif peak: NDVI 0.58–0.68 | Fallow trough: NDVI 0.20–0.25
  - Forest year-round: NDVI 0.78–0.88

### 3. Tribal Claimant Data
- **Source**: Modelled after structures from:
  - MP FRA Portal (vanaadhikar.mp.gov.in) report formats
  - TISS FRA implementation audit reports (2018–2022)
  - Community Forest Rights Learning and Advocacy (CFRLA) case database
- **Tribes**: Baiga (PVTG), Bharia (PVTG), Sahariya (PVTG), Gond, Bhil, Bhilala, Korku, Kol, Halba, Madia Gond, Dhurwa

### 4. Officer Data
- **Source**: Modelled after real SDLC officer structures in MP districts
- **Rejection rates**: Based on published audit data from Ministry of Tribal Affairs (MoTA) annual FRA report (2022–23)

### 5. Forest Reserve Data
- **Source**: MoEFCC Protected Area Network + Wildlife Institute of India (WII) corridor maps
- **32 Forest Reserves**: Kanha Tiger Reserve, Bandhavgarh National Park, Satpura Biosphere Reserve, Pench Tiger Reserve, Panna Tiger Reserve, Kuno Wildlife Sanctuary + 27 additional buffer zones

### 6. Legal Framework Data
- **FRA 2006 Sections and Rules**: Ministry of Law and Justice official gazette (egazette.nic.in)
- **Rule 12A Procedure**: MoTA model guidelines for SDLC proceedings

---

## 💻 Running the Project Locally

### Prerequisites
```bash
Python 3.10+
```

### Step 1 — Install Backend Dependencies
```bash
cd fra-guardian/backend
pip install fastapi uvicorn pymongo python-dotenv httpx
```

### Step 2 — Configure MongoDB Atlas (Optional)
Edit `backend/.env`:
```env
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
DATABASE_NAME=fra_guardian
```
> Skip this step if you want offline/embedded mode.

### Step 3 — Start the FastAPI Backend
```bash
cd fra-guardian/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 4 — Build the Frontend
```bash
cd fra-guardian
python3 build_unified_index.py
# Output: Generated unified index.html successfully: ~897533 bytes
```

### Step 5 — Serve the Frontend
```bash
cd fra-guardian
python3 -m http.server 8088 --bind 0.0.0.0
```

### Step 6 — Open in Browser
```
http://localhost:8088/index.html
```

> The app works fully offline (embedded data). MongoDB Atlas enhances it with live data if connected.

---

## 🔮 Future Potential & What We Can Add

### 1. 🛰️ Real ISRO Bhuvan API Integration
Replace simulated NDVI values with **live calls to ISRO Bhuvan's OGC/WMS APIs** (bhuvan-ras.nrsc.gov.in), pulling actual multi-spectral imagery for any coordinate on demand. ISRO's Bhuvan platform already exposes WMS tile services — integrating them would make every overlay 100% real satellite data.

### 2. 🤖 Groq / Gemini LLM-Powered Debate
Replace pre-scripted agent turns with a **live LLM API call (Groq / Google Gemini / GPT-4)** — truly dynamic debates where agents respond to the specific data of each claim in real time, generating different arguments for every claimant.

### 3. 📱 Mobile-First Field Officer App
A lightweight React Native / Flutter app for field officers to:
- Submit new GPS scan requests with phone camera + location
- Photograph and upload documents to Atlas
- Receive instant AI pre-assessment of their claim

### 4. 🗺️ Multi-State Expansion
The data model is entirely state-agnostic. Adding claims from **Jharkhand, Odisha, Chhattisgarh, and Assam** (states with the highest FRA pendency) requires only loading new JSON data.

### 5. 📄 PDF Dossier Auto-Generation
Use **ReportLab** (already in `requirements.txt`) to auto-generate a legally formatted PDF dossier per claim — including the NDVI chart, satellite coordinates, statutory citations, and officer audit — ready for tribunal submission.

### 6. 📊 Officer Performance Dashboard
A separate analytics panel for District Collectors showing officer-level rejection rate trends, district-wise approval rates, and automatic alerts when an officer's rate deviates more than 2σ from the district average.

### 7. 🔔 Pendency Alerts & SLA Enforcement
Automatic email/SMS alerts when claims exceed the **60-day statutory decision period** under FRA Rule 12A — directly notifying the Collector and State Tribal Department.

### 8. 🌐 National FRA Portal Integration
Connect to the Ministry of Tribal Affairs **Vanadhikar Online Portal** API to pull live national data directly, eliminating manual seeding.

### 9. 🏘️ Gram Sabha e-Resolution Module
A tamper-proof digital platform for Gram Sabhas to pass and record resolutions with digital signatures, timestamping, and automatic forwarding to the SDLC.

### 10. 🔍 Satellite Change Detection Alerts
Monitor 1-Ha plots over time using **Sentinel-2 time series** — automatically alert if land use changes after a claim is filed (e.g., a forest plot is cleared, or farmland is rewilded).

---

## ⚠️ Limitations We Faced

### 1. No Real ISRO Bhuvan API Access
**The biggest limitation.** ISRO's Bhuvan platform does not have a public open-data API that serves raw NDVI values or multi-spectral imagery at pixel level for arbitrary coordinates. The WMS tile services serve visual imagery only, not spectral data. We simulated NDVI values using published phenological models rather than pulling real satellite readings.

### 2. Synthetic (Not Live) Claimant Data
Due to the sensitivity and privacy of actual FRA claimant records, we could not access real Ministry of Tribal Affairs or state government databases. All 220 claims are realistically modelled but are not actual government records.

### 3. Static AI Agents
The AI debate agents use carefully crafted pre-written scripts rather than live LLM inference. While the content is legally accurate and contextually specific to each claim's data, agents cannot dynamically respond to novel arguments.

### 4. Third-Party Satellite Tiles
The Leaflet map uses ESRI World Imagery tiles (public). These are not ISRO Bhuvan's own layers. ISRO Bhuvan provides Cartosat/ResourceSat imagery which requires authenticated access — not available for open integration.

### 5. No Real-Time SDLC Data Feed
The system cannot currently sync with the actual Madhya Pradesh government FRA portal (vanaadhikar.mp.gov.in). There is no open API from state government systems. Any real deployment would require a government-side MoU and API access.

### 6. Offline NDVI Chart
The NDVI time-series chart is rendered on HTML5 Canvas using modelled data — not connected to a real satellite data stream. Each year's NDVI trajectory is a parametric simulation calibrated to known seasonal patterns.

### 7. Scale & Performance
The current architecture embeds all 220 claims as an inline JavaScript array in `index.html`. This works well at 220 claims but would become a bottleneck at 10,000+ claims. A production system would require pagination, MongoDB Atlas Search indexing, and lazy-loading.

### 8. No Authentication / Role-Based Access
The current build has no login system. In a real government deployment, role-based access control would be mandatory — distinguishing claimants, field officers, SDLC members, collectors, and state-level auditors.

---

## 📊 Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Claims** | 220 |
| **Approved** | 61 (27.7%) |
| **Rejected** | 127 (57.7%) |
| **Pending** | 32 (14.5%) |
| **Farmland Claims** | 135 (61.4%) |
| **Forest Claims** | 85 (38.6%) |
| **Anomaly Flagged** | 159 (72.3%) |
| **Districts Covered** | 19 |
| **Forest Reserves Covered** | 32 |
| **Tribes Represented** | 11 (including 3 PVTGs) |
| **Year Range** | 2019–2025 |
| **State** | Madhya Pradesh |

### Districts Covered
Alirajpur, Anuppur, Balaghat, Barwani, Betul, Chhindwara, Damoh, Dhar, Dindori, Hoshangabad, Mandla, Narmadapuram, Panna, Raisen, Seoni, Shahdol, Sheopur, Sidhi, Umaria

### Tribes Represented
Baiga (PVTG), Bharia (PVTG), Sahariya (PVTG), Gond, Bhil, Bhilala, Korku, Kol, Halba, Madia Gond, Dhurwa

---

## 📁 Project File Structure

```
fra-guardian/
│
├── index.html                    # Generated single-file frontend (~897 KB)
├── build_unified_index.py        # Build script — generates index.html from data
├── sample_fra_claims.json        # 220 FRA claims dataset (embedded + Atlas seed)
├── farmland.jpg                  # Reference satellite image — farmland
├── forest.jpg                    # Reference satellite image — forest
├── README.md                     # This file
│
├── backend/
│   ├── main.py                   # FastAPI app — REST API endpoints
│   ├── models.py                 # Pydantic data models
│   ├── database.py               # MongoDB Atlas connection
│   ├── requirements.txt          # Python package dependencies
│   ├── .env                      # MongoDB Atlas URI (not committed to git)
│   ├── routes/                   # API route handlers
│   └── data/                     # Backend static data assets
│
└── frontend/
    └── generate_frontend.py      # Legacy frontend generator (superseded by build_unified_index.py)
```

---

## 🙏 Acknowledgements

- **ISRO NRSC** — Bhuvan Satellite Platform & NDVI phenological research
- **Ministry of Tribal Affairs, Government of India** — FRA 2006 statutory framework
- **Campaign for Survival and Dignity (CSD)** — FRA implementation documentation
- **TISS & CFRLA** — Field audit reports and community evidence frameworks
- **Wildlife Institute of India (WII)** — Protected area corridor mapping

---

*Built as a technology pilot to demonstrate how AI, satellite imagery, and open data can accelerate justice for India's tribal communities under the Forest Rights Act, 2006.*
# FRA-Guardian-AI-Decision-Support-ISRO-Bhuvan-Satellite-Verification-System
# FRA-Guardian-AI-Decision-Support-ISRO-Bhuvan-Satellite-Verification-System
