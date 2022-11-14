from src.scraping.players import scrape_players
from src.scraping.tournaments import scrape_tournaments

if __name__ == "__main__":
    scrape_players.scrape_players(2000)
    scrape_tournaments.scrape_tournaments()
