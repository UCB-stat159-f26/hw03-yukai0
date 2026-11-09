from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from tennis_career.data import _parse_matches, _clean_matches
from tennis_career.plot import plot_career_matches


def test_nadal_plot():
    """Check if Nadal's plot is correct"""
    path = Path(__file__).parent / "test_data" / "MalePlayerCareer.js"
    records = _parse_matches(path.read_text(encoding="utf-8"))
    matches = _clean_matches(records, pd.Timestamp("1986-06-03"))

    fig, ax = plot_career_matches(matches, "Rafael Nadal")

    assert "Rafael Nadal" in ax.get_title()
    assert len(ax.collections) == 2
    assert len(ax.collections[0].get_offsets()) == 1
    assert len(ax.collections[1].get_offsets()) == 2

    plt.close(fig)


def test_serena_plot():
    """Check if Williams's plot is correct"""
    path = Path(__file__).parent / "test_data" / "FemalePlayerCareer.js"
    records = _parse_matches(path.read_text(encoding="utf-8"))
    matches = _clean_matches(records, pd.Timestamp("1981-09-26"))

    fig, ax = plot_career_matches(matches, "Serena Williams")

    assert "Serena Williams" in ax.get_title()
    assert len(ax.collections) == 2
    assert len(ax.collections[0].get_offsets()) == 0
    assert len(ax.collections[1].get_offsets()) == 3

    plt.close(fig)

def test_plot_empty_data():
    """Check if plot empty data."""
    empty = pd.DataFrame(columns=["player_age", "age_difference", "result"])

    with pytest.raises(ValueError, match="No valid match ages"):
        plot_career_matches(empty)
