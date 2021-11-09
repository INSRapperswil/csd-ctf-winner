import shelve
from typing import List
import unittest.mock as mock
from ctf.model import User
from ctf.service.users import get_users
from ctf.service.challenges import get_challenges
from ctf.winner import select_winners
from tests.mocks import mocked_solutions, authorized_session


def _get_previous_winners_testdata() -> List[User]:
    with shelve.open("tests/data/memory.ctf") as shelf:
        return shelf["winners"]


@mock.patch("ctf.winner._get_previous_winners")
def test_select_winner_users(
    _get_previous_winners_mock, mocked_solutions, authorized_session
):
    _get_previous_winners_mock.return_value = _get_previous_winners_testdata()
    users = get_users(authorized_session, event_id=1)
    challenges = get_challenges(
        authorized_session, event_id=1, teams_only=False, users=users
    )
    alice1 = challenges[5]
    alice1_candidates_before = list(map(lambda c: c.id, alice1.candidates))
    assert 10 in alice1_candidates_before
    challenges_with_winners = select_winners(challenges, teams_only=False, users=users)
    alice1 = challenges_with_winners[5]
    alice1_candidates_after = set(map(lambda c: c.id, alice1.candidates))
    assert 10 not in alice1_candidates_after
    assert alice1.winner == None or alice1.winner.id == 561


@mock.patch("ctf.winner._get_previous_winners")
def test_select_winner_teams(
    _get_previous_winners_mock, mocked_solutions, authorized_session
):
    _get_previous_winners_mock.return_value = _get_previous_winners_testdata()
    users = get_users(authorized_session, event_id=1)
    challenges = get_challenges(
        authorized_session, event_id=1, teams_only=True, users=users
    )
    riddle = challenges[1]
    challenges_with_winners = select_winners(challenges, teams_only=True, users=users)
    riddle = challenges_with_winners[1]
    assert riddle.winner.id == 10


@mock.patch("ctf.winner._get_previous_winners")
def test_no_double_winners(
    _get_previous_winners_mock, mocked_solutions, authorized_session
):
    _get_previous_winners_mock.return_value = _get_previous_winners_testdata()
    users = get_users(authorized_session, event_id=1)
    challenges = get_challenges(
        authorized_session, event_id=1, teams_only=False, users=users
    )
    challenges_with_winners = select_winners(challenges, teams_only=False, users=users)
    dating2 = challenges_with_winners[2]
    assert dating2.winner == None or dating2.winner == users[0]
    emperor = challenges_with_winners[3]
    assert emperor.winner == None
