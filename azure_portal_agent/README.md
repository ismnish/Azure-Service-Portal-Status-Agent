Azure Service Health API 🚀
The Azure status page provides you with a global view of the health of Azure services and regions, along with service availability.

A FastAPI service that fetches Azure Service Health incidents from Microsoft’s official status RSS feed and returns clean JSON.
Optionally, it adds AI-powered summaries using Google’s Generative AI (Gemini).

What this project does

Pulls real-time incidents from Azure’s public RSS feed.

Lets you filter by main region (e.g., Americas, Europe) and optional subregion (e.g., eastus2, uksouth).

Returns structured JSON: incident title, summary, link, published, and matched_subregion.

Adds an AI summary (ai_summary) when configured with a Google API key.

Provides interactive docs via Swagger UI at /docs.

Requirements

Python 3.11+

macOS/Linux/WSL (Windows works too; see activation notes below)

Internet access (to read Azure’s RSS feed)

Quick Start (one command)

If your repo includes the helper scripts:

chmod +x setup.sh test.sh
./setup.sh


Creates a virtual environment .venv

Installs dependencies

Starts the API at http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

If you don’t have the scripts, follow “Manual Setup” below.

Manual Setup

Create & activate a virtual environment

python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1


Install dependencies

pip install -r requirements.txt


(Optional) AI summaries – set your Google API key

Create a file named .env in the project root:

GOOGLE_API_KEY=your-google-api-key-here


If unset, the API still works; it will just return a default “All systems operational” style summary when there are no incidents.

Run the API

uvicorn app.main:app --reload


API: http://127.0.0.1:8000/

Swagger UI: http://127.0.0.1:8000/docs

Swagger UI (Interactive Docs)

Open:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc (alt docs): http://127.0.0.1:8000/redoc

From Swagger UI you can:

Explore endpoints

Click Try it out

Pass query params (main_region, subregion)

Execute and see live JSON responses

Endpoints
GET /

Simple welcome message and quick links.

GET /api/v1/azure/service_health

Fetch incidents for a region (and optional subregion).

Query parameters

main_region (required): e.g., Americas, Europe

subregion (optional): e.g., eastus2, westus2, uksouth

200 Response (example)

{
  "status": "success",
  "main_region": "Americas",
  "subregion_filter": "all",
  "incidents_found": 0,
  "data": [],
  "ai_summary": "✅ All systems operational. No incidents reported.",
  "timestamp": "2025-08-28T10:00:00.000Z"
}


When an incident is present (example)

{
  "status": "success",
  "main_region": "Europe",
  "subregion_filter": "uksouth",
  "incidents_found": 1,
  "data": [
    {
      "title": "SQL Database - UK South",
      "summary": "We are investigating connectivity issues impacting SQL Database in UK South.",
      "published": "Thu, 28 Aug 2025 08:45:00 GMT",
      "link": "https://status.azure.com/en-us/status/history/",
      "matched_subregion": "uksouth"
    }
  ],
  "ai_summary": "⚠️ Azure SQL Database in UK South is experiencing connectivity issues; mitigation in progress.",
  "timestamp": "2025-08-28T10:05:00.000Z"
}

Example requests (curl)

Americas (all subregions monitored):

curl "http://127.0.0.1:8000/api/v1/azure/service_health?main_region=Americas"


Americas (specific subregion):

curl "http://127.0.0.1:8000/api/v1/azure/service_health?main_region=Americas&subregion=eastus2"


Europe (all subregions monitored):

curl "http://127.0.0.1:8000/api/v1/azure/service_health?main_region=Europe"

Project structure
app/
 ├── __init__.py
 ├── main.py                     # FastAPI app + root route + router include
 ├── routers/
 │    ├── __init__.py
 │    └── status.py              # /api/v1/azure/service_health endpoint
 ├── schemas/
 │    ├── __init__.py
 │    └── status.py              # Pydantic models (response, enums)
 └── services/
      ├── __init__.py
      ├── status_service.py      # RSS parsing + filtering logic
      └── ai_service.py          # Optional Gemini summary
tests/
 └── test_status.py              # Basic tests for the endpoint
requirements.txt
setup.sh                         # Optional: create venv, install deps, run API
test.sh                          # Optional: activate venv and run pytest
.env                             # Optional: GOOGLE_API_KEY (not committed)

Running tests

If you have the helper script:

chmod +x test.sh
./test.sh


Or manually:

source .venv/bin/activate
python -m pytest -v

Notes & Tips

RSS feed source: Both Americas and Europe currently use the same Azure status feed URL and are filtered by subregion keywords in code.

Common subregions monitored by default:

Americas: eastus2, westus2, westus, southcentralus, canadacentral, canadaeast, mexicocentral

Europe: uksouth, ukwest

If you see “No operations defined in spec!” in Swagger:

Ensure app.include_router(status.router, prefix="/api/v1/azure", tags=["Azure Service Health"]) is present in app/main.py.

macOS/Linux permissions:

If ./setup.sh or ./test.sh says “permission denied”: chmod +x setup.sh test.sh

Windows venv activation:

PowerShell: .venv\Scripts\Activate.ps1

CMD: .venv\Scripts\activate.bat

