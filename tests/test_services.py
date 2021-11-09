from tests.mocks import (
    mocked_token,
    mocked_teams,
    mocked_participants,
    mocked_solutions,
    authorized_session,
)
from ctf.service.users import get_teams, get_users
from ctf.service.challenges import get_challenges


def test_authorize(mocked_token, authorized_session):
    assert authorized_session._refresh_token == None
    login_success = authorized_session._authorize()
    assert login_success
    assert authorized_session._refresh_token == "rt"


def test_get_teams(mocked_teams, authorized_session):
    teams = get_teams(authorized_session)
    assert len(teams) == 2
    team9 = teams[0]
    team10 = teams[1]
    assert team9.id == 9
    assert team9.name == "Test-Competers"
    assert team9.member_ids == [10, 764]
    assert team10.id == 10


def test_get_users(mocked_participants, authorized_session):
    users = get_users(authorized_session, event_id=1)
    assert len(users) == 5
    mwilli = users[0]
    assert mwilli.name == "m.willi"
    assert mwilli.team.id == 9
    zerrrro = users[3]
    assert zerrrro.id == 541
    assert zerrrro.team == None
    whatthehack = users[4]
    assert whatthehack.team.id == 9


def test_get_challenges_single(mocked_solutions, authorized_session):
    users = get_users(authorized_session, event_id=1)
    challenges = get_challenges(
        authorized_session, event_id=1, teams_only=False, users=users
    )
    assert len(challenges) == 6
    galactic = challenges[0]
    assert galactic.id == 1992
    assert galactic.name == "Galactic File Share"
    assert 10 in list(map(lambda c: c.id, galactic.candidates))
    assert len(galactic.candidates) == 1
    riddle = challenges[1]
    assert len(riddle.candidates) == 4


def test_get_challenges_teams(mocked_solutions, authorized_session):
    users = get_users(authorized_session, event_id=1)
    challenges = get_challenges(
        authorized_session, event_id=1, teams_only=True, users=users
    )
    assert len(challenges) == 6
    galactic = challenges[0]
    assert galactic.id == 1992
    assert galactic.name == "Galactic File Share"
    assert 9 in list(map(lambda c: c.id, galactic.candidates))
    assert len(galactic.candidates) == 1
    riddle = challenges[1]
    assert riddle.name == "Riddle Earth Flags"
    assert len(riddle.candidates) == 2
