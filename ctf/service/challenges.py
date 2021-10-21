import logging as log
from typing import Dict, List
from functools import partial
from ctf.model.User import User
from ctf.model.Challenge import Challenge
from ctf.service import AuthorizedSession
from ctf.service.users import get_users


def get_challenges(
    session: AuthorizedSession, event_id: int, teams_only=False
) -> List[Challenge]:
    try:
        solutions_response = session.get(f"api/teacher/events/{event_id}/solutions/")
        solutions_response.raise_for_status()
        users = get_users(session, event_id)
        challenges = _extract_challenges_from_solutions(
            solutions_response.json(), users, teams_only
        )
        return challenges
    except Exception:
        log.error("unknown error in get_challenges")
        return []


def _extract_challenges_from_solutions(
    solution_json: Dict, users: List[User], teams_only: bool
) -> Challenge:
    challenges = []
    for s in solution_json:
        id = s["challenge"]["id"]
        if id not in map(lambda c: c.id, challenges):
            challenge = Challenge(id, s["challenge"]["title"])
            challenges.append(challenge)
    for s in solution_json:
        if s["state"] == "FULL_POINTS":
            user = next(u for u in users if u.id == s["user"]["id"])
            challenge = next(c for c in challenges if c.id == s["challenge"]["id"])
            if not teams_only or (teams_only and user.team):
                challenge.candidates.append(user)

    return challenges
