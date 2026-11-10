from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from tennis_career.data import _parse_matches, _clean_matches
from tennis_career.plot import _create_plot


def test_nadal_plot():
    """Check that Nadal's data produces a graph."""
    path = Path(__file__).parent / "test_data" / "MalePlayerCareer.js"
    records = _parse_matches(path.read_text(encoding="utf-8"))
    matches = _clean_matches(records, pd.Timestamp("1986-06-03"))

    fig, ax = _create_plot(matches, "Rafael Nadal")

    assert isinstance(fig, plt.Figure)
    assert sum(len(c.get_offsets()) for c in ax.collections) == 3

    plt.close(fig)


def test_serena_plot():
    """Check that Serena's data produces a graph."""
    path = Path(__file__).parent / "test_data" / "FemalePlayerCareer.js"
    records = _parse_matches(path.read_text(encoding="utf-8"))
    matches = _clean_matches(records, pd.Timestamp("1981-09-26"))

    fig, ax = _create_plot(matches, "Serena Williams")

    assert isinstance(fig, plt.Figure)
    assert sum(len(c.get_offsets()) for c in ax.collections) == 3

    plt.close(fig)


def test_plot_empty_data():
    """Check that empty match data raises an error."""
    empty = pd.DataFrame(
        columns=["player_age", "age_difference", "result"]
    )

    with pytest.raises(ValueError, match="No valid match ages"):
        _create_plot(empty, "Unknown Player")
