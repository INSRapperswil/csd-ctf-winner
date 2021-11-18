import pytest
import responses
from pathlib import Path
from ctf.service.AuthorizedSession import AuthorizedSession


def _token():
    return {
        "method": responses.POST,
        "url": "https://auth.test-dc.hacking-lab.com/auth/realms/test/protocol/openid-connect/token/",
        "body": Path("tests/data/token.json").read_text(),
        "status": 200,
        "content_type": "application/json",
    }


def _teams():
    return {
        "method": responses.GET,
        "url": "https://test.hacking-lab.com/api/user/teams/",
        "body": Path("tests/data/teams.json").read_text(),
        "status": 200,
        "content_type": "application/json",
    }


def _participants(event_id: int):
    return {
        "method": responses.GET,
        "url": f"https://test.hacking-lab.com/api/teacher/events/{event_id}/participants/",
        "body": Path(f"tests/data/participants_{event_id}.json").read_text(),
        "status": 200,
        "content_type": "application/json",
    }


def _solutions(event_id: int):
    return {
        "method": responses.GET,
        "url": f"https://test.hacking-lab.com/api/teacher/events/{event_id}/solutions/",
        "body": Path(f"tests/data/solutions_{event_id}.json").read_text(),
        "status": 200,
        "content_type": "application/json",
    }


@pytest.fixture
def mocked_token():
    with responses.RequestsMock() as response:
        response.add(**_token())
        yield response


@pytest.fixture
def mocked_teams_1():
    with responses.RequestsMock() as response:
        response.add(**_token())
        response.add(**_teams())
        response.add(**_participants(1))
        response.add(**_solutions(1))
        yield response


@pytest.fixture
def mocked_users_1():
    with responses.RequestsMock() as response:
        response.add(**_token())
        response.add(**_teams())
        response.add(**_participants(1))
        response.add(**_solutions(1))
        yield response


@pytest.fixture
def mocked_users_2():
    with responses.RequestsMock() as response:
        response.add(**_token())
        response.add(**_teams())
        response.add(**_participants(1))
        response.add(**_solutions(1))
        response.add(**_participants(2))
        response.add(**_solutions(2))
        yield response


@pytest.fixture
def mocked_solutions_1():
    with responses.RequestsMock() as response:
        response.add(**_token())
        response.add(**_participants(1))
        response.add(**_teams())
        response.add(**_solutions(1))
        yield response


@pytest.fixture
def mocked_solutions_2():
    with responses.RequestsMock() as response:
        response.add(**_token())
        response.add(**_participants(1))
        response.add(**_participants(2))
        response.add(**_teams())
        response.add(**_solutions(1))
        response.add(**_solutions(2))
        response.add(**_solutions(2))
        yield response


@pytest.fixture
def authorized_session() -> AuthorizedSession:
    return AuthorizedSession("test", "username", "password")
