from typing import List


class Team:
    def __init__(self, id: int, name: str, member_ids: List[int]) -> None:
        self.id = id
        self.name = name
        self.member_ids = member_ids

    def __str__(self) -> str:
        return self.name
