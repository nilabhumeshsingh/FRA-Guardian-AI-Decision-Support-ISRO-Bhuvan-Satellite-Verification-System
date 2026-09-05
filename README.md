# 🌿 FRA Guardian — AI Decision Support & ISRO Bhuvan Satellite Verification System

### *Forest Rights Act (FRA 2006) — Madhya Pradesh Pilot*

> **An end-to-end AI-powered platform that accelerates tribal land rights verification using ISRO Bhuvan satellite imagery, real-time data analytics, and multi-agent AI deliberation.**

---

## 🎯 Executive Summary

India's **Forest Rights Act (FRA), 2006** aims to grant land titles to forest-dwelling communities. However, over **1.9 million claims remain pending nationwide** due to slow paper-based workflows, hand-drawn maps, and potential inconsistencies in manual decision-making.

**FRA Guardian** bridges satellite science and legal workflows. It converts ISRO Bhuvan imagery, 6-year multi-temporal NDVI trajectory data, and crop phenology into **1-Hectare GIS-standard dossiers**, helping reduce weeks of manual review into a **2-minute automated audit**.

---

## 🏛️ Key Value Propositions

* **Speed & Scale:** Collapses manual field cross-referencing into a single dashboard screen for rapid SDLC/DLRC review.
* **Data-Driven Accountability:** Flags officer bias by benchmarking individual rejection rates against district averages and auto-detecting satellite vs. officer decision mismatches (`SAT_MISMATCH`).
* **Statutory AI Alignment:** Evaluates claims within the legal framework of FRA 2006, including Section 3(1)(a), Section 4(3), and Rule 12A.
* **Offline Resilience:** Automatically switches to an embedded dataset when rural district connectivity drops.

---

## 🔧 Architecture & Workflow

```text
┌─────────────────────────────────────────────────────────────────────┐
│                       FRA GUARDIAN SYSTEM                           │
│                                                                     │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐  │
│  │   MongoDB    │    │  FastAPI Backend │    │   Python Build   │  │
│  │    Atlas     │◄──►│   (Port 8000)    │    │      Script      │  │
│  │ fra_guardian │    │    main.py       │    │  build_unified_  │  │
│  │   .claims    │    │   /api/claims    │    │   index.py       │  │
│  └──────────────┘    └──────────────────┘    └────────┬─────────┘  │
│                                                       │             │
│                                              ┌────────▼──────────┐ │
│                                              │    index.html     │ │
│                                              │  (Single-File)    │ │
│                                              └────────┬──────────┘ │
│                                                       │             │
│                              ┌────────────────────────▼──────────┐ │
│                              │       HTTP Server (Port 8088)     │ │
│                              └───────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Workflow

1. **Seeding:** Stores 220 Madhya Pradesh pilot claims in MongoDB Atlas using `sample_fra_claims.json`.
2. **Backend API:** FastAPI runs on port `8000`, serves live MongoDB queries, and performs 1-Hectare spatial area analysis.
3. **Frontend Build:** `build_unified_index.py` bundles the UI and fallback data into a zero-dependency, self-contained `index.html` (~897 KB).
4. **Execution Mode:** The application fetches live MongoDB data when available and automatically uses the embedded dataset when offline.

---

## 📱 Platform Features

### 1. 📊 Executive Dashboard

* **Live KPI Counters:** Total claims, approval rates, anomaly alerts, and land distribution.
* **Anomaly Engine:** Automatically surfaces claims where satellite observations contradict officer rejection notes.
* **Global Filter & Search:** Search across claimant names, PVTG tribes, districts, and seasonal categories such as *Kharif*, *Rabi*, and *Zaid*.
* **Automated AI Briefs:** Generates DLRC Memorandums, Spatial Cross-Examinations, and Officer Bias Audits.

---

### 2. 🛰️ ISRO Bhuvan GIS Verification

* **220 Interactive Coordinates:** Claim locations categorized as Farmland, Forest, Verified, and Disputed.

* **Dynamic 1-Hectare Seasonal Overlays:** Visuals change according to the selected month and year.

  * **Kharif (Monsoon):** Active crop canopy.
  * **Rabi (Winter):** Harvest canopy.
  * **Zaid (Summer):** Dry, ploughed fallow soil.

* **NDVI Time-Series Canvas:** Visualizes vegetation index patterns from 2019–2024 to support land-use and cultivation analysis.

---

### 3. 🤖 Multi-Agent SDLC Hearing Debate

Simulates a Sub-Divisional Level Committee hearing using four specialized AI personas that debate the validity of each claim.

* **Legal Counsel — Arjun Mehta:** Cites FRA 2006 sections and Rule 12A.
* **Range Forest Officer — Priya Sharma:** Scrutinizes compartment boundaries and potential forest encroachment.
* **Tribal Welfare Officer — Sunita Patel:** Validates Gram Sabha resolutions and historical community evidence.
* **SDM / SDLC Chair — Vikram Rathore:** Evaluates all arguments and renders a final consensus ruling.

---

### 4. 📡 Field Scan Request

Allows field officers to:

* Enter custom GPS coordinates.
* Trigger the spatial boundary analysis algorithm.
* Evaluate forest reserve proximity.
* Generate preliminary land-use analysis.
* Store new records in MongoDB Atlas.

---

## 🛠️ Technology Stack

### Frontend

* Vanilla JavaScript (ES6+)
* HTML5
* CSS3
* Leaflet.js
* HTML5 Canvas API

> **Zero React, Node.js, or npm dependencies.**

### Backend

* Python 3.10+
* FastAPI
* Uvicorn
* PyMongo
* Pydantic

### Database

* MongoDB Atlas
* Embedded local fallback dataset

---

## 💻 Quick Start

### 1. Backend Setup

```bash
cd fra-guardian/backend
pip install fastapi uvicorn pymongo python-dotenv httpx
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Build and Launch Frontend

