
from pathlib import Path

import pandas as pd
import pytest

from tennis_career.data import (
    _normalize_name,
    _parse_matches,
    _clean_matches
)


TEST_DATA = Path(__file__).parent / "test_data"


def _load_records(filename):
    """Read a sample JS file and extract its match records."""
    js_text = (TEST_DATA / filename).read_text(encoding="utf-8")
    return _parse_matches(js_text)


def test_player_names():
    """Check that different name formats work."""
    assert _normalize_name("serena williams") == "SerenaWilliams"
    assert _normalize_name("SerenaWilliams") == "SerenaWilliams"
    assert _normalize_name("Rafael Nadal") == "RafaelNadal"


def test_empty_name():
    """Check that an empty player name raises an error."""
    with pytest.raises(ValueError, match="player name"):
        _normalize_name("")


def test_female_js_parsing():
    """Check that female match records are extracted correctly."""
    records = _load_records("FemalePlayerCareer.js")

    assert len(records) == 3
    assert records[0][11] == "Anne Miller"
    assert records[0][16] == "19770119"


def test_male_js_parsing():
    """Check that male match records are extracted correctly."""
    records = _load_records("MalePlayerCareer.js")

    assert len(records) == 3
    assert records[0][11] == "Guillermo Platel"
    assert records[0][16] == "22.264202601"


def test_female_age_calculation():
    """Check the cleaned female DataFrame and age calculations."""
    records = _load_records("FemalePlayerCareer.js")
    matches = _clean_matches(records, pd.Timestamp("1981-09-26"))

    expected_columns = [
        "date", "tournament", "surface", "result",
        "opponent", "opponent_dob", "opponent_age",
        "player_age", "age_difference"
    ]

    assert matches.columns.tolist() == expected_columns
    assert len(matches) == 3

    assert matches.loc[0, "date"] == pd.Timestamp("1995-10-30")
    assert matches.loc[0, "tournament"] == "Canadian Open"
    assert matches.loc[0, "surface"] == "Carpet"
    assert matches.loc[0, "result"] == "L"
    assert matches.loc[0, "opponent"] == "Anne Miller"
    assert matches.loc[0, "opponent_dob"] == pd.Timestamp("1977-01-19")

    assert matches.loc[0, "player_age"] == pytest.approx(169 / 12)
    assert matches.loc[0, "opponent_age"] == pytest.approx(225 / 12)
    assert matches.loc[0, "age_difference"] == pytest.approx(-56 / 12)


def test_male_age_calculation():
    """Check the cleaned male DataFrame and age calculations."""
    records = _load_records("MalePlayerCareer.js")
    matches = _clean_matches(records, pd.Timestamp("1986-06-03"))

    expected_columns = [
        "date", "tournament", "surface", "result",
        "opponent", "opponent_dob", "opponent_age",
        "player_age", "age_difference"
    ]

    assert matches.columns.tolist() == expected_columns
    assert len(matches) == 3

    assert matches.loc[0, "date"] == pd.Timestamp("2001-09-10")
    assert matches.loc[0, "tournament"] == "Spain F10"
    assert matches.loc[0, "surface"] == "Hard"
    assert matches.loc[0, "result"] == "L"
    assert matches.loc[0, "opponent"] == "Guillermo Platel"
    assert pd.isna(matches.loc[0, "opponent_dob"])

    assert matches.loc[0, "player_age"] == pytest.approx(183 / 12)
    assert matches.loc[0, "opponent_age"] == pytest.approx(267 / 12)
    assert matches.loc[0, "age_difference"] == pytest.approx(-7)
