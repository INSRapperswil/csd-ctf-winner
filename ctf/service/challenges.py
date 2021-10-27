import logging as log
from typing import Dict, List
from ctf.model.User import User
from ctf.model.Challenge import Challenge
from ctf.service import AuthorizedSession
from ctf.service.users import get_users


def get_challenges(
    session: AuthorizedSession, event_id: int, teams_only: bool, users: List[User]
) -> List[Challenge]:
    try:
        solutions_response = session.get(f"api/teacher/events/{event_id}/solutions/")
        solutions_response.raise_for_status()
        challenges = _extract_challenges_from_solutions(
            solutions_response.json(), users, teams_only
        )
        return challenges
    except Exception as e:
        log.error(f"get_challenges: {str(e)}")
        return []


def _extract_challenges_from_solutions(
    solution_json: Dict, users: List[User], teams_only: bool
) -> List[Challenge]:
    challenges = []
    for s in solution_json:
        challenge = next((c for c in challenges if c.id == s["challenge"]["id"]), None)
        if not challenge:
            challenge = Challenge(s["challenge"]["id"], s["challenge"]["title"])
            challenges.append(challenge)
        if s["state"] == "FULL_POINTS":
            user = next(u for u in users if u.id == s["user"]["id"])
            if not teams_only:
                challenge.candidates.add(user)
            elif user.team:
                challenge.candidates.add(user.team)
    return challenges
