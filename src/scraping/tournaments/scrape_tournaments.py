from datetime import date, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup

from ..matches.scrape_matches import scrape_matches
from .tournament import Tournament

base_link = "https://bwf.tournamentsoftware.com/find/tournament/DoSearch"


def scrape_tournaments() -> None:
    df = pd.read_csv("out/tournaments.csv", delimiter=",", header=0)
    tournaments = scrape_tournaments_on_page()

    tournaments = pd.concat([tournament.to_data_list() for tournament in tournaments])
    df = pd.concat([df, tournaments], ignore_index=True)
    df = df.drop_duplicates()
    df.to_csv("out/tournaments.csv", sep=",", index=False)


def scrape_tournaments_on_page() -> list[Tournament]:
    data = {
        "page": 1,
        "TournamentFilter.StartDate": (date.today() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "TournamentFilter.EndDate": date.today().strftime("%Y-%m-%d"),
    }
    response = requests.post(base_link, data=data)
    soup = BeautifulSoup(response.content, "html.parser")
    tournaments = soup.find_all("li", class_="list__item", recursive=False)
    tournament_list = []
    for tournament in tournaments:
        tournament_list.append(parse_tournament(tournament))
    return tournament_list


def parse_tournament(tournament) -> Tournament:
    name = tournament.find("span", class_="nav-link__value").text
    link = tournament.find("a", class_="media__link")["href"]
    organization, location = tournament.find("small", class_="media__subheading").text.strip().split(" | ")
    try:
        city, country = location.split(", ")
    except ValueError:
        _, city, country = location.split(", ")
    dates = tournament.find("small", class_="media__subheading--muted").text.strip().split("\r\nto")
    start_date, end_date = dates[0].strip(), dates[1].strip()
    try:
        tournament_type = tournament.find("span", class_="tag--soft").text.strip()
    except AttributeError:
        tournament_type = None

    return Tournament(
        name=name,
        organization=organization,
        city=city,
        country=country,
        start_date=start_date,
        end_date=end_date,
        type=tournament_type,
        link=link,
    )


if __name__ == "__main__":
    scrape_tournaments()
