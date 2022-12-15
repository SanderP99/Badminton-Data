from dataclasses import dataclass
from typing import Optional, Tuple

Set = Tuple[int, int]


@dataclass
class Player:
    name: str
    nationality: str


@dataclass
class Pair:
    player_one: Player
    player_two: Player


@dataclass
class Match:
    date: str
    round: str
    scores: Tuple[Set, Set, Optional[Set]]
    seedings: Tuple[Optional[int], Optional[int]]
    discipline: str


@dataclass
class SinglesMatch(Match):
    player_one: Player
    player_two: Player


@dataclass
class DoublesMatch(Match):
    pair_one: Pair
    pair_two: Pair
