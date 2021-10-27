import shelve
from typing import List, Any, Set
from random import choice
from ctf.model.Challenge import Challenge
from ctf.model.User import User


def select_winners(
    challenges: List[Challenge], teams_only: bool, users: List[User]
) -> List[Challenge]:
    clean_challenges = _remove_previous_winners(challenges, teams_only)
    for challenge in clean_challenges:
        winner = choice(list(challenge.candidates)) if challenge.candidates else None
        challenge.winner = winner
    winners = []
    if teams_only:
        winner_teams = set(
            map(
                lambda c: c.winner, filter(lambda c: c.winner != None, clean_challenges)
            )
        )
        winner_user_ids = [
            x
            for sublist in list(map(lambda w: w.member_ids, winner_teams))
            for x in sublist
        ]
        winners = filter(lambda u: u.id in winner_user_ids, users)
    else:
        winners = map(
            lambda c: c.winner, filter(lambda c: c.winner != None, clean_challenges)
        )

    _remember_winners(list(winners))
    return clean_challenges


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
        invalid_winners = []
        if teams_only:
            invalid_winners = previous_winner_teams & challenge.candidates
        else:
            invalid_winners = previous_winners & challenge.candidates
        for invalid_winner in invalid_winners:
            challenge.candidates.discard(invalid_winner)
    return challenges
