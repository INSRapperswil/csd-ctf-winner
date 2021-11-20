import logging as log
import json
from typing import Dict, List
from functools import partial
from requests.exceptions import (
    HTTPError,
    ConnectionError,
    RequestException,
    Timeout,
)
from pathlib import Path
from os.path import getmtime
from datetime import datetime
from ctf.model import Participant, Team, User
from ctf.service.AuthorizedSession import AuthorizedSession


def get_teams(
    session: AuthorizedSession, force_renew: bool, *event_ids: int
) -> List[Team]:
    teams = set()
    users = get_users(session, force_renew, *event_ids)
    for user in users:
        if user.team:
            teams.add(user.team)
    return _sort_participants(teams)


def get_users(
    session: AuthorizedSession, force_renew: bool, *event_ids: int
) -> List[User]:
    try:
        teams = _http_get_teams(session, force_renew, *event_ids)
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


def _http_get_teams(
    session: AuthorizedSession, force_renew: bool, *event_ids: int
) -> List[Team]:
    teams_file = Path("teams.ctf")
    teams_file_valid = teams_file.exists()
    log.info
    if teams_file_valid:
        modification_time = getmtime(teams_file)
        now = datetime.now().timestamp()
        teams_file_valid = not (now - modification_time > (5 * 60))
    if teams_file_valid and not force_renew:
        log.info("read teams from file")
        teams_json = teams_file.read_text()
    else:
        log.info("download teams from server")
        teams = []
        # for event_id in event_ids:
        event_id = 404
        teams_response = session.get(f"api/events/{event_id}/teams/")
        teams_response.raise_for_status()
        for teams_for_event in teams_response.json():
            team_id = teams_for_event["team"]["id"]
            if team_id in list(map(lambda t: t["id"], teams)):
                continue
            members_response = session.get(f"api/teams/{team_id}/members/")
            members_response.raise_for_status()
            teams_for_event["team"].setdefault("members", members_response.json())
            teams.append(teams_for_event["team"])
        teams_json = json.dumps(teams)
        teams_file.write_text(teams_json)
    teams = list(map(_map_json_to_team, json.loads(teams_json)))
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
        if solution["points"] == 0:
            continue
        user = next(u for u in users if u.id == solution["user"]["id"])
        if user.team:
            challenge_id = solution["challenge"]["id"]
            counted_teams = challenge_teams.get(challenge_id, [])
            if user.team not in counted_teams:
                user.team.add_points(solution["points"], solution["lastEdited"])
                counted_teams.append(user.team)
                challenge_teams[challenge_id] = counted_teams
        else:
            user.add_points(solution["points"], solution["lastEdited"])


def _map_json_to_team(team_json: Dict) -> Team:
    member_ids = map(lambda member: member["user"]["id"], team_json["members"])
    return Team(team_json["id"], team_json["name"], list(member_ids))


def _map_json_to_user(participant_json: Dict, teams: List[Team]) -> User:
    profile = participant_json["profile"]
    id = profile["id"]
    user = User(id, profile["username"])
    user.team = next((t for t in teams if id in t.member_ids), None)
    return user
