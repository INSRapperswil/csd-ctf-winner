from typing import List
from rich import print
from rich.table import Table
from random import choice
from ctf.model import Challenge, Participant


_win_symbols = "🏆🥂🍾🎈🎇🎆🎉✨🎊🍻🚀"
_lose_symbols = "🤔🤨😮🙄😫🤐😵"
_rank_symbols = iter("🥇🥈🥉")


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


def print_ranking(participants: List[Participant], teams: bool):
    table = Table(
        title=f"Ranking {'Multiplayer' if teams else 'Single Player'}",
        show_lines=True,
        title_style="spring_green1",
        header_style="deep_pink3",
    )
    table.add_column("Rank", justify="right")
    table.add_column(f"{'Team' if teams else 'Player'} Name")
    table.add_column("Points", justify="right")
    price_available = 3 if teams else 5
    for idx, participant in enumerate(participants):
        table.add_row(
            f"{idx + 1}." if idx > 2 else f"{next(_rank_symbols)}.",
            participant.name,
            str(participant.total_points),
            style="spring_green1" if idx < price_available else None,
        )
    print(table)


def html_ranking(participants: List[Participant]):
    table_before = """<table>
    <tbody>"""
    table_after = """
    </tbody>
</table>
"""
    table_content = ""
    for idx, participant in enumerate(participants):
        table_content += f"""
        <tr>
            <td><b>{idx + 1}</b></td>
            <td>{participant.name}</td>
            <td>{participant.total_points}</td>
        </tr>"""
    print(table_before + table_content + table_after)
