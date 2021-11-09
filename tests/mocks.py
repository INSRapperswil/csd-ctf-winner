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


def _participants():
    return {
        "method": responses.GET,
        "url": "https://test.hacking-lab.com/api/teacher/events/1/participants/",
        "body": Path("tests/data/participants.json").read_text(),
        "status": 200,
        "content_type": "application/json",
    }


def _solutions():
    return {
        "method": responses.GET,
        "url": "https://test.hacking-lab.com/api/teacher/events/1/solutions/",
        "body": Path("tests/data/solutions.json").read_text(),
        "status": 200,
        "content_type": "application/json",
    }


@pytest.fixture
def mocked_token():
    with responses.RequestsMock() as response:
        response.add(**_token())
        yield response


@pytest.fixture
def mocked_teams():
    with responses.RequestsMock() as response:
        response.add(**_token())
        response.add(**_teams())
        yield response


@pytest.fixture
def mocked_participants():
    with responses.RequestsMock() as response:
        response.add(**_token())
        response.add(**_teams())
        response.add(**_participants())
        yield response


@pytest.fixture
def mocked_solutions():
    with responses.RequestsMock() as response:
        response.add(**_token())
        response.add(**_solutions())
        response.add(**_participants())
        response.add(**_teams())
        yield response


@pytest.fixture
def authorized_session() -> AuthorizedSession:
    return AuthorizedSession("test", "username", "password")
