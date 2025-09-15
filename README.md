# Basketball Shot Tracker

A web scraper for basketball-reference.com that extracts player shooting data and creates shot charts for the 2024-2025 NBA season.

## Features

- Scrape player shooting data from basketball-reference.com
- Create visual shot charts showing shooting percentages by court zone
- Compare two players side-by-side
- Support for 2024-2025 season data
- Interactive visualization with color-coded shooting efficiency

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script and follow the prompts:
```bash
python webScraper.py
```

The script will ask for two player names and create a comparison shot chart.

### Programmatic Usage

```python
from webScraper import BasketballReferenceScraper, ShotChartVisualizer

# Initialize scraper and visualizer
scraper = BasketballReferenceScraper()
visualizer = ShotChartVisualizer()

# Get player data
player1_data = scraper.get_player_shooting_data("LeBron James", "2025")
player2_data = scraper.get_player_shooting_data("Stephen Curry", "2025")

# Create comparison chart
fig = visualizer.compare_players(player1_data, player2_data, 
                               "LeBron James", "Stephen Curry")
plt.show()
```

## Shot Chart Features

- **Color Coding**: 
  - Green: 50%+ field goal percentage
  - Yellow: 40-49% field goal percentage  
  - Red: <40% field goal percentage
- **Zone Coverage**: Restricted Area, Paint, Mid-Range, Corner 3s, Above the Break 3s
- **Data Display**: Shows shooting percentage and field goal attempts for each zone

## Data Sources

This scraper pulls data from [basketball-reference.com](https://www.basketball-reference.com/), specifically from player shooting pages for the 2024-2025 season.

## Notes

- The scraper includes rate limiting to be respectful to the website
- Player names should be entered as they appear on basketball-reference.com
- The script automatically searches for players if exact names aren't found
- Shot charts are saved as PNG files for easy sharing

## Example Output

The script generates:
1. A side-by-side comparison chart of two players
2. Console output with detailed shooting statistics
3. A saved PNG file of the comparison chart

## Troubleshooting

- If a player isn't found, try using their full name or common nickname
- Ensure you have an internet connection for web scraping
- Some players may not have complete shooting data for the current season
