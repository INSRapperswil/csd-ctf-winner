from typing import List
from rich import print
from rich.table import Table
from random import choice
from ctf.model.Challenge import Challenge


_win_symbols = "🏆🥂🍾🎈🎇🎆🎉✨🎊🍻🚀"
_lose_symbols = "🤔🤨😮🙄😫🤐😵"


def print_round(challenges_with_winner: List[Challenge]) -> None:
    table = Table(
        title="Round Winners",
        show_lines=True,
        title_style="spring_green1",
        header_style="deep_pink3",
    )
    table.add_column("Challenge")
    table.add_column("Winner")
    for challenge in challenges_with_winner:
        winner = (
            f"{choice(_win_symbols)} [spring_green1]{challenge.winner.name}"
            if challenge.winner
            else f"{choice(_lose_symbols)} Unresolved"
        )
        table.add_row(challenge.name, winner)
    print(table)
