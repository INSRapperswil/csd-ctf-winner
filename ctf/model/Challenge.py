from typing import Set, Union
from ctf.model.User import User
from ctf.model.Team import Team


class Challenge:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.candidates: Set[Union[User, Team]] = set([])
        self.winner: Union[None, User, Team] = None

    def __repr__(self) -> str:
        return f"{self.name} (won by {self.winner.name})" if self.winner else self.name

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, o: object) -> bool:
        return self.id == o.id if o else False
