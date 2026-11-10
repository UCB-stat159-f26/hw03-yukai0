import matplotlib.pyplot as plt
import re
from .data import *

def _plot_points(ax, matches):
    wins = matches[matches["result"] == "W"]
    losses = matches[matches["result"] == "L"]

    # Plot wins
    ax.scatter(wins["player_age"], wins["age_difference"],
               s=18, alpha=0.8, color="#3fc1e8", label="Match won")

    # Plot losses
    ax.scatter(losses["player_age"], losses["age_difference"],
               s=18, alpha=0.8, color="#96358f", label="Match lost")

    # Same-age line
    ax.axhline(0, color="gray", linewidth=1)


def _format_axes(ax, matches):
    """Format the axes, grid, and borders as in HW2."""

    # Automatically determine the player's age range.
    start_age = int(matches["player_age"].min())
    end_age = int(matches["player_age"].max()) + 1

    # Axis limits and ticks
    ax.set_xlim(start_age - 0.5, end_age + 0.5)
    ax.set_ylim(-20, 22)
    ax.set_xticks(range(start_age + start_age % 2, end_age + 1, 2))
    ax.set_yticks([-20, -10, 0, 10, 20])
    ax.set_yticklabels(["−20", "−10", "Same age", "+10", "+20 years"])

    # Put x-axis labels on top
    ax.tick_params(axis="x", color="#dddddd", labelcolor="gray",
                   top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.tick_params(axis="y", color="#dddddd", labelcolor="gray")

    # Grid
    ax.grid(True, color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)

    # Remove borders
    for side in ("top", "left", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#dddddd")


def _add_labels(fig, ax, player_name, matches):
    """Add the title, labels, legend, and source."""

    start_age = int(matches["player_age"].min())
    end_age = int(matches["player_age"].max())

    # Title
    ax.set_title(f"{player_name}’s Professional Matches, Age {start_age} to {end_age}",
                 fontsize=14, fontweight="bold", pad=80)

    # Player age label
    ax.text(0.01, 1.06, "Player’s\nage:", transform=ax.transAxes,
            fontsize=10, color="gray")

    # Older / younger labels
    ax.text(-0.01, 0.88, "Older\nthan\nopponent", transform=ax.transAxes,
            ha="right", va="center", color="gray")
    ax.text(-0.01, 0.08, "Younger\nthan\nopponent", transform=ax.transAxes,
            ha="right", va="center", color="gray")

    # Legend
    ax.legend(loc="upper center", bbox_to_anchor=(0.46, 1.17),
              ncol=2, frameon=False, handletextpad=-0.5)

    # Source
    fig.text(0.21, 0.03, "Source: Tennis Abstract",
             fontsize=9, color="gray", ha="left")


def _format_player_name(name):
    """Format a player's name for the graph title."""
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
    return name.title()

def _create_plot(matches, player_name):
    """Create a scatter plot from cleaned match data."""
    if matches.empty or matches["player_age"].dropna().empty:
        raise ValueError("No valid match ages available for plotting.")

    fig, ax = plt.subplots(figsize=(12, 8))
    _plot_points(ax, matches)
    _format_axes(ax, matches)
    _add_labels(fig, ax, player_name, matches)

    return fig, ax

def plot_career_matches(player_name):
    """Retrieve a player's career matches and create a scatter plot."""
    matches = get_career_matches(player_name)
    display_name = _format_player_name(player_name)
    return _create_plot(matches, display_name)