from typing import List

from ctf.model.User import User


class Challenge:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.candidates: List[User] = []

    def __str__(self) -> str:
        return self.name
