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


def get_teams(session: AuthorizedSession, *event_ids: int) -> List[Team]:
    teams = set()
    users = get_users(session, *event_ids)
    for user in users:
        if user.team:
            teams.add(user.team)
    return _sort_participants(teams)


def get_users(session: AuthorizedSession, *event_ids: int) -> List[User]:
    try:
        teams = _http_get_teams(session)
        users = _http_get_users(session, teams, *event_ids)
        for event_id in event_ids:
            _add_points_to_participants(session, event_id, users)
        return _sort_participants(users)
    except HTTPError as e:
        log.error(f"get_users: HTTP not ok: {e.response}")
    except ConnectionError:
        log.error(f"get_users: there was a connection error")
    except Timeout:
        log.error(f"get_users: there was a timeout")
    except RequestException as e:
        log.error(f"get_users: {str(e)} ")
    return []


def _http_get_users(
    session: AuthorizedSession, teams: List[Team], *event_ids: int
) -> List[User]:
    collected_user_responses = []
    for event_id in event_ids:
        users_response = session.get(f"api/teacher/events/{event_id}/participants/")
        users_response.raise_for_status()
        for user_response in users_response.json():
            user_not_yet_collected = user_response["profile"]["id"] not in map(
                lambda r: r["profile"]["id"], collected_user_responses
            )
            if user_not_yet_collected:
                collected_user_responses.append(user_response)
    users = list(map(partial(_map_json_to_user, teams=teams), collected_user_responses))
    return users


def _http_get_teams(session: AuthorizedSession) -> List[Team]:
    teams_response = session.get("api/user/teams/")
    teams_response.raise_for_status()
    teams = list(map(_map_json_to_team, teams_response.json()))
    return teams


def _sort_participants(participants: List[Participant]) -> List[Participant]:
    sorted_participants = sorted(
        participants,
        key=lambda p: (-p.total_points, p.last_submission.timestamp()),
    )
    return list(sorted_participants)


def _add_points_to_participants(
    session: AuthorizedSession, event_id: int, users: List[User]
) -> List[Participant]:
    solutions_response = session.get(f"api/teacher/events/{event_id}/solutions/")
    solutions_response.raise_for_status()
    challenge_teams = {}
    for solution in solutions_response.json():
        user = next(u for u in users if u.id == solution["user"]["id"])
        user.add_points(solution["points"], solution["lastEdited"])
        if user.team:
            challenge_id = solution["challenge"]["id"]
            counted_teams = challenge_teams.get(challenge_id, [])
            if user.team not in counted_teams:
                user.team.add_points(solution["points"], solution["lastEdited"])
                counted_teams.append(user.team)
                challenge_teams[challenge_id] = counted_teams


def _map_json_to_team(team_json: Dict) -> Team:
    member_ids = map(lambda member: member["user"]["id"], team_json["members"])
    return Team(team_json["id"], team_json["name"], list(member_ids))


def _map_json_to_user(participant_json: Dict, teams: List[Team]) -> User:
    profile = participant_json["profile"]
    id = profile["id"]
    user = User(id, profile["username"])
    user.team = next((t for t in teams if id in t.member_ids), None)
    return user