```bash
cd fra-guardian
python3 build_unified_index.py
python3 -m http.server 8088
```

Access the application at:

`http://localhost:8088/index.html`

### Optional MongoDB Configuration

Configure MongoDB connectivity in:

```text
backend/.env
```

Using:

```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=fra_guardian
```

---

## 📊 Dataset Overview — Madhya Pradesh Pilot

| Metric                 | Details                                                                          |
| ---------------------- | -------------------------------------------------------------------------------- |
| **Total Pilot Claims** | 220 claims across 19 districts and 32 forest reserves                            |
| **Status Split**       | Approved: 61 (27.7%) · Rejected: 127 (57.7%) · Pending: 32 (14.5%)               |
| **Land Distribution**  | Farmland: 135 (61.4%) · Forest: 85 (38.6%)                                       |
| **Flagged Anomalies**  | 159 claims (72.3%)                                                               |
| **Tribes Covered**     | Baiga (PVTG), Bharia (PVTG), Sahariya (PVTG), Gond, Bhil, Korku, Kol, and others |

---

## ⚠️ Known Limitations & Future Roadmap

### 🛰️ Live Bhuvan API Access

Current NDVI curves use published NRSC phenological models because public access to raw pixel-level satellite APIs is restricted. Direct OGC/WMS integration is planned for a future phase.

### 🤖 LLM Engine Upgrade

Multi-agent debates currently use structured evidentiary scripts. Future releases may integrate live Gemini, Groq, or other LLM pipelines.

### 📱 Mobile Field Application

A lightweight mobile application is planned with:

* Offline GPS capability.
* Field data collection.
* Document OCR.
* Mobile claim submission.
* Preliminary AI-based assessments.

---

> *Built to demonstrate how spatial data, transparent AI reasoning, and open legal frameworks can accelerate justice under the Forest Rights Act, 2006.*
