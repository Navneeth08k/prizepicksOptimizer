import requests
from bs4 import BeautifulSoup

url = "https://www.espn.com/nba/boxscore/_/gameId/401585442"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find all rows containing player data
rows = soup.find_all("tr", class_="Table__TR--sm")


# Iterate over each row and extract player scores
for row in rows:
    # Check if the row is a player row (data-idx is less than 15)
    if "data-idx" in row.attrs and int(row["data-idx"]) < 15:
        # Find all cells within the row
        cells = row.find_all("td")
        
        # Extract data from each cell
        player = cells[0].text.strip()  # Player name or identifier
        score = cells[-1].text.strip()  # Points scored
        
        # Skip rows with non-player data
        if "starters" in player.lower() or "bench" in player.lower() or "dnp" in player.lower() or "min" in player.lower():
            continue
        
        # Print player and score
        print("Player:", player, "Scores:", score)
