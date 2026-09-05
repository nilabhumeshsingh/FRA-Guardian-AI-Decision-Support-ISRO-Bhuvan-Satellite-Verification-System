🌿 FRA Guardian — AI Decision Support & ISRO Bhuvan Satellite Verification System
Forest Rights Act (FRA 2006) — Madhya Pradesh Pilot
An end-to-end AI-powered platform that accelerates tribal land rights verification using ISRO Bhuvan satellite imagery, real-time data analytics, and multi-agent AI deliberation.

🎯 Executive Summary
India's Forest Rights Act (FRA), 2006 aims to grant land titles to forest-dwelling communities. However, over 1.9 million claims remain pending nationwide due to slow paper-based workflows, hand-drawn maps, and officer bias.
FRA Guardian bridges satellite science and legal workflows. It converts raw ISRO Bhuvan imagery, 6-year multi-temporal NDVI trajectory data, and crop phenology into 1-Hectare GIS-standard dossiers, turning weeks of manual review into a 2-minute automated audit.
🏛️ Key Value Propositions
Speed & Scale: Collapses manual field cross-referencing into a single dashboard screen for rapid SDLC/DLRC review.
Data-Driven Accountability: Flags officer bias by benchmarking individual rejection rates against district averages and auto-detecting satellite vs. officer decision mismatches (SAT_MISMATCH).
Statutory AI Alignment: Evaluates claims strictly within the legal bounds of FRA 2006 (Section 3(1)(a), Section 4(3), and Rule 12A).
Offline Resilience: Auto-fails over to an embedded dataset when rural district connectivity drops.
🔧 Architecture & Workflow
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
Seeding: Stores 220 MP pilot claims in MongoDB Atlas (sample_fra_claims.json).
Backend API: FastAPI (port 8000) serves live MongoDB queries and runs the 1-Ha spatial area analysis algorithm.
Frontend Build: build_unified_index.py bundles the UI and fallback data into a zero-dependency, self-contained index.html (~897 KB).
Execution Mode: App fetches live MongoDB data on launch; automatically defaults to the embedded dataset if offline.
📱 Platform Features
1. 📊 Executive Dashboard
Live KPI Counters: Total claims, approval rates, anomaly alerts, and land distribution.
Anomaly Engine: Auto-surfaces claims where satellite observation contradicts officer rejection notes.
Global Filter & Search: Real-time search across claimant names, PVTG tribes (Baiga, Bharia, Sahariya), districts, or seasonal badges (Kharif / Rabi / Zaid).
Automated AI Briefs: Generates official DLRC Memorandums, Spatial Cross-Examinations, and Officer Bias Audits in one click.
2. 🛰️ ISRO Bhuvan GIS Verification
220 Interactive Coordinates: Plotted pins categorized by Farmland, Forest, Verified, and Disputed claims.
Dynamic 1-Ha Season Overlays: Polygon boundary visuals shift based on selected month/year to reflect seasonal vegetation dynamics:
Kharif (Monsoon): Active crop canopy.
Rabi (Winter): Harvest canopy.
Zaid (Summer): Dry ploughed fallow soil.
NDVI Time-Series Canvas: Visualizes 2019–2024 vegetation index curves to legally establish continuous land cultivation prior to statutory cut-offs.
3. 🤖 Multi-Agent SDLC Hearing Debate
Simulates a Sub-Divisional Level Committee hearing using four specialized AI personas that debate claim validity:
Legal Counsel (Arjun Mehta): Cites FRA 2006 sections and Rule 12A.
Range Forest Officer (Priya Sharma): Scrutinizes compartment boundaries and potential forest encroachment.
Tribal Welfare Officer (Sunita Patel): Validates Gram Sabha resolutions and historical community evidence.
SDM / SDLC Chair (Vikram Rathore): Evaluates all arguments to render a final consensus ruling.
4. 📡 Field Scan Request
Portal for field officers to enter custom GPS coordinates, trigger the spatial boundary algorithm, evaluate forest reserve proximity, and push new records to MongoDB Atlas.
🛠️ Tech Stack
Frontend: Vanilla JavaScript (ES6+), HTML5, CSS3, Leaflet.js, Canvas API (Zero React, Node, or npm dependencies).
Backend: Python 3.10+, FastAPI, Uvicorn, PyMongo, Pydantic.
Database: MongoDB Atlas (M0 Cloud / Local fallback).
💻 Quick Start
1. Backend Setup
Bash
cd fra-guardian/backend
pip install fastapi uvicorn pymongo python-dotenv httpx
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
2. Build & Launch Frontend
Bash
cd fra-guardian
python3 build_unified_index.py
python3 -m http.server 8088
Access the application at http://localhost:8088/index.html.
(Optional) Configure MongoDB connectivity in backend/.env using MONGODB_URI and DATABASE_NAME.
📊 Dataset Overview (Madhya Pradesh Pilot)
Metric	Detail
Total Pilot Claims	220 claims across 19 Districts & 32 Forest Reserves
Status Split	Approved: 61 (27.7%) | Rejected: 127 (57.7%) | Pending: 32 (14.5%)
Land Distribution	Farmland: 135 (61.4%) | Forest: 85 (38.6%)
Flagged Anomalies	159 claims (72.3%)
Tribes Covered	Baiga (PVTG), Bharia (PVTG), Sahariya (PVTG), Gond, Bhil, Korku, Kol, and others
⚠️ Known Limitations & Future Roadmap
Live Bhuvan API Access: Current NDVI curves utilize published NRSC phenological models due to restricted public access to raw pixel-level satellite APIs. Direct OGC/WMS integration is planned for phase two.
LLM Engine Upgrade: Multi-agent debates currently use structured evidentiary scripts; future releases will integrate live Gemini/Groq LLM pipelines.
Mobile Field App: Planned lightweight mobile application with offline GPS capability and document OCR for field officers.
Built to demonstrate how spatial data, transparent AI reasoning, and open legal frameworks can accelerate justice under the Forest Rights Act, 2006.
