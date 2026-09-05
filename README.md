# FRA Guardian

A full-stack prototype for managing and reviewing Forest Rights Act (FRA) land claims. The project combines a FastAPI backend, MongoDB integration, structured claim models, sample claim data, and a browser-based frontend.

---

## Overview

FRA Guardian is a prototype decision-support application designed around Forest Rights Act claim data.

The repository contains:

* A Python backend built with FastAPI.
* MongoDB connectivity for storing and retrieving claim records.
* Pydantic models for structured claim data.
* Sample FRA claim data.
* A frontend application with its own source structure.
* A generated standalone `index.html`.
* A Python script used to build or consolidate frontend assets and data.
* Deployment configuration through `vercel.json`.

The project is structured as an application prototype rather than a production-ready government system.

---



## Project Purpose

FRA Guardian is a technical prototype exploring how structured claim data, backend APIs, geospatial-style interfaces, and data visualisation can be combined into a single system for reviewing Forest Rights Act-related claims.

The current repository should be considered a prototype or demonstration project.

It should not be represented as:

* An official Government of India system.
* A production FRA claim-processing platform.
* A replacement for statutory or legal verification.
* A direct live connection to official satellite or government databases unless such integrations are independently configured and verified.

---
## Image Reference

<img width="1459" height="833" alt="Screenshot 2026-09-05 at 7 48 39 AM" src="https://github.com/user-attachments/assets/64fc92a2-8306-41dc-a4c0-c3d8feeea33e" />

<img width="1458" height="835" alt="Screenshot 2026-09-05 at 7 49 56 AM" src="https://github.com/user-attachments/assets/60a99915-51ea-46ff-b3e7-edfe5bcd190c" />

<img width="1459" height="832" alt="Screenshot 2026-09-05 at 7 50 38 AM" src="https://github.com/user-attachments/assets/626a7677-cd73-4a16-840a-c9a9182025e1" />
## Ai Discussion
<img width="1453" height="814" alt="Screenshot 2026-09-05 at 7 52 01 AM" src="https://github.com/user-attachments/assets/a7c0133b-3b51-4615-9802-b8f368baffdf" />


## Repository Structure

```text
FRA-Guardian-AI-Decision-Support-ISRO-Bhuvan-Satellite-Verification-System/
│
├── api/
│
├── backend/
│   ├── data/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── tsconfig.json
│
├── fra-guardian/
│
├── build_unified_index.py
├── generate_frontend.py
├── index.html
├── sample_fra_claims.json
├── requirements.txt
├── vercel.json
│
├── farmland.jpg
└── forest.jpg
```

---

## Development Notes

The repository currently contains multiple frontend-related components:

1. A source frontend under `frontend/`.
2. A generated standalone `index.html`.
3. Build scripts such as `build_unified_index.py`.
4. Additional frontend generation logic in `generate_frontend.py`.

When modifying the project, it is important to identify which frontend artifact is actually used by the deployment.

A recommended development workflow is:

```text
Modify source code
      ↓
Run backend locally
      ↓
Run/test frontend locally
      ↓
Update sample data if required
      ↓
Generate standalone build if required
      ↓
Test final deployment artifact
```

---

## Contributing

Contributions should focus on improving the actual application rather than adding unsupported claims.

Useful areas for contribution include:

* Backend API improvements.
* Database reliability.
* Frontend usability.
* Claim-data validation.
* Automated testing.
* Documentation.
* Deployment automation.
* Security improvements.

---

## Disclaimer

This repository is a software prototype created for experimentation and demonstration.

Any real-world implementation involving Forest Rights Act claims, land records, satellite imagery, government data, or tribal land rights must be independently validated with authorised data sources and the appropriate legal and administrative authorities.

The application should not be used as the sole basis for approving, rejecting, or modifying an official claim.


---

## Backend

The backend is implemented in Python and organised around three main components:

### `backend/main.py`

The main FastAPI application.

This file is responsible for exposing the backend application and handling API functionality.

### `backend/database.py`

Handles database-related functionality and MongoDB integration.

The project uses MongoDB as the persistence layer for claim records when a database connection is configured.

### `backend/models.py`

Contains structured data models used by the application.

Using Pydantic models allows incoming and outgoing claim data to follow a predictable structure.

### `backend/data/`

Contains data used by the backend.

---

## Frontend

The repository contains a separate frontend project under:

```text
frontend/
```

The frontend includes:

```text
frontend/
├── public/
├── src/
├── index.html
├── package.json
└── tsconfig.json
```

This indicates that the source frontend and the generated standalone frontend are maintained separately.

The root-level `index.html` appears to be a generated or consolidated frontend artifact intended for direct deployment or standalone execution.

---

## Data

The repository includes:

```text
sample_fra_claims.json
```

This file provides sample Forest Rights Act claim data used for demonstration, testing, or application seeding.

The data is intended to support the application's claim-management and review workflow.

The repository also includes image assets:

```text
farmland.jpg
forest.jpg
```

These assets are used by the application to visually represent land categories.

---

## Unified Frontend Build

The project includes:

```text
build_unified_index.py
```

This script is responsible for generating or consolidating the frontend into a unified output.

The generated output allows the frontend to be distributed as a standalone HTML application.

This approach is useful for demonstrations and deployments where serving a compiled frontend separately is unnecessary.

---

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* MongoDB / PyMongo
* Pydantic

### Frontend

The frontend is maintained as a separate project with:

* HTML
* JavaScript / TypeScript tooling
* A package-based frontend configuration

### Data and Deployment

* JSON-based sample data
* MongoDB for persistent storage
* Vercel deployment configuration

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/nilabhumeshsingh/FRA-Guardian-AI-Decision-Support-ISRO-Bhuvan-Satellite-Verification-System.git
```

```bash
cd FRA-Guardian-AI-Decision-Support-ISRO-Bhuvan-Satellite-Verification-System
```

---

## Backend Setup

Move into the backend directory:

```bash
cd backend
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI application:

```bash
uvicorn main:app --reload
```

The API should then be available locally through the configured Uvicorn server.

---

## MongoDB Configuration

The backend contains database integration for MongoDB.

Configure the required connection settings according to the environment variables and database configuration expected by:

```text
backend/database.py
```

Do not commit database credentials or connection strings to the repository.

A typical local configuration can use environment variables such as:

```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=fra_guardian
```

The exact configuration should match the database implementation in the project.

---

## Frontend Setup

Move into the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Use the scripts defined in `package.json` to run or build the frontend.

---

## Standalone Frontend

The repository also includes a root-level standalone:

```text
index.html
```

For local testing, it can be served with a simple HTTP server.

For example:

```bash
python3 -m http.server 8088
```

Then open:

```text
http://localhost:8088
```

---

## Rebuilding the Unified Frontend

The repository includes:

```bash
build_unified_index.py
```

Run the script from the project root:

```bash
python3 build_unified_index.py
```

This regenerates the unified frontend output according to the build logic implemented in the script.

---
## Current Limitations

The repository currently contains prototype-level application code and sample data.

Before production use, the following areas would require additional work:

* Authentication and role-based access control.
* Secure credential management.
* Input validation and security testing.
* Production database configuration.
* API documentation.
* Automated tests.
* Logging and monitoring.
* Error handling.
* Deployment configuration for backend and frontend services.
* Verification of all external data sources.
* Legal and administrative validation for real FRA workflows.

---

## Repository

GitHub:

https://github.com/nilabhumeshsingh/FRA-Guardian-AI-Decision-Support-ISRO-Bhuvan-Satellite-Verification-System
