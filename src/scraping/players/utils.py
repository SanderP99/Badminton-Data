def is_doubles(category: str) -> bool:
    return category.__contains__("D")


def get_player_id_from_name_link(link) -> str:
    return link["href"].split("player=")[1]
