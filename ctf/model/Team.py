from typing import List


class Team:
    def __init__(self, id: int, name: str, member_ids: List[int]) -> None:
        self.id = id
        self.name = name
        self.member_ids = member_ids

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, o: object) -> bool:
        return self.id == o.id if o else False
