import os
import requests
from typing import Optional
from google.adk.agents import Agent
from .utils import map_main_region, map_subregion, KNOWN_SUBREGIONS

FASTAPI_URL = "https://azure-service-portal-health.onrender.com/api/v1/azure/service_health"

def load_prompt(filepath="prompts/azure_status_agent_instructions.txt") -> str:
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "r", encoding="utf-8") as file:
        return file.read()

azure_status_agent_instructions = load_prompt()

def fetch_health_data(main_region: str, subregion: Optional[str] = None):
    params = {"main_region": main_region.capitalize()}
    if subregion:
        params["subregion"] = subregion.replace("-", " ").title().replace(" ", "")
    try:
        response = requests.get(FASTAPI_URL, params=params, timeout=5)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def get_region_status(user_main_region: str, user_subregion: Optional[str] = None):
    main_region = map_main_region(user_main_region)
    if not main_region:
        return f"Invalid or unsupported main region '{user_main_region}'. Please provide a valid main region like Americas or Europe."

    subregion = map_subregion(user_subregion) if user_subregion else None
    if user_subregion and not subregion:
        return f"Invalid or unsupported subregion '{user_subregion}'. Please provide a valid subregion."

    response = fetch_health_data(main_region, subregion)
    if response.get("status") != "success":
        return f"No status data available for {subregion or main_region} from Azure Service Health API."

    data = response.get("data", {})
    incidents = data.get("data", [])

    if not subregion:
        if not incidents:
            result_lines = [f"Region: {main_region.capitalize()}", "Subregions:"]
            for sr in KNOWN_SUBREGIONS.get(main_region, []):
                result_lines.append(f"  - {sr.replace('-', ' ').title()}: Good")
            return "\n".join(result_lines)
        else:
            incident_subregions = {inc.get("subregion", "").lower() for inc in incidents}
            result_lines = [f"Region: {main_region.capitalize()}", "Subregions:"]
            for sr in KNOWN_SUBREGIONS.get(main_region, []):
                status = "Issue" if sr.lower() in incident_subregions else "Good"
                result_lines.append(f"  - {sr.replace('-', ' ').title()}: {status}")
            return "\n".join(result_lines)
    else:
        if not incidents:
            return f"Region: {main_region.capitalize()}\nSubregion: {subregion.replace('-', ' ').title()}\nStatus: Good"
        else:
            incident_subregions = {inc.get("subregion", "").lower() for inc in incidents}
            status = "Issue" if subregion.lower() in incident_subregions else "Good"
            return f"Region: {main_region.capitalize()}\nSubregion: {subregion.replace('-', ' ').title()}\nStatus: {status}"

root_agent = Agent(
    name="azure_service_health_agent",
    model="gemini-2.0-flash",
    instruction=azure_status_agent_instructions,
    description="Agent that retrieves Azure service health with user-friendly region/subregion matching.",
    tools=[get_region_status]
)
