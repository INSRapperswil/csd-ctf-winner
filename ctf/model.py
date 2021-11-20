from dataclasses import dataclass
from typing import List, Set, Union
from datetime import datetime
from dateutil import parser


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
        self.last_submission = parser.parse("1900-01-01T00:00:00Z")

    def add_points(self, points: int, submission_date="1900-01-01T00:00:00Z") -> None:
        if points > 0:
            self.total_points += points
            self._set_last_submission(submission_date)

    def _set_last_submission(self, submission_date) -> None:
        parsed_date = parser.parse(submission_date)
        if parsed_date.timestamp() > self.last_submission.timestamp():
            self.last_submission = parsed_date


class Team(Participant):
    def __init__(self, id: int, name: str, member_ids: List[int]) -> None:
        super().__init__(id, name)
        self.member_ids = member_ids


class User(Participant):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
        self.team: Team = None

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, team={self.team!r})"


class Challenge(Base):
    def __init__(self, id: int, name: str) -> None:
        super().__init__(id, name)
        self.candidates: Set[Participant] = set()
        self.winner: Union[None, Participant] = None

    def __repr__(self) -> str:
        return f"{self.name} (won by {self.winner.name})" if self.winner else self.name
