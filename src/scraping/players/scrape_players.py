import csv
import os
import re
from datetime import date
from typing import Union

import bs4
import requests
from bs4 import BeautifulSoup

from . import utils
from .player import Pair, Player, SinglePlayer

categories = {"MS": 472, "WS": 473, "MD": 474, "WD": 475, "XD": 476}

base_link = "https://bwf.tournamentsoftware.com/ranking/ranking.aspx?rid=70"
ranking_link = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=%d&category=%d&C472FOC=&p=%d&ps=%d"


def scrape_players(number_of_players: int = 1000, output_path: str = "out") -> None:
    number_of_pages = number_of_players // 100
    ranking_id = get_correct_ranking_id()

    for category in categories.keys():
        players = []
        is_doubles = utils.is_doubles(category)
        for page_number in range(1, number_of_pages + 1):
            players.extend(scrape_players_on_page(get_ranking_link(ranking_id, category, page_number), is_doubles))
        write_to_csv(players, category, output_path)


def write_to_csv(players: Union[list[SinglePlayer], list[Pair]], category: str, output_path: str) -> None:
    path = f'{output_path}/{date.today().strftime("%Y-%m-%d")}'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + f'/{category}_{date.today().strftime("%Y-%m-%d")}', "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(players[0].header())
        for player in players:
            writer.writerow(player.to_csv())


def scrape_players_on_page(link: str, is_doubles: bool) -> Union[list[SinglePlayer], list[Pair]]:
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    records = soup.find_all("tr")[2:-1]  # Remove two headers and footer
    players = []
    for record in records:
        if is_doubles:
            players.append(parse_record_doubles(record))
            if players[-1] is None:
                players.pop()
        else:
            players.append(parse_record_singles(record))
    return players


def parse_record_singles(record: bs4.element.Tag) -> SinglePlayer:
    rank = record.find("td", class_="rank").text
    try:
        previous_rank = record.find("td", class_=re.compile(r"rank_(.*)"))["title"].split(": ")[1]
    except TypeError:
        previous_rank = None
    name_link, profile_link, continent_link, country_link = record.find_all("a")
    name = name_link.text
    player_id = utils.get_player_id_from_name_link(name_link)
    player_profile_id = profile_link["href"].split("/")[-1]
    continent = continent_link.text
    country = country_link.text

    x = record.find_all("td", class_="right")
    points = x[0].text
    number_of_tournaments = x[1].text

    player = Player(
        name=name,
        player_id=player_id,
        continent=continent,
        country=country,
        player_profile_id=player_profile_id,
    )

    return SinglePlayer(
        player=player,
        rank=rank,
        previous_rank=previous_rank,
        points=points,
        number_of_tournaments=number_of_tournaments,
    )


def parse_record_doubles(record: bs4.element.Tag) -> Pair:
    error = False
    rank = record.find("td", class_="rank").text
    try:
        previous_rank = record.find("td", class_=re.compile(r"rank_(.*)"))["title"].split(": ")[1]
    except TypeError:
        previous_rank = None

    x = record.find_all("td", class_="right")
    points = x[0].text
    number_of_tournaments = x[1].text

    try:
        (
            name_link_one,
            name_link_two,
            profile_link_one,
            profile_link_two,
            continent_link,
            country_link,
        ) = record.find_all("a")
        country_one, country_two = country_link.text, country_link.text
        continent_one, continent_two = continent_link.text, continent_link.text
    except ValueError:  # Two different countries
        try:
            (
                name_link_one,
                name_link_two,
                profile_link_one,
                profile_link_two,
                continent_link,
                country_link_one,
                country_link_two,
            ) = record.find_all("a")
            country_one, country_two = country_link_one.text, country_link_two.text
            continent_one, continent_two = continent_link.text, continent_link.text
        except ValueError:  # Two different continents
            try:
                (
                    name_link_one,
                    name_link_two,
                    profile_link_one,
                    profile_link_two,
                    continent_link_one,
                    continent_link_two,
                    country_link_one,
                    country_link_two,
                ) = record.find_all("a")
                country_one, country_two = country_link_one.text, country_link_two.text
                continent_one, continent_two = continent_link_one.text, continent_link_two.text
            except ValueError:
                error = True

    if not error:
        player_one = Player(
            name=name_link_one.text,
            player_id=utils.get_player_id_from_name_link(name_link_one),
            player_profile_id=profile_link_one["href"].split("/")[-1],
            country=country_one,
            continent=continent_one,
        )

        player_two = Player(
            name=name_link_two.text,
            player_id=utils.get_player_id_from_name_link(name_link_two),
            player_profile_id=profile_link_two["href"].split("/")[-1],
            country=country_two,
            continent=continent_two,
        )

        return Pair(
            player_one=player_one,
            player_two=player_two,
            rank=rank,
            previous_rank=previous_rank,
            points=points,
            number_of_tournaments=number_of_tournaments,
        )
    else:
        return None


def get_ranking_link(ranking_id: int, category: str, page_number: int = 1, items_per_page: int = 100) -> str:
    category_id = categories.get(category, "MS")
    return ranking_link % (ranking_id, category_id, page_number, items_per_page)


def get_correct_ranking_id() -> int:
    response = requests.get(base_link)
    return int(BeautifulSoup(response.content, "html.parser").find("option").get("value"))


if __name__ == "__main__":
    scrape_players(100, "out")
