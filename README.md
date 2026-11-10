# Tennis Career Match Analysis

## Overview

This project is a Python package developed for STAT 159 Homework 3. It retrieves tennis players' career match data from Tennis Abstract and creates a scatter plot comparing a player's age with the age difference between the player and their opponents.

The project builds on my Homework 2 visualization by turning the original data processing and plotting code into reusable Python functions.

## Installation

This package can be installed directly from GitHub using `pip`:

```bash
pip install git+https://github.com/yukai0/hw03-yukai0.git
```

The package requires Python 3.10 or newer.

## Usage

The package provides two public functions:

- `get_career_matches(player_name)`: Retrieves and cleans a player's career match data, returning a Pandas DataFrame.
- `plot_career_matches(player_name)`: Retrieves a player's career match data and creates a scatter plot, returning a Matplotlib figure and axes.

Example:

```python
from tennis_career import get_career_matches, plot_career_matches
import matplotlib.pyplot as plt

player_name = "Serena Williams"

# Retrieve and examine career match data
matches = get_career_matches(player_name)
print(matches.head())

# Create a scatter plot
fig, ax = plot_career_matches(player_name)
plt.show()
```

The two functions can also be used independently. Users can retrieve a player's career match data without creating a graph, or generate a graph directly by providing a player's name.

The scatter plot shows the player's age on the x-axis and the age difference between the player and their opponents on the y-axis. Wins and losses are represented separately, with a horizontal line at zero indicating opponents of the same age.

## Repository Structure

```text
hw03-yukai0/
├── tennis_career/
│   ├── __init__.py
│   ├── data.py
│   └── plot.py
├── tests/
│   ├── test_data/
│   │   ├── FemalePlayerCareer.js
│   │   └── MalePlayerCareer.js
│   ├── test_data.py
│   └── test_plot.py
├── pyproject.toml
├── README.md
└── ai.md
```

## Data Source

Career match records are retrieved from [Tennis Abstract](https://www.tennisabstract.com/).

The package processes male and female match records, which provide opponent age information in different formats. Female records include opponent birth dates, while male records provide decimal ages. The package cleans these records and calculates the ages and age differences used for visualization.

## Testing

The project uses `pytest` to test player-name processing, JavaScript parsing, DataFrame cleaning, age calculations, and scatter plot creation.

The tests use local sample JavaScript files provided in the homework instructions rather than requesting data from Tennis Abstract. This allows the tests to run without accessing live servers.

To run the tests, execute the following command from the repository's root directory:

```bash
python -m pytest -v tests/
```

## Personal Reflection

This homework helped me learn a lot more about web scraping. Although I had used web scraping before, this assignment really put my skills to the test because I had to retrieve data from a website that was not always straightforward to work with. I spent a lot of time experimenting with different approaches, exploring different pages, and figuring out which methods worked best for retrieving the information I needed. This taught me that web scraping often requires trial and error, especially when the data is not presented in a consistent format. I also learned more about managing a Python project and organizing my code into multiple functions and files. One of the biggest challenges was figuring out how to structure everything and make the functions work together. I had to think through and experiment with different approaches to make my code simpler and more efficient. The plotting portion was relatively straightforward because I was able to reuse much of my code from Homework 2. This also showed me the benefits of writing reusable code and how work from a previous project could be adapted for a new purpose. Another interesting part of this assignment was learning how to create a `pyproject.toml` file and turn my code into an installable Python package. I enjoyed this process because it was something new to me. Along the way, I also learned more technical skills, such as using different Python functions and libraries. I also gained more experience writing Python tests. Although I had worked with tests before, creating them from scratch for my own package was valuable practice. It helped me better understand how to verify that different parts of my code work correctly. Overall, this assignment gave me more hands-on experience with web scraping, project organization, Python packaging, and automated testing. More importantly, it taught me how to experiment with different solutions, improve my technical skills, and refine my code when my initial approach did not work.