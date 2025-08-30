from typing import Dict
from typing import Optional
MAIN_REGION_ALIASES = {
    "americas": ["america", "americas", "amerca", "americass", "america's"],
    "europe": ["europe", "europa", "eu", "eur", "europ"],
}

SUBREGION_ALIASES = {
    "us-east": ["useast", "us east", "us-east", "eastus", "east us"],
    "us-east-2": ["useast2", "us east 2", "us-east-2", "eastus2", "east us 2"],
    "us-west": ["uswest", "us west", "us-west", "westus", "west us"],
    "us-west-2": ["uswest2", "us west 2", "us-west-2", "westus2", "west us 2"],
    "canada-central": ["canadacentral", "canada central", "canadacent", "canada-cent"],
    "brazil-south": ["brazilsouth", "brazil south", "brazil-south"],
    "northern-europe": ["northerneurope", "northern europe", "north europe"],
    "western-europe": ["westerneurope", "western europe", "west europe"],
    "uk-south": ["uksouth", "uk south", "uk-south"],
    "france-central": ["francecentral", "france central"],
    "Mexico Central": ["mexicocentral", "mexico central"],
}

KNOWN_SUBREGIONS = {
    "americas": list(SUBREGION_ALIASES.keys())[:6],
    "europe": list(SUBREGION_ALIASES.keys())[6:],
}

def build_reverse_lookup(alias_map):
    lookup = {}
    for canonical, aliases in alias_map.items():
        lookup[canonical.lower()] = canonical
        for a in aliases:
            normalized = a.strip().replace(" ", "").lower()
            lookup[normalized] = canonical
    return lookup


MAIN_REGION_LOOKUP = build_reverse_lookup(MAIN_REGION_ALIASES)
SUBREGION_LOOKUP = build_reverse_lookup(SUBREGION_ALIASES)

def normalize_input(text: str) -> str:
    return text.strip().replace(" ", "").lower()

def map_main_region(user_input: str) -> Optional[str]:
    key = normalize_input(user_input)
    return MAIN_REGION_LOOKUP.get(key)


def map_subregion(user_input: str) -> str:
    return SUBREGION_LOOKUP.get(normalize_input(user_input))
