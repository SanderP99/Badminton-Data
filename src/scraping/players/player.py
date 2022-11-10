from dataclasses import dataclass


@dataclass
class Player:
    name: str
    player_id: str
    player_profile_id: str
    country: str
    continent: str


@dataclass
class SinglePlayer:
    player: Player
    rank: int
    previous_rank: int
    points: int
    number_of_tournaments: int

    def header(self) -> tuple:
        return (
            "player_id",
            "name",
            "country",
            "continent",
            "player_profile_id",
            "rank",
            "previous_rank",
            "points",
            "number_of_tournaments",
        )

    def to_csv(self) -> tuple:
        return (
            self.player.player_id,
            self.player.name,
            self.player.country,
            self.player.continent,
            self.player.player_profile_id,
            self.rank,
            self.previous_rank,
            self.points,
            self.number_of_tournaments,
        )


@dataclass
class Pair:
    player_one: Player
    player_two: Player
    rank: int
    previous_rank: int
    points: int
    number_of_tournaments: int

    def header(self) -> tuple:
        return (
            "player_id_one",
            "name_one",
            "country_one",
            "continent_one",
            "player_profile_id_one",
            "player_id_two",
            "name_two",
            "country_two",
            "continent_two",
            "player_profile_id_two",
            "rank",
            "previous_rank",
            "points",
            "number_of_tournaments",
        )

    def to_csv(self) -> tuple:
        return (
            self.player_one.player_id,
            self.player_one.name,
            self.player_one.country,
            self.player_one.continent,
            self.player_one.player_profile_id,
            self.player_two.player_id,
            self.player_two.name,
            self.player_two.country,
            self.player_two.continent,
            self.player_two.player_profile_id,
            self.rank,
            self.previous_rank,
            self.points,
            self.number_of_tournaments,
        )
