from ctf.model import Team


class User:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.team: Team = None

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, o: object) -> bool:
        return self.id == o.id if o else False
