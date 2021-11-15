from dataclasses import dataclass
from typing import List, Set, Union


@dataclass
class Base:
    id: int
    name: str

    def __hash__(self) -> int:
        return hash(self.id)


class Participant(Base):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
        self.total_points = 0

    def add_points(self, points: int) -> None:
        if points > 0:
            self.total_points += points


class Team(Participant):
    def __init__(self, id: int, name: str, member_ids: List[int]) -> None:
        super().__init__(id, name)
        self.member_ids = member_ids


class User(Participant):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
        self.team: Team = None


class Challenge(Base):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
        self.candidates: Set[Participant] = set()
        self.winner: Union[None, Participant] = None

    def __repr__(self) -> str:
        return f"{self.name} (won by {self.winner.name})" if self.winner else self.name
