import requests
from random import choice
from rich import print
from rich.table import Table


def print_challenges_and_their_winners(ranking_url):
    ranking = get_ranking(ranking_url)
    challenges_and_potentials = get_challenges_with_winners(ranking)
    challenges_and_valid_potentials = remove_some_potentials(
        challenges_and_potentials, []
    )
    challenges_and_their_winner = get_winners(challenges_and_valid_potentials)
    print_winners(challenges_and_their_winner)


def get_ranking(ranking_url):
    request = requests.get(ranking_url)
    if request.status_code != 200:
        raise requests.ConnectionError()
    return request.json()


def get_challenges_with_winners(ranking):
    result = {}
    for user in ranking:
        for challenge in [c for c in user["challenges"] if c]:
            winners = result.setdefault(challenge["title"], set())
            if challenge["points"] >= challenge["maxPoints"]:
                winners.add(user["username"])
    return result


def remove_some_potentials(challenges_and_potentials, users_to_remove: list):
    result = {}
    for challenge in challenges_and_potentials:
        valid_potentials = challenges_and_potentials[challenge] - set(users_to_remove)
        result.setdefault(challenge, valid_potentials)
    return result


def get_winners(challenges_and_potentials):
    result = {}
    for challenge in challenges_and_potentials:
        winner = (
            choice(tuple(challenges_and_potentials[challenge]))
            if len(challenges_and_potentials[challenge]) > 0
            else None
        )
        result.setdefault(challenge, winner)
    return result


def print_winners(challenges_and_their_winner):
    winSymbols = "🏆🥂🍾🎈🎇🎆🎉✨🎊🍻🚀"
    loseSymbols = "🤔🤨😮🙄😫🤐😵"
    table = Table(
        title="Challenge Winners",
        show_lines=True,
        title_style="spring_green1",
        header_style="deep_pink3",
    )
    table.add_column("Challenge")
    table.add_column("Winner")
    for challenge in challenges_and_their_winner:
        winner = challenges_and_their_winner[challenge]
        winnerText = (
            f"{choice(winSymbols)} [spring_green1]{winner}"
            if winner
            else f"{choice(loseSymbols)} Unresolved"
        )
        table.add_row(challenge, winnerText)
    print(table)
