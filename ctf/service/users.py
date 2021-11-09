import logging as log
from typing import Dict, List
from functools import partial
from ctf.model import Team, User
from ctf.service.AuthorizedSession import AuthorizedSession


def get_teams(session: AuthorizedSession) -> List[Team]:
    try:
        teams_response = session.get("api/user/teams/")
        teams_response.raise_for_status()
        teams = list(map(_map_json_to_team, teams_response.json()))
        return teams
    except Exception as e:
        log.error(f"get_teams: {str(e)}")
        return []


def get_users(session: AuthorizedSession, event_id: int) -> List[User]:
    try:
        users_response = session.get(f"api/teacher/events/{event_id}/participants/")
        users_response.raise_for_status()
        teams = get_teams(session)
        users = list(
            map(partial(_map_json_to_user, teams=teams), users_response.json())
        )
        return users
    except Exception as e:
        log.error(f"get_users: {str(e)}")
        return []


def _map_json_to_team(team_json: Dict) -> Team:
    member_ids = map(lambda member: member["user"]["id"], team_json["members"])
    return Team(team_json["id"], team_json["name"], list(member_ids))


def _map_json_to_user(participant_json: Dict, teams: List[Team]) -> User:
    profile = participant_json["profile"]
    id = profile["id"]
    user = User(id, profile["username"])
    user.team = next((t for t in teams if id in t.member_ids), None)
    return user
