import pytest
from tests.mocks import (
    mocked_token,
    mocked_teams,
    mocked_users,
    mocked_solutions,
    authorized_session,
)
from ctf.model import Challenge, Team, User
from ctf.service.users import get_teams, get_users
from ctf.service.challenges import get_challenges

# Parameters for teams
TEST_COMPETERS = Team(id=9, name="Test-Competers", member_ids=[10, 764])
TEST_COMPETERS.add_points(400 + 400)
TEST_COMPETERS2 = Team(id=10, name="Test-Competers2", member_ids=[561, 5])
TEST_COMPETERS2.add_points(300 + 300)

# Parameters for users
MWILLI = User(id=764, name="m.willi")
MWILLI.team = TEST_COMPETERS
MWILLI.add_points(400)
WHATTHEHACK = User(10, "whatthehack")
WHATTHEHACK.team = TEST_COMPETERS
WHATTHEHACK.add_points(400)
ZERRRRO = User(id=541, name="zerrrro")
ZERRRRO.add_points(300)
AMO = User(id=561, name="amo")
AMO.team = TEST_COMPETERS2
AMO.add_points(300)
IGOBLAU = User(id=5, name="igoblau")
IGOBLAU.team = TEST_COMPETERS2
IGOBLAU.add_points(300)

# Parameters for challenges with user candidates
GALACTIC_FILE_SHARE_S = Challenge(1992, "Galactic File Share")
GALACTIC_FILE_SHARE_S.candidates.add(WHATTHEHACK)
RIDDLE_EARTH_FLAGS_S = Challenge(1989, "Riddle Earth Flags")
RIDDLE_EARTH_FLAGS_S.candidates.add(AMO)
RIDDLE_EARTH_FLAGS_S.candidates.add(IGOBLAU)
RIDDLE_EARTH_FLAGS_S.candidates.add(ZERRRRO)
RIDDLE_EARTH_FLAGS_S.candidates.add(MWILLI)
DATING_ALICE_2_S = Challenge(1990, "Dating Alice 2")
DATING_ALICE_2_S.candidates.add(MWILLI)
EMPEROR_SAYS_S = Challenge(1991, "Emperor Says")
EMPEROR_SAYS_S.candidates.add(MWILLI)
DATE_MATE_S = Challenge(1994, "Date Mate")
DATE_MATE_S.candidates.add(IGOBLAU)
DATE_MATE_S.candidates.add(ZERRRRO)
DATING_ALICE_1_S = Challenge(1993, "Dating Alice 1")
DATING_ALICE_1_S.candidates.add(AMO)
DATING_ALICE_1_S.candidates.add(WHATTHEHACK)

# Parameters for challenges with team candidates
GALACTIC_FILE_SHARE_T = Challenge(1992, "Galactic File Share")
GALACTIC_FILE_SHARE_T.candidates.add(TEST_COMPETERS)
RIDDLE_EARTH_FLAGS_T = Challenge(1989, "Riddle Earth Flags")
RIDDLE_EARTH_FLAGS_T.candidates.add(TEST_COMPETERS2)
RIDDLE_EARTH_FLAGS_T.candidates.add(TEST_COMPETERS)
DATING_ALICE_2_T = Challenge(1990, "Dating Alice 2")
DATING_ALICE_2_T.candidates.add(TEST_COMPETERS)
EMPEROR_SAYS_T = Challenge(1991, "Emperor Says")
EMPEROR_SAYS_T.candidates.add(TEST_COMPETERS)
DATE_MATE_T = Challenge(1994, "Date Mate")
DATE_MATE_T.candidates.add(TEST_COMPETERS2)
DATING_ALICE_1_T = Challenge(1993, "Dating Alice 1")
DATING_ALICE_1_T.candidates.add(TEST_COMPETERS2)
DATING_ALICE_1_T.candidates.add(TEST_COMPETERS)


def test_authorize(mocked_token, authorized_session):
    assert authorized_session._refresh_token == None
    login_success = authorized_session._authorize()
    assert login_success
    assert authorized_session._refresh_token == "rt"


@pytest.mark.parametrize("idx, team", [(0, TEST_COMPETERS), (1, TEST_COMPETERS2)])
def test_get_teams(mocked_teams, authorized_session, idx, team):
    teams = get_teams(authorized_session, event_id=1)
    assert vars(teams[idx]) == vars(team)


@pytest.mark.parametrize(
    "idx, user", [(0, MWILLI), (1, AMO), (2, IGOBLAU), (3, ZERRRRO), (4, WHATTHEHACK)]
)
def test_get_users(mocked_users, authorized_session, idx, user):
    users = get_users(authorized_session, event_id=1)
    assert vars(users[idx]) == vars(user)


@pytest.mark.parametrize(
    "idx, challenge",
    [
        (0, GALACTIC_FILE_SHARE_S),
        (1, RIDDLE_EARTH_FLAGS_S),
        (2, DATING_ALICE_2_S),
        (3, EMPEROR_SAYS_S),
        (4, DATE_MATE_S),
        (5, DATING_ALICE_1_S),
    ],
)
def test_get_challenges_single(mocked_solutions, authorized_session, idx, challenge):
    users = get_users(authorized_session, event_id=1)
    challenges = get_challenges(
        authorized_session, event_id=1, teams_only=False, users=users
    )
    assert vars(challenges[idx]) == vars(challenge)


@pytest.mark.parametrize(
    "idx, challenge",
    [
        (0, GALACTIC_FILE_SHARE_T),
        (1, RIDDLE_EARTH_FLAGS_T),
        (2, DATING_ALICE_2_T),
        (3, EMPEROR_SAYS_T),
        (4, DATE_MATE_T),
        (5, DATING_ALICE_1_T),
    ],
)
def test_get_challenges_teams(mocked_solutions, authorized_session, idx, challenge):
    users = get_users(authorized_session, event_id=1)
    challenges = get_challenges(
        authorized_session, event_id=1, teams_only=True, users=users
    )
    assert vars(challenges[idx]) == vars(challenge)
