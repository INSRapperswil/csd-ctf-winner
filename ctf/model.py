from dataclasses import dataclass
from typing import List, Set, Union


@dataclass
class Base:
    id: int
    name: str

    def __hash__(self) -> int:
        return hash(self.id)


class Team(Base):
    def __init__(self, id: int, name: str, member_ids: List[int]) -> None:
        super().__init__(id, name)
        self.member_ids = member_ids


class User(Base):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
        self.team: Team = None


class Challenge(Base):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
        self.candidates: Set[Union[User, Team]] = set()
        self.winner: Union[None, User, Team] = None

    def __repr__(self) -> str:
        return f"{self.name} (won by {self.winner.name})" if self.winner else self.name
