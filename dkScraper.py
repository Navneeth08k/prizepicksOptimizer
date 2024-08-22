import requests
from bs4 import BeautifulSoup
import csv

def scrape_data(url, category):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables containing the data
    tables = soup.find_all('table', class_='sportsbook-table')

    # Initialize lists to store data
    players = []
    stats = []

    # Extract data from each table
    for table in tables:
        # Extract data from the table rows
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            # Extract player name
            player_span = row.find('span', class_='sportsbook-row-name')
            if player_span:
                player = player_span.text.strip()
            else:
                player = "Unknown"  # If player name not found, use "Unknown"

            # Extract text containing stats
            stats_text = columns[1].text.strip()

            # Split the text by '-' or '+' to get the part before the odds
            stats_parts = stats_text.split('-')
            if len(stats_parts) == 1:  # If '-' is not found, try splitting by '+'
                stats_parts = stats_text.split('+')

            # Extract the numerical part if available
            if len(stats_parts) >= 1:
                stats_value = stats_parts[0].split()[1]  # Extract the second part after splitting by whitespace
                # Extract only the numerical value if available
                if '−' in stats_value:
                    stats_value = stats_value.split('−')[0].strip()  # Split by '−' and take the first part
                elif '-' in stats_value:
                    stats_value = stats_value.split('-')[0].strip()  # Split by '-' and take the first part
                try:
                    stats_value = float(stats_value)
                except ValueError:
                    stats_value = None
            else:
                stats_value = None

            # Append data to lists
            players.append(player)
            stats.append(stats_value)

    return players, stats, [category] * len(players)

# URLs of the webpages to scrape
urls = {
    'points': 'https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-points',
    'rebounds': 'https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-rebounds',
    'threes': 'https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-threes',
    'assists': 'https://sportsbook.draftkings.com/leagues/basketball/nba?category=player-assists'
}

# Initialize lists to store all data
all_players = []
all_stats = []
all_categories = []

# Scrape data for each category
for category, url in urls.items():
    players, stats, categories = scrape_data(url, category)
    all_players.extend(players)
    all_stats.extend(stats)
    all_categories.extend(categories)

# Write data to a single CSV file
with open('draftKings_combined.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Player', 'Category', 'Stat'])  # Write header row
    for player, category, stat in zip(all_players, all_categories, all_stats):
        writer.writerow([player, category, stat])

print("Combined data has been written to draftKings_combined.csv")
