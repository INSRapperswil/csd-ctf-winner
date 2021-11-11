import logging as log
from typing import Dict, List
from functools import partial
from requests.exceptions import (
    HTTPError,
    ConnectionError,
    RequestException,
    Timeout,
)
from ctf.model import Participant, Team, User
from ctf.service.AuthorizedSession import AuthorizedSession


def get_teams(session: AuthorizedSession, event_id: int) -> List[Team]:
    teams = set()
    users = get_users(session, event_id)
    for user in users:
        teams.add(user.team)
    return list(teams)


def get_users(session: AuthorizedSession, event_id: int) -> List[User]:
    try:
        users_response = session.get(f"api/teacher/events/{event_id}/participants/")
        users_response.raise_for_status()
        teams_response = session.get("api/user/teams/")
        teams_response.raise_for_status()
        teams = list(map(_map_json_to_team, teams_response.json()))
        users = list(
            map(partial(_map_json_to_user, teams=teams), users_response.json())
        )
        _add_points_to_participants(session, event_id, users, teams)
        return users
    except HTTPError as e:
        log.error(f"get_users: HTTP not ok: {e.response}")
    except ConnectionError:
        log.error(f"get_users: there was a connection error")
    except Timeout:
        log.error(f"get_users: there was a timeout")
    except RequestException as e:
        log.error(f"get_users: {str(e)} ")
    return []


def _add_points_to_participants(
    session: AuthorizedSession, event_id: int, users: List[User], teams: List[Team]
) -> List[Participant]:
    solutions_response = session.get(f"api/teacher/events/{event_id}/solutions/")
    solutions_response.raise_for_status()
    for solution in solutions_response.json():
        participant = next(u for u in users if u.id == solution["user"]["id"])
        participant.add_points(solution["points"])


def _map_json_to_team(team_json: Dict) -> Team:
    member_ids = map(lambda member: member["user"]["id"], team_json["members"])
    return Team(team_json["id"], team_json["name"], list(member_ids))


def _map_json_to_user(participant_json: Dict, teams: List[Team]) -> User:
    profile = participant_json["profile"]
    id = profile["id"]
    user = User(id, profile["username"])
    user.team = next((t for t in teams if id in t.member_ids), None)
    return user
