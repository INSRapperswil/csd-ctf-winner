import shelve
from typing import List, Any, Set, Union
from random import choice
from ctf.model.Challenge import Challenge
from ctf.model.User import User
from ctf.model.Team import Team


def select_winners(
    challenges: List[Challenge], teams_only: bool, users: List[User]
) -> List[Challenge]:
    challenges_with_possible_winners = _remove_previous_winners(challenges, teams_only)
    round_winners = set()
    for challenge in challenges_with_possible_winners:
        candidates = list(challenge.candidates - round_winners)
        winner = choice(candidates) if candidates else None
        challenge.winner = winner
        round_winners.add(winner)
    winners = _get_winners(challenges_with_possible_winners)
    if teams_only:
        winner_user_ids = []
        for winner_team in winners:
            winner_user_ids += winner_team.member_ids
        winners = filter(lambda u: u.id in winner_user_ids, users)

    _remember_winners(list(winners))
    return challenges_with_possible_winners


def _get_winners(
    challenges: List[Challenge],
) -> Set[Union[Team, User]]:
    winners = set()
    for challenge in challenges:
        if challenge.winner != None:
            winners.add(challenge.winner)
    return winners


def _get_previous_winners() -> List[User]:
    with shelve.open("memory.ctf") as shelf_file:
        return list(shelf_file.get("winners", []))


def _remember_winners(new_winners: List[User]) -> None:
    with shelve.open("memory.ctf") as shelf_file:
        previous_winners = list(shelf_file.get("winners", []))
        winners = set(previous_winners + new_winners)
        shelf_file["winners"] = winners


def _remove_previous_winners(
    challenges: List[Challenge], teams_only: bool
) -> List[Challenge]:
    previous_winners = set(_get_previous_winners())
    if not previous_winners:
        return challenges
    previous_winner_teams = set(map(lambda w: w.team, previous_winners))
    for challenge in challenges:
        if teams_only:
            invalid_winners = previous_winner_teams & challenge.candidates
        else:
            invalid_winners = previous_winners & challenge.candidates
        for invalid_winner in invalid_winners:
            challenge.candidates.discard(invalid_winner)
    return challenges
