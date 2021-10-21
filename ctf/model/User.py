from ctf.model import Team


class User:
    def __init__(self, id: int, username: str) -> None:
        self.id = id
        self.username = username
        self.team: Team = None

    def __str__(self) -> str:
        return self.username
