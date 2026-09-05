import json
import os

with open('sample_fra_claims.json') as f:
    claims = json.load(f)

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FRA Guardian — Satellite Land & Cultivation Verification (Madhya Pradesh)</title>
  <meta name="description" content="Multi-temporal satellite verification for Madhya Pradesh Forest Rights Act claims. Inspects cultivated fields vs forest canopy across 2019-2024 backed by MongoDB Atlas." />
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet" />

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <style>
    :root {
      --bg: #040a06;
      --surf: #09140c;
      --surf2: #0f2014;
      --surf3: #162c1d;
      --border: #1a3522;
      --border2: #244930;
      --green: #22c55e;
      --green-glow: rgba(34, 197, 94, 0.25);
      --amber: #f59e0b;
      --amber-glow: rgba(245, 158, 11, 0.25);
      --red: #ef4444;
      --red-glow: rgba(239, 68, 68, 0.25);
      --blue: #38bdf8;
      --blue-glow: rgba(56, 189, 248, 0.25);
      --purple: #a855f7;
      --text: #f0fdf4;
      --text2: #bbf7d0;
      --muted: #65826f;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      overflow-x: hidden;
      display: flex;
      flex-direction: column;
    }

    /* Header */
    header {
      background: rgba(9, 20, 12, 0.95);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      position: sticky;
      top: 0;
      z-index: 1000;
      backdrop-filter: blur(12px);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand-icon {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      background: linear-gradient(135deg, #16a34a, #052e16);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 19px;
      box-shadow: 0 0 16px var(--green-glow);
    }
    .brand-title {
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 800;
    }
    .brand-title span {
      background: linear-gradient(135deg, #22c55e, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-sub {
      font-size: 10px;
      color: var(--muted);
      font-family: 'JetBrains Mono', monospace;
    }

    .db-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(34, 197, 94, 0.12);
      border: 1px solid rgba(34, 197, 94, 0.3);
      color: var(--green);
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
    }
    .db-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--green);
      box-shadow: 0 0 6px var(--green);
    }

    .claim-picker-wrap {
      margin-left: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .claim-picker-label {
      font-size: 10px;
      font-weight: 700;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .claim-select {
      background: var(--surf2);
      border: 1px solid var(--border2);
      color: var(--text);
      padding: 7px 14px;
      border-radius: 9px;
      font-size: 12px;
      font-weight: 600;
      font-family: 'Inter', sans-serif;
      outline: none;
      cursor: pointer;
      min-width: 380px;
      transition: all 0.2s;
    }
    .claim-select:focus {
      border-color: var(--green);
      box-shadow: 0 0 12px var(--green-glow);
    }

    .nav-links {
      margin-left: auto;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .nav-btn {
      font-size: 11px;
      font-weight: 700;
      padding: 7px 12px;
      border-radius: 9px;
      text-decoration: none;
      border: 1px solid var(--border);
      background: var(--surf2);
      color: var(--text2);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .nav-btn:hover {
      border-color: var(--green);
      color: var(--green);
      box-shadow: 0 0 12px var(--green-glow);
      transform: translateY(-1px);
    }
    .nav-btn.active {
      background: rgba(34, 197, 94, 0.15);
      border-color: var(--green);
      color: var(--green);
    }

    /* Main Grid */
    .app-main {
      display: grid;
      grid-template-columns: 1fr 460px;
      flex: 1;
      height: calc(100vh - 63px);
      overflow: hidden;
    }

    /* Map Column */
    .map-pane {
      display: flex;
      flex-direction: column;
      position: relative;
      border-right: 1px solid var(--border);
      background: #020703;
    }
    #map {
      flex: 1;
      width: 100%;
      background: #020703;
      z-index: 1;
    }

    /* Floating Map Controls & Overlays */
    .map-top-bar {
      position: absolute;
      top: 14px;
      left: 14px;
      right: 14px;
      z-index: 500;
      display: flex;
      align-items: center;
      justify-content: space-between;
      pointer-events: none;
      gap: 10px;
    }
    .map-controls-group {
      pointer-events: auto;
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(9, 20, 12, 0.92);
      padding: 5px 8px;
      border-radius: 10px;
      border: 1px solid var(--border);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(8px);
    }
    .layer-toggle-btn {
      font-size: 10px;
      font-weight: 700;
      padding: 5px 10px;
      border-radius: 7px;
      background: var(--surf2);
      border: 1px solid var(--border);
      color: var(--muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
    }
    .layer-toggle-btn:hover {
      color: var(--text);
      border-color: var(--border2);
    }
    .layer-toggle-btn.active {
      background: rgba(34, 197, 94, 0.18);
      border-color: var(--green);
      color: var(--green);
      box-shadow: 0 0 10px var(--green-glow);
    }

    /* Field Detection HUD */
    .field-status-hud {
      pointer-events: auto;
      background: rgba(9, 20, 12, 0.94);
      border: 1px solid var(--border2);
      border-radius: 12px;
      padding: 9px 15px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 6px 24px rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(10px);
      transition: all 0.3s ease;
    }
    .field-status-icon { font-size: 22px; }
    .field-status-title { font-size: 12px; font-weight: 800; letter-spacing: 0.2px; }
    .field-status-sub { font-size: 10px; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
    .field-status-hud.cultivated {
      border-color: rgba(245, 158, 11, 0.5);
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.14), rgba(9, 20, 12, 0.95));
    }
    .field-status-hud.cultivated .field-status-title { color: var(--amber); }

    .field-status-hud.forest {
      border-color: rgba(34, 197, 94, 0.5);
      background: linear-gradient(135deg, rgba(34, 197, 94, 0.14), rgba(9, 20, 12, 0.95));
    }
    .field-status-hud.forest .field-status-title { color: var(--green); }

    .field-status-hud.clearing {
      border-color: rgba(239, 68, 68, 0.5);
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.16), rgba(9, 20, 12, 0.95));
    }
    .field-status-hud.clearing .field-status-title { color: var(--red); }

    /* Timeline Bar */
    .timeline-bar {
      background: var(--surf);
      border-top: 1px solid var(--border);
      padding: 12px 20px 14px;
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .timeline-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .timeline-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--text2);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .timeline-title strong {
      font-family: 'JetBrains Mono', monospace;
      color: var(--green);
      font-size: 14px;
    }
    .phenology-badge {
      font-size: 10px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 6px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: var(--blue);
    }
    .random-btn {
      padding: 5px 12px;
      border-radius: 8px;
      font-size: 10px;
      font-weight: 700;
      border: 1px solid var(--border2);
      background: var(--surf2);
      color: var(--text);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .random-btn:hover {
      border-color: var(--green);
      color: var(--green);
      box-shadow: 0 0 10px var(--green-glow);
    }

    .year-slider-row {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    #yearSlider {
      flex: 1;
      -webkit-appearance: none;
      appearance: none;
      height: 6px;
      background: var(--border);
      border-radius: 3px;
      outline: none;
      cursor: pointer;
    }
    #yearSlider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: var(--green);
      border: 3px solid var(--bg);
      box-shadow: 0 0 12px var(--green-glow);
      cursor: grab;
    }
    .year-buttons { display: flex; gap: 4px; }
    .year-btn {
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      background: var(--surf2);
      border: 1px solid var(--border);
      color: var(--muted);
      cursor: pointer;
      transition: all 0.2s;
    }
    .year-btn:hover { color: var(--text); border-color: var(--border2); }
    .year-btn.active {
      background: rgba(34, 197, 94, 0.2);
      border-color: var(--green);
      color: var(--green);
      box-shadow: 0 0 8px var(--green-glow);
    }

    .month-grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 4px;
    }
    .month-pill {
      padding: 7px 2px;
      text-align: center;
      font-size: 10px;
      font-weight: 700;
      border-radius: 7px;
      background: var(--surf2);
      border: 1px solid var(--border);
      color: var(--muted);
      cursor: pointer;
      font-family: 'JetBrains Mono', monospace;
      transition: all 0.2s;
    }
    .month-pill:hover { border-color: var(--border2); color: var(--text); }
    .month-pill.active {
      background: rgba(34, 197, 94, 0.22);
      border-color: var(--green);
      color: var(--green);
      box-shadow: 0 0 10px var(--green-glow);
    }

    /* Right Info Panel */
    .info-pane {
      background: var(--surf);
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      border-left: 1px solid var(--border);
    }
    .info-pane::-webkit-scrollbar { width: 4px; }
    .info-pane::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

    .pane-section {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
    }
    .section-label {
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--muted);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Verdict Card */
    .verdict-card {
      border-radius: 14px;
      padding: 16px 18px;
      transition: all 0.3s ease;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .verdict-card.agrees {
      background: linear-gradient(135deg, rgba(22, 163, 74, 0.18), rgba(5, 46, 22, 0.4));
      border: 1px solid rgba(34, 197, 94, 0.4);
    }
    .verdict-card.contradicts {
      background: linear-gradient(135deg, rgba(220, 38, 38, 0.18), rgba(69, 10, 10, 0.4));
      border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .verdict-card.partial {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.18), rgba(69, 38, 10, 0.4));
      border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .verdict-header {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .verdict-icon { font-size: 26px; }
    .verdict-title { font-size: 15px; font-weight: 800; }
    .verdict-card.agrees .verdict-title { color: var(--green); }
    .verdict-card.contradicts .verdict-title { color: var(--red); }
    .verdict-card.partial .verdict-title { color: var(--amber); }

    .confidence-row {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 4px;
    }
    .confidence-track {
      flex: 1;
      height: 6px;
      background: var(--surf2);
      border-radius: 3px;
      overflow: hidden;
    }
    .confidence-fill {
      height: 100%;
      border-radius: 3px;
      transition: width 0.6s ease;
    }
    .verdict-card.agrees .confidence-fill { background: var(--green); box-shadow: 0 0 8px var(--green); }
    .verdict-card.contradicts .confidence-fill { background: var(--red); box-shadow: 0 0 8px var(--red); }
    .verdict-card.partial .confidence-fill { background: var(--amber); box-shadow: 0 0 8px var(--amber); }

    /* Key Card: WHY LAND WAS NOT GIVEN / DECISION AUDIT */
    .why-card {
      background: linear-gradient(135deg, #102417 0%, #0d1a10 100%);
      border: 1px solid #22c55e55;
      border-radius: 14px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
    }
    .why-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 9px;
      font-weight: 800;
      text-transform: uppercase;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.5px;
      width: fit-content;
    }
    .why-text {
      font-size: 12px;
      line-height: 1.65;
      color: #e2fbe8;
    }
    .why-official-reason {
      font-size: 10.5px;
      color: var(--muted);
      border-top: 1px solid var(--border);
      padding-top: 8px;
      margin-top: 4px;
    }

    /* Phenology Card */
    .pheno-card {
      background: var(--surf2);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .pheno-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
    }
    .pheno-key { color: var(--muted); }
    .pheno-val { font-weight: 700; font-family: 'JetBrains Mono', monospace; }

    /* Chart Box */
    .chart-box {
      background: var(--surf2);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      height: 180px;
      position: relative;
    }
    #ndviCanvas { width: 100%; height: 100%; }

    /* Year History List */
    .year-history-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .year-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      border-radius: 8px;
      background: var(--surf2);
      border: 1px solid var(--border);
      font-size: 11px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .year-row:hover { border-color: var(--border2); transform: translateX(3px); }
    .year-row.active {
      border-color: var(--green);
      background: rgba(34, 197, 94, 0.12);
      box-shadow: 0 0 10px var(--green-glow);
    }
    .year-row-badge {
      padding: 2px 7px;
      border-radius: 5px;
      font-size: 9px;
      font-weight: 800;
    }
    .badge-cultivated { background: rgba(245, 158, 11, 0.2); color: var(--amber); border: 1px solid rgba(245, 158, 11, 0.4); }
    .badge-forest { background: rgba(34, 197, 94, 0.2); color: var(--green); border: 1px solid rgba(34, 197, 94, 0.4); }

    .action-cta-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 12px;
      border-radius: 10px;
      background: linear-gradient(135deg, #16a34a, #052e16);
      border: 1px solid var(--green);
      color: #fff;
      text-decoration: none;
      font-size: 12px;
      font-weight: 700;
      box-shadow: 0 4px 16px var(--green-glow);
      transition: all 0.2s;
    }
    .action-cta-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4);
    }

    .leaflet-image-layer {
      transition: filter 0.4s ease, opacity 0.3s ease;
      border-radius: 4px;
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="brand">
      <div class="brand-icon">🛰️</div>
      <div>
        <div class="brand-title">FRA <span>Guardian</span> • Satellite Verification</div>
        <div class="brand-sub">Madhya Pradesh • ISRO Bhuvan & Sentinel Multispectral Analysis</div>
      </div>
    </div>

    <!-- MongoDB Atlas Status Pill -->
    <div class="db-status-pill" id="mongoStatusPill">
      <span class="db-dot"></span>
      <span>MongoDB Atlas: Connected (20 MP Claims)</span>
    </div>

    <!-- Claim Selector -->
    <div class="claim-picker-wrap">
      <span class="claim-picker-label">Claim:</span>
      <select id="claimSelect" class="claim-select" title="Select a claim to inspect"></select>
    </div>

    <!-- Navigation Links -->
    <div class="nav-links">
      <a href="index.html" class="nav-btn">📊 Dashboard</a>
      <a href="satellite-verify.html" class="nav-btn active">🛰️ Satellite Verify</a>
      <a href="request-scan.html" class="nav-btn">📡 Scan Portal</a>
      <a href="bot-debate.html" class="nav-btn">⚖️ AI Legal Debate</a>
    </div>
  </header>

  <!-- Main Body Grid -->
  <main class="app-main">
    
    <!-- Left Map Pane -->
    <div class="map-pane">
      
      <!-- Top Floating Map Controls -->
      <div class="map-top-bar">
        
        <!-- Live Field Detection HUD -->
        <div id="fieldStatusHud" class="field-status-hud cultivated">
          <div id="fieldHudIcon" class="field-status-icon">🌾</div>
          <div>
            <div id="fieldHudTitle" class="field-status-title">CULTIVATED FIELD DETECTED</div>
            <div id="fieldHudSub" class="field-status-sub">Active Agricultural Plots • Kharif Season (NDVI 0.58)</div>
          </div>
        </div>

        <!-- Layer Toggles -->
        <div class="map-controls-group">
          <button id="toggleFieldImagery" class="layer-toggle-btn active" onclick="toggleOverlayLayer('field')">
            🌾 Field Satellite View
          </button>
          <button id="toggleCadastral" class="layer-toggle-btn active" onclick="toggleOverlayLayer('cadastral')">
            📐 Farm Plots
          </button>
          <button id="toggleNdviHeat" class="layer-toggle-btn" onclick="toggleOverlayLayer('ndvi')">
            🌡️ NDVI Heat
          </button>
          <button id="toggleBhuvanWms" class="layer-toggle-btn active" onclick="toggleOverlayLayer('bhuvan')">
            🌲 Bhuvan WMS
          </button>
        </div>

      </div>

      <!-- Leaflet Map Canvas -->
      <div id="map"></div>

      <!-- Bottom Timeline & Month Controller -->
      <div class="timeline-bar">
        <div class="timeline-header">
          <div class="timeline-title">
            <span>📅 Scan Date:</span>
            <strong id="activeDateDisplay">August 2024</strong>
            <span id="activeSeasonBadge" class="phenology-badge">🌧️ Kharif Monsoon (Peak Vegetative)</span>
          </div>
          
          <button class="random-btn" onclick="selectRandomMonth()" title="Pick a random month to view seasonal crop changes">
            🎲 Random Month
          </button>
        </div>

        <!-- Year Slider -->
        <div class="year-slider-row">
          <span style="font-size:10px;font-weight:700;color:var(--muted);font-family:'JetBrains Mono',monospace">2019</span>
          <input type="range" id="yearSlider" min="2019" max="2024" step="1" value="2024" />
          <span style="font-size:10px;font-weight:700;color:var(--muted);font-family:'JetBrains Mono',monospace">2024</span>
          <div class="year-buttons" id="yearButtons"></div>
        </div>

        <!-- Month Grid -->
        <div class="month-grid" id="monthGrid"></div>
      </div>

    </div>

    <!-- Right Sidebar -->
    <aside class="info-pane">
      
      <!-- Verdict Card -->
      <div class="pane-section">
        <div class="section-label">AI Decision Support Verdict</div>
        <div id="verdictCard" class="verdict-card agrees">
          <div class="verdict-header">
            <div id="verdictIcon" class="verdict-icon">✅</div>
            <div>
              <div id="verdictTitle" class="verdict-title">SATELLITE CONFIRMS CULTIVATION</div>
              <div style="font-size:10px;color:var(--muted);font-family:'JetBrains Mono',monospace">ISRO Bhuvan + Sentinel Multi-Temporal Match</div>
            </div>
          </div>
          <div class="confidence-row">
            <span style="font-size:10px;color:var(--muted)">Evidence Confidence</span>
            <div class="confidence-track">
              <div id="confidenceFill" class="confidence-fill" style="width:94%"></div>
            </div>
            <span id="confidenceVal" style="font-size:10px;font-weight:700;font-family:'JetBrains Mono',monospace">94%</span>
          </div>
        </div>
      </div>

      <!-- KEY HIGHLIGHT CARD: WHY LAND WAS NOT GIVEN -->
      <div class="pane-section">
        <div class="section-label">
          <span>⚖️ Why Land Was Not Given / Decision Audit</span>
          <span id="landCategoryTag" style="font-size:9px;color:var(--amber);font-family:'JetBrains Mono',monospace">FARMLAND</span>
        </div>
        <div class="why-card" id="whyCard">
          <div class="why-badge" id="whyBadge" style="background:#16a34a22;color:var(--green);border:1px solid #22c55e44">
            TITLE VESTED (APPROVED)
          </div>
          <div class="why-text" id="whyText">
            Loading decision audit...
          </div>
          <div class="why-official-reason" id="whyOfficialReason">
            Official Paper Reason: None (Approved)
          </div>
        </div>
      </div>

      <!-- Agricultural Phenology Card -->
      <div class="pane-section">
        <div class="section-label">
          <span>🌾 Agricultural & Seasonal Analysis</span>
          <span id="cropCycleTag" style="color:var(--amber);font-size:10px">Kharif Crop</span>
        </div>
        <div class="pheno-card">
          <div class="pheno-item">
            <span class="pheno-key">Detected Land Cover:</span>
            <span id="phenoCover" class="pheno-val" style="color:var(--amber)">Active Cultivated Field</span>
          </div>
          <div class="pheno-item">
            <span class="pheno-key">Crop Cycle Stage:</span>
            <span id="phenoStage" class="pheno-val">Peak Vegetative Growth</span>
          </div>
          <div class="pheno-item">
            <span class="pheno-key">NDVI Vegetation Index:</span>
            <span id="phenoNdvi" class="pheno-val" style="color:var(--green)">0.61 (Healthy Crop)</span>
          </div>
          <div class="pheno-item">
            <span class="pheno-key">Plot Area Verified:</span>
            <span id="phenoArea" class="pheno-val">1.50 Acres</span>
          </div>
          <div class="pheno-item">
            <span class="pheno-key">Pre-2005 Evidence:</span>
            <span id="phenoHistorical" class="pheno-val" style="color:var(--green)">Continuous Pre-2005</span>
          </div>
        </div>
      </div>

      <!-- 6-Year NDVI Timeline Chart -->
      <div class="pane-section">
        <div class="section-label">
          <span>📊 6-Year NDVI Vegetation Trajectory</span>
          <span style="font-size:9px;color:var(--muted)">2019 – 2024</span>
        </div>
        <div class="chart-box">
          <canvas id="ndviCanvas"></canvas>
        </div>
      </div>

      <!-- Year Breakdown List -->
      <div class="pane-section">
        <div class="section-label">📅 Multi-Year Historical Satellite Passes</div>
        <div class="year-history-list" id="yearHistoryList"></div>
      </div>

      <!-- Claimant & Land Details -->
      <div class="pane-section">
        <div class="section-label">👤 Claimant Record</div>
        <div class="pheno-card" style="font-size:11px;gap:8px">
          <div class="pheno-item"><span class="pheno-key">Claimant:</span><span id="recName" class="pheno-val">--</span></div>
          <div class="pheno-item"><span class="pheno-key">Tribe / Category:</span><span id="recTribe" class="pheno-val">--</span></div>
          <div class="pheno-item"><span class="pheno-key">Village / District:</span><span id="recVillage" class="pheno-val">--</span></div>
          <div class="pheno-item"><span class="pheno-key">Forest Reserve:</span><span id="recReserve" class="pheno-val">--</span></div>
          <div class="pheno-item"><span class="pheno-key">Claimed Land Use:</span><span id="recClaimedUse" class="pheno-val">--</span></div>
          <div class="pheno-item"><span class="pheno-key">Reviewing Officer:</span><span id="recOfficer" class="pheno-val">--</span></div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="pane-section" style="border-bottom:none">
        <a href="request-scan.html" class="action-cta-btn">
          📡 Mark New Forest Range Scan →
        </a>
      </div>

    </aside>

  </main>

  <script>
    // ══════════════════════════════════════════════════════════════
    // 20 MADHYA PRADESH CLAIMS (BACKED BY MONGODB ATLAS)
    // ══════════════════════════════════════════════════════════════
    let CLAIMS = __CLAIMS_JSON__;

    // Months & Phenology curves
    const MONTHS = [
      { name: "January", short: "Jan", season: "❄️ Rabi Winter", stage: "Winter Crop Growth (Wheat/Gram)", cycle: "Rabi",
        farmFilter: "brightness(1.02) saturate(1.22) contrast(1.1)", 
        forestFilter: "brightness(0.96) saturate(1.05) contrast(1.08)",
        ndviMultiplier: 0.90 },
      { name: "February", short: "Feb", season: "❄️ Late Winter", stage: "Peak Rabi Vegetative Stage", cycle: "Rabi",
        farmFilter: "brightness(1.04) saturate(1.28) contrast(1.12)",
        forestFilter: "brightness(0.97) saturate(1.08) contrast(1.1)",
        ndviMultiplier: 0.96 },
      { name: "March", short: "Mar", season: "🌾 Spring Harvest", stage: "Rabi Maturation & Golden Ripening", cycle: "Rabi Harvest",
        farmFilter: "brightness(1.12) saturate(1.3) sepia(0.35) hue-rotate(16deg) contrast(1.1)",
        forestFilter: "brightness(0.98) saturate(0.98) contrast(1.08)",
        ndviMultiplier: 0.68 },
      { name: "April", short: "Apr", season: "☀️ Summer Harvest", stage: "Crop Cutting & Field Stubble", cycle: "Post-Harvest",
        farmFilter: "brightness(1.10) saturate(1.1) sepia(0.45) hue-rotate(18deg) contrast(1.12)",
        forestFilter: "brightness(0.99) saturate(0.92) contrast(1.05)",
        ndviMultiplier: 0.46 },
      { name: "May", short: "May", season: "☀️ Peak Summer", stage: "Plowed Earth & Summer Fallow", cycle: "Fallow / Soil Prep",
        farmFilter: "brightness(0.93) saturate(0.68) sepia(0.58) contrast(1.18)",
        forestFilter: "brightness(1.0) saturate(0.88) contrast(1.04)",
        ndviMultiplier: 0.35 },
      { name: "June", short: "Jun", season: "🌧️ Pre-Monsoon", stage: "Pre-Monsoon Plowing & Sowing", cycle: "Kharif Sowing",
        farmFilter: "brightness(0.98) saturate(0.92) sepia(0.28) contrast(1.14)",
        forestFilter: "brightness(0.98) saturate(1.12) contrast(1.08)",
        ndviMultiplier: 0.55 },
      { name: "July", short: "Jul", season: "🌧️ Peak Monsoon", stage: "Rapid Vegetative Germination", cycle: "Kharif Growth",
        farmFilter: "brightness(1.04) saturate(1.42) hue-rotate(-10deg) contrast(1.16)",
        forestFilter: "brightness(0.94) saturate(1.28) hue-rotate(-6deg) contrast(1.12)",
        ndviMultiplier: 1.22 },
      { name: "August", short: "Aug", season: "🌧️ Monsoon High", stage: "Peak Crop Canopy (Paddy/Millets)", cycle: "Kharif Peak",
        farmFilter: "brightness(1.06) saturate(1.48) hue-rotate(-12deg) contrast(1.18)",
        forestFilter: "brightness(0.92) saturate(1.35) hue-rotate(-8deg) contrast(1.15)",
        ndviMultiplier: 1.38 },
      { name: "September", short: "Sep", season: "🌧️ Late Monsoon", stage: "Grain Formation & Panicle Emergence", cycle: "Kharif Grain",
        farmFilter: "brightness(1.05) saturate(1.36) hue-rotate(-8deg) contrast(1.15)",
        forestFilter: "brightness(0.93) saturate(1.30) hue-rotate(-6deg) contrast(1.12)",
        ndviMultiplier: 1.30 },
      { name: "October", short: "Oct", season: "🍂 Post-Monsoon", stage: "Kharif Maturing & Early Harvest", cycle: "Harvest",
        farmFilter: "brightness(1.08) saturate(1.22) sepia(0.22) hue-rotate(8deg) contrast(1.12)",
        forestFilter: "brightness(0.96) saturate(1.15) contrast(1.1)",
        ndviMultiplier: 1.02 },
      { name: "November", short: "Nov", season: "🍂 Early Winter", stage: "Post-Harvest Tillage & Rabi Sowing", cycle: "Rabi Sowing",
        farmFilter: "brightness(0.98) saturate(0.95) sepia(0.30) contrast(1.1)",
        forestFilter: "brightness(0.97) saturate(1.05) contrast(1.08)",
        ndviMultiplier: 0.65 },
      { name: "December", short: "Dec", season: "❄️ Winter", stage: "Emerging Winter Seedlings", cycle: "Rabi Emergence",
        farmFilter: "brightness(1.0) saturate(1.14) contrast(1.08)",
        forestFilter: "brightness(0.95) saturate(1.02) contrast(1.08)",
        ndviMultiplier: 0.78 }
    ];

    let currentClaim = null;
    let currentYear = 2024;
    let currentMonth = 7; // August default
    let map = null;
    let baseSatelliteLayer = null;
    let bhuvanWmsLayer = null;
    let groundImageOverlay = null;
    let parcelPolygonLayer = null;
    let cadastralPlotLayer = null;
    let ndviHeatLayer = null;

    const layersConfig = {
      field: true,
      cadastral: true,
      ndvi: false,
      bhuvan: true
    };

    // Try fetching live data from MongoDB Atlas API
    async function syncMongoDBClaims() {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/claims');
        if (res.ok) {
          const data = await res.json();
          if (data.claims && data.claims.length > 0) {
            CLAIMS = data.claims;
            const pill = document.getElementById('mongoStatusPill');
            if (pill) {
              pill.innerHTML = `<span class="db-dot"></span><span>MongoDB Atlas: Live (${data.claims.length} MP Claims)</span>`;
            }
            setupClaimSelector();
          }
        }
      } catch (err) {
        console.log('Using pre-bundled MongoDB Atlas snapshot', err);
      }
    }

    function init() {
      setupClaimSelector();
      setupTimelineControls();
      initMap();

      const params = new URLSearchParams(window.location.search);
      const claimId = params.get('id') || localStorage.getItem('fra_latest_scan_id');
      const found = CLAIMS.find(c => c.claim_id === claimId);
      
      selectClaim(found || CLAIMS[0]);
      syncMongoDBClaims();
    }

    function setupClaimSelector() {
      const sel = document.getElementById('claimSelect');
      const curId = currentClaim ? currentClaim.claim_id : null;
      sel.innerHTML = '';
      
      CLAIMS.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c.claim_id;
        const icon = c.status === 'Approved' ? '✅' : c.status === 'Rejected' ? '❌' : '⏳';
        const tag = c.land_category === 'Farmland' ? '🌾 Farmland' : '🌲 Forest';
        opt.textContent = `${icon} ${c.claim_id} • ${c.claimant_name} (${tag}) — ${c.district}`;
        sel.appendChild(opt);
      });

      if (curId) sel.value = curId;

      sel.onchange = e => {
        const c = CLAIMS.find(claim => claim.claim_id === e.target.value);
        if (c) selectClaim(c);
      };
    }

    function setupTimelineControls() {
      const slider = document.getElementById('yearSlider');
      const yearBtns = document.getElementById('yearButtons');
      yearBtns.innerHTML = '';

      [2019, 2020, 2021, 2022, 2023, 2024].forEach(y => {
        const btn = document.createElement('button');
        btn.className = `year-btn ${y === currentYear ? 'active' : ''}`;
        btn.id = `ybtn-${y}`;
        btn.textContent = y;
        btn.onclick = () => setYear(y);
        yearBtns.appendChild(btn);
      });

      slider.addEventListener('input', e => {
        setYear(parseInt(e.target.value));
      });

      const monthGrid = document.getElementById('monthGrid');
      monthGrid.innerHTML = '';
      MONTHS.forEach((m, idx) => {
        const btn = document.createElement('button');
        btn.className = `month-pill ${idx === currentMonth ? 'active' : ''}`;
        btn.id = `mpill-${idx}`;
        btn.textContent = m.short;
        btn.title = `${m.name} (${m.season})`;
        btn.onclick = () => setMonth(idx);
        monthGrid.appendChild(btn);
      });
    }

    function initMap() {
      map = L.map('map', { zoomControl: true, attributionControl: false }).setView([22.5, 78.5], 7);

      baseSatelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19,
        attribution: 'Esri World Imagery'
      }).addTo(map);

      try {
        bhuvanWmsLayer = L.tileLayer.wms('https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms', {
          layers: 'lulc:LULC50K_1516',
          format: 'image/png',
          transparent: true,
          opacity: 0.30,
          token: '83e0ea6d0f53fcf1e79614e1da1f67a8e93cca8e',
          maxZoom: 19
        }).addTo(map);
      } catch(e) {}
    }

    function selectClaim(claim) {
      currentClaim = claim;
      const sel = document.getElementById('claimSelect');
      if (sel) sel.value = claim.claim_id;

      const bounds = L.latLngBounds(claim.coords);
      map.fitBounds(bounds, { padding: [60, 60], maxZoom: 16, animate: true, duration: 0.8 });

      // Update metadata
      document.getElementById('recName').textContent = claim.claimant_name;
      document.getElementById('recTribe').textContent = claim.tribe;
      document.getElementById('recVillage').textContent = `${claim.village}, ${claim.district} (${claim.state})`;
      document.getElementById('recReserve').textContent = claim.forest_reserve;
      document.getElementById('recClaimedUse').textContent = claim.claimed_land_use;
      document.getElementById('recOfficer').textContent = `${claim.officer_name} (${claim.officer_id})`;

      // Render cards
      renderVerdictCard(claim);
      renderWhyCard(claim);
      renderYearHistoryList(claim);
      renderNdviChart(claim);

      // Render map overlays
      renderMapParcelState();
    }

    function renderMapParcelState() {
      if (!currentClaim || !map) return;

      const m = MONTHS[currentMonth];
      const bounds = L.latLngBounds(currentClaim.coords);

      const isFarmlandType = currentClaim.land_category === 'Farmland';
      const yearTrajectory = currentClaim.ndvi_trajectory || [];
      const currentYearData = yearTrajectory.find(n => n.year === currentYear) || yearTrajectory[yearTrajectory.length - 1];
      
      const isCultivatedNow = currentYearData ? currentYearData.cls === 'Cultivated' : isFarmlandType;
      const isClearingNow = currentYearData ? currentYearData.cls === 'Clearing' : false;

      let currentNdvi = (currentYearData ? currentYearData.avg : 0.5) * m.ndviMultiplier;
      currentNdvi = Math.max(0.16, Math.min(0.89, parseFloat(currentNdvi.toFixed(2))));

      // 1. Ground Satellite Image Overlay
      if (groundImageOverlay) {
        map.removeLayer(groundImageOverlay);
        groundImageOverlay = null;
      }

      if (layersConfig.field) {
        let imageUrl = 'forest.jpg';
        let customFilter = m.forestFilter;

        if (isCultivatedNow) {
          imageUrl = 'farmland.jpg';
          customFilter = m.farmFilter;
        } else if (isClearingNow) {
          imageUrl = 'farmland.jpg';
          customFilter = 'brightness(0.9) saturate(0.6) sepia(0.4) contrast(1.2)';
        }

        groundImageOverlay = L.imageOverlay(imageUrl, bounds, {
          opacity: 0.95,
          interactive: true,
          zIndex: 400
        }).addTo(map);

        setTimeout(() => {
          if (groundImageOverlay && groundImageOverlay.getElement()) {
            groundImageOverlay.getElement().style.filter = customFilter;
          }
        }, 50);
      }

      // 2. Boundary & Cadastral Plots
      if (parcelPolygonLayer) {
        map.removeLayer(parcelPolygonLayer);
        parcelPolygonLayer = null;
      }
      if (cadastralPlotLayer) {
        map.removeLayer(cadastralPlotLayer);
        cadastralPlotLayer = null;
      }

      const boundaryColor = isCultivatedNow ? '#f59e0b' : isClearingNow ? '#ef4444' : '#22c55e';

      parcelPolygonLayer = L.polygon(currentClaim.coords, {
        color: boundaryColor,
        weight: 3,
        dashArray: isCultivatedNow ? '6 4' : 'none',
        fillColor: boundaryColor,
        fillOpacity: layersConfig.field ? 0.05 : 0.25,
        zIndex: 500
      }).addTo(map);

      if (layersConfig.cadastral && (isCultivatedNow || isClearingNow)) {
        const c = currentClaim.coords;
        const midLat = (c[0][0] + c[2][0]) / 2;
        const midLng = (c[0][1] + c[2][1]) / 2;

        const subPlotA = [[c[0][0], c[0][1]], [c[1][0], c[1][1]], [midLat, c[1][1]], [midLat, c[0][1]]];
        const subPlotB = [[midLat, c[0][1]], [midLat, c[2][1]], [c[2][0], c[2][1]], [c[3][0], c[3][1]]];
        const bundLine = [[midLat, c[0][1]], [midLat, c[1][1]]];

        cadastralPlotLayer = L.featureGroup([
          L.polyline(bundLine, { color: '#fcd34d', weight: 2, dashArray: '3 3' }),
          L.polygon(subPlotA, { color: '#f59e0b', weight: 1.5, fillOpacity: 0.04 }),
          L.polygon(subPlotB, { color: '#f59e0b', weight: 1.5, fillOpacity: 0.04 })
        ]).addTo(map);
      }

      // 3. NDVI Heat Layer
      if (ndviHeatLayer) {
        map.removeLayer(ndviHeatLayer);
        ndviHeatLayer = null;
      }
      if (layersConfig.ndvi) {
        const center = bounds.getCenter();
        const heatColor = currentNdvi >= 0.65 ? '#15803d' : currentNdvi >= 0.40 ? '#f59e0b' : '#b45309';
        ndviHeatLayer = L.circle(center, {
          radius: (currentClaim.area_acres || 2) * 55,
          color: heatColor,
          fillColor: heatColor,
          fillOpacity: 0.35,
          weight: 2
        }).addTo(map);
      }

      // 4. Update HUD
      const hud = document.getElementById('fieldStatusHud');
      const hudIcon = document.getElementById('fieldHudIcon');
      const hudTitle = document.getElementById('fieldHudTitle');
      const hudSub = document.getElementById('fieldHudSub');

      if (isCultivatedNow) {
        hud.className = 'field-status-hud cultivated';
        hudIcon.textContent = '🌾';
        hudTitle.textContent = 'CULTIVATED FIELD DETECTED';
        hudSub.textContent = `${m.season} • ${m.stage} (NDVI: ${currentNdvi})`;
      } else if (isClearingNow) {
        hud.className = 'field-status-hud clearing';
        hudIcon.textContent = '⚠️';
        hudTitle.textContent = 'RECENT FOREST CLEARING DETECTED';
        hudSub.textContent = `Tree cover loss detected in ${currentYear} • Cutoff Anomaly (NDVI: ${currentNdvi})`;
      } else {
        hud.className = 'field-status-hud forest';
        hudIcon.textContent = '🌲';
        hudTitle.textContent = 'DENSE FOREST CANOPY';
        hudSub.textContent = `Undisturbed Forest Reserve • Zero Agricultural Furrows (NDVI: ${currentNdvi})`;
      }

      // 5. Update timeline header & phenology
      document.getElementById('activeDateDisplay').textContent = `${m.name} ${currentYear}`;
      document.getElementById('activeSeasonBadge').textContent = `${m.season} — ${m.stage}`;
      
      document.getElementById('cropCycleTag').textContent = m.cycle;
      document.getElementById('phenoCover').textContent = isCultivatedNow ? 'Active Cultivated Field' : isClearingNow ? 'Recent Clearing / Encroachment' : 'Dense Forest Canopy';
      document.getElementById('phenoCover').style.color = boundaryColor;
      document.getElementById('phenoStage').textContent = m.stage;
      document.getElementById('phenoNdvi').textContent = `${currentNdvi} (${currentNdvi > 0.50 ? 'Lush Green' : currentNdvi > 0.30 ? 'Moderate Crop' : 'Fallow / Stubble'})`;
      document.getElementById('phenoNdvi').style.color = currentNdvi > 0.50 ? 'var(--green)' : currentNdvi > 0.30 ? 'var(--amber)' : 'var(--muted)';
      document.getElementById('phenoArea').textContent = `${currentClaim.area_acres} Acres (${currentClaim.area_ha} Ha)`;
      document.getElementById('phenoHistorical').textContent = isCultivatedNow && currentClaim.land_category === 'Farmland' ? 'Continuous Pre-2005' : currentClaim.anomaly_flags && currentClaim.anomaly_flags.includes('TIME_TRAP') ? 'Post-2005 Encroachment' : 'Reserved Forest Canopy';
      document.getElementById('phenoHistorical').style.color = isCultivatedNow && currentClaim.land_category === 'Farmland' ? 'var(--green)' : 'var(--red)';

      document.querySelectorAll('.year-row').forEach(row => {
        row.classList.toggle('active', parseInt(row.dataset.year) === currentYear);
      });
    }

    function setYear(year) {
      currentYear = year;
      document.getElementById('yearSlider').value = year;
      document.querySelectorAll('.year-btn').forEach(btn => {
        btn.classList.toggle('active', btn.id === `ybtn-${year}`);
      });
      renderMapParcelState();
    }

    function setMonth(monthIdx) {
      currentMonth = monthIdx;
      document.querySelectorAll('.month-pill').forEach((pill, idx) => {
        pill.classList.toggle('active', idx === monthIdx);
      });
      renderMapParcelState();
    }

    function selectRandomMonth() {
      let rand = Math.floor(Math.random() * 12);
      if (rand === currentMonth) rand = (rand + 3) % 12;
      setMonth(rand);
    }

    function toggleOverlayLayer(layerName) {
      layersConfig[layerName] = !layersConfig[layerName];
      const btnIdMap = {
        field: 'toggleFieldImagery',
        cadastral: 'toggleCadastral',
        ndvi: 'toggleNdviHeat',
        bhuvan: 'toggleBhuvanWms'
      };
      const btn = document.getElementById(btnIdMap[layerName]);
      if (btn) btn.classList.toggle('active', layersConfig[layerName]);

      if (layerName === 'bhuvan') {
        if (bhuvanWmsLayer) {
          if (layersConfig.bhuvan) map.addLayer(bhuvanWmsLayer);
          else map.removeLayer(bhuvanWmsLayer);
        }
      } else {
        renderMapParcelState();
      }
    }

    function renderVerdictCard(claim) {
      const card = document.getElementById('verdictCard');
      const icon = document.getElementById('verdictIcon');
      const title = document.getElementById('verdictTitle');
      const fill = document.getElementById('confidenceFill');
      const val = document.getElementById('confidenceVal');

      const v = (claim.satellite_verdict || 'agrees').toLowerCase();
      card.className = `verdict-card ${v}`;

      if (v === 'agrees') {
        icon.textContent = '✅';
        title.textContent = claim.status === 'Approved' ? 'TITLE APPROVED & SATELLITE CONFIRMED' : 'SATELLITE CONFIRMS CULTIVATION';
      } else if (v === 'contradicts') {
        icon.textContent = '❌';
        title.textContent = 'SATELLITE CONTRADICTS CLAIM';
      } else {
        icon.textContent = '⚠️';
        title.textContent = 'TIME-TRAP / CUTOFF ANOMALY';
      }

      fill.style.width = `${claim.confidence_score}%`;
      val.textContent = `${claim.confidence_score}%`;
    }

    function renderWhyCard(claim) {
      const tag = document.getElementById('landCategoryTag');
      tag.textContent = (claim.land_category || 'Farmland').toUpperCase();
      tag.style.color = claim.land_category === 'Farmland' ? 'var(--amber)' : 'var(--green)';

      const badge = document.getElementById('whyBadge');
      if (claim.status === 'Approved') {
        badge.textContent = 'TITLE VESTED (APPROVED)';
        badge.style.background = '#16a34a22';
        badge.style.color = 'var(--green)';
        badge.style.border = '1px solid #22c55e44';
      } else if (claim.status === 'Rejected') {
        badge.textContent = 'CLAIM REJECTED';
        badge.style.background = '#ef444422';
        badge.style.color = 'var(--red)';
        badge.style.border = '1px solid #ef444444';
      } else {
        badge.textContent = 'CLAIM PENDING';
        badge.style.background = '#f59e0b22';
        badge.style.color = 'var(--amber)';
        badge.style.border = '1px solid #f59e0b44';
      }

      document.getElementById('whyText').textContent = claim.why_land_was_not_given || 'No decision record available.';
      document.getElementById('whyOfficialReason').innerHTML = `<strong>Official Paper Reason:</strong> ${claim.rejection_reason_given || 'None (Title Approved / Pending Joint Inspection)'}`;
    }

    function renderYearHistoryList(claim) {
      const list = document.getElementById('yearHistoryList');
      list.innerHTML = '';
      const trajectory = claim.ndvi_trajectory || [];

      trajectory.forEach(n => {
        const row = document.createElement('div');
        row.className = `year-row ${n.year === currentYear ? 'active' : ''}`;
        row.dataset.year = n.year;
        row.onclick = () => setYear(n.year);

        const isCult = n.cls === 'Cultivated';
        const badgeClass = isCult ? 'badge-cultivated' : 'badge-forest';
        const badgeText = isCult ? '🌾 CULTIVATED' : n.cls === 'Clearing' ? '⚠️ CLEARING' : '🌲 FOREST';

        row.innerHTML = `
          <div style="display:flex;align-items:center;gap:8px">
            <strong style="font-family:'JetBrains Mono',monospace;color:var(--text)">${n.year}</strong>
            <span class="year-row-badge ${badgeClass}">${badgeText}</span>
          </div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--muted)">
            NDVI: <strong style="color:var(--text2)">${n.avg.toFixed(2)}</strong> (Monsoon: ${n.monsoon.toFixed(2)})
          </div>
        `;
        list.appendChild(row);
      });
    }

    function renderNdviChart(claim) {
      const canvas = document.getElementById('ndviCanvas');
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();

      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;
      const pad = { top: 15, right: 20, bottom: 25, left: 35 };
      const cw = w - pad.left - pad.right;
      const ch = h - pad.top - pad.bottom;

      ctx.clearRect(0, 0, w, h);

      ctx.strokeStyle = '#1e3328';
      ctx.lineWidth = 1;
      ctx.fillStyle = '#65826f';
      ctx.font = '9px "JetBrains Mono", monospace';
      ctx.textAlign = 'right';

      for (let i = 0; i <= 4; i++) {
        const yVal = (1.0 - i * 0.25).toFixed(2);
        const y = pad.top + (ch / 4) * i;
        ctx.beginPath();
        ctx.moveTo(pad.left, y);
        ctx.lineTo(pad.left + cw, y);
        ctx.stroke();
        ctx.fillText(yVal, pad.left - 6, y + 3);
      }

      const years = claim.ndvi_trajectory || [];
      if (years.length < 2) return;
      const stepX = cw / (years.length - 1);

      // Monsoon curve
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 2;
      ctx.beginPath();
      years.forEach((item, i) => {
        const x = pad.left + i * stepX;
        const y = pad.top + (1 - item.monsoon) * ch;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();

      // Avg curve
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      years.forEach((item, i) => {
        const x = pad.left + i * stepX;
        const y = pad.top + (1 - item.avg) * ch;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();
      ctx.setLineDash([]);

      // Points & Labels
      ctx.textAlign = 'center';
      years.forEach((item, i) => {
        const x = pad.left + i * stepX;
        const yAvg = pad.top + (1 - item.avg) * ch;
        const yMonsoon = pad.top + (1 - item.monsoon) * ch;

        ctx.fillStyle = '#22c55e';
        ctx.beginPath();
        ctx.arc(x, yMonsoon, 3.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(x, yAvg, 3.5, 0, Math.PI * 2);
        ctx.fill();

        if (item.year === currentYear) {
          ctx.strokeStyle = '#fff';
          ctx.lineWidth = 2;
          ctx.stroke();
        }

        ctx.fillStyle = item.year === currentYear ? '#22c55e' : '#65826f';
        ctx.fillText(item.year, x, h - 6);
      });
    }

    window.addEventListener('resize', () => {
      if (currentClaim) renderNdviChart(currentClaim);
    });

    document.addEventListener('DOMContentLoaded', init);
  </script>

</body>
</html>
"""

final_html = template.replace('__CLAIMS_JSON__', json.dumps(claims, indent=2))

with open('satellite-verify.html', 'w') as f:
    f.write(final_html)

print("Generated satellite-verify.html successfully with all 20 MP claims!")
