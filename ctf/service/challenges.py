import logging as log
from typing import Dict, List
from requests.exceptions import (
    HTTPError,
    ConnectionError,
    RequestException,
    Timeout,
)
from ctf.model import User, Challenge
from ctf.service import AuthorizedSession


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
    except HTTPError as e:
        log.error(f"get_challenges: HTTP not ok: {e.response}")
    except ConnectionError:
        log.error(f"get_challenges: there was a connection error")
    except Timeout:
        log.error(f"get_challenges: there was a timeout")
    except RequestException as e:
        log.error(f"get_challenges: {str(e)} ")
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
            user = next((u for u in users if u.id == s["user"]["id"]), None)
            if not user:
                continue

            if teams_only and user.team:
                challenge.candidates.add(user.team)
            elif not teams_only and not user.team:
                challenge.candidates.add(user)

    return challenges
