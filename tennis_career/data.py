from bs4 import BeautifulSoup
import json
import re

import pandas as pd
import requests

BASE_URL = "https://www.tennisabstract.com"


def _normalize_name(name):
    """Convert player names to Tennis Abstract filename format."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Please enter a player name.")

    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name.strip())
    return "".join(word.capitalize() for word in name.split())



def _get_matches(name):
    """Download the player's Career.js file."""
    url = f"{BASE_URL}/jsmatches/{name}Career.js"
    response = requests.get(url, timeout=15)

    if response.status_code == 404:
        raise ValueError(f"Player '{name}' was not found.")

    response.raise_for_status()
    return _parse_matches(response.text)


def _parse_matches(js_text):
    """Extract match records from the Career.js file."""
    found = re.search(r"\bvar\s+morematchmx\s*=\s*", js_text)

    if not found:
        raise ValueError("No match data was found in the Career.js file.")

    matches, _ = json.JSONDecoder().raw_decode(
        js_text[found.end():].lstrip()
    )
    return matches


def _completed_months(date, birthday):
    """Calculate completed age in months using the HW2 formula."""
    return ((date.year - birthday.year) * 12 + (date.month - birthday.month) - (date.day < birthday.day))


def _get_opponent_age(value, match_date):
    """Calculate opponent age from a birth date or an existing age."""
    value = str(value).strip()

    # Female records contain opponent dates of birth (YYYYMMDD).
    if len(value) == 8 and value.isdigit():
        birthday = pd.to_datetime(value, format="%Y%m%d", errors="coerce")
        return _completed_months(match_date, birthday) / 12

    # Male records already contain opponent ages.
    age = pd.to_numeric(value, errors="coerce")
    return (age * 12 // 1) / 12



def _clean_matches(records, birthday):
    """Create a DataFrame with the same age calculations as HW2."""

    # Convert records into a DataFrame and select necessary columns.
    data = pd.DataFrame(records)
    data = data.iloc[:, [0, 1, 2, 4, 11, 16]].copy()
    data.columns = ["date", "tournament", "surface", "result", "opponent", "opponent_dob"]

    # Convert match dates to datetime.
    data["date"] = pd.to_datetime(data["date"], format="%Y%m%d", errors="coerce")

    # Calculate opponent ages and preserve available DOBs.
    raw = data["opponent_dob"].copy()
    data["opponent_age"] = [_get_opponent_age(v, d) for v, d in zip(raw, data["date"])]
    
    data["opponent_dob"] = pd.to_datetime(raw.where(raw.astype(str).str.fullmatch(r"\d{8}")), format="%Y%m%d", errors="coerce")

    # Calculate the selected player's age using the HW2 method.
    data["player_age"] = [_completed_months(d, birthday) / 12 if pd.notna(d) else float("nan") for d in data["date"]]

    # Calculate age difference and remove incomplete observations.
    data["age_difference"] = data["player_age"] - data["opponent_age"]
    return data.dropna(subset=["player_age", "age_difference", "result"])


def _get_birthdate(name):
    """Find a player's birth date from Tennis Abstract ranking reports."""

    # Find the first year in the player's career records.
    records = _get_matches(name)
    first_year = min(int(row[0][:4]) for row in records)
    player = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)

    # Check ranking reports from the player's early career.
    for year in range(first_year + 2, first_year + 7):
        for report in ("rankingsByAgeWta", "rankingsByAge"):
            url = f"{BASE_URL}/reports/{report}{year}.html"
            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(" ", strip=True).replace("\xa0", " ")

            pattern = rf"{re.escape(player)}\s+[A-Z]{{3}}\s+(\d{{4}}-\d{{2}}-\d{{2}})"
            found = re.search(pattern, text, re.I)

            if found:
                return pd.to_datetime(found.group(1), format="%Y-%m-%d")

    raise ValueError(f"Could not find birth date for '{name}'.")





def get_career_matches(player_name):
    """Retrieve and clean a player's career match data."""
    name = _normalize_name(player_name)
    records = _get_matches(name)
    # birthday = _get_birthdate(name)
    birthday = _get_birthdate(name)
    data = _clean_matches(records, birthday)

    if data.empty:
        raise ValueError(f"No usable matches found for '{player_name}'.")

    return data
