import pytest
import json
import responses
from requests import ConnectionError
from pathlib import Path
from ctf.challenge import (
    get_challenges_with_winners,
    get_ranking,
    remove_some_potentials,
)


def get_user_simple():
    return json.loads(Path("tests/testdata.user.simple.json").read_text())


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_get_ranking_json(mocked_responses):
    mocked_responses.add(
        responses.GET,
        "https://ranking.ost.hacking-lab.com/api/rankings/users/",
        body=Path("tests/testdata.user.single.json").read_text(),
        status=200,
        content_type="application/json",
    )
    ranking = get_ranking("https://ranking.ost.hacking-lab.com/api/rankings/users/")
    assert ranking == [
        dict(
            rank=1,
            points=100,
            challenges=[
                {
                    "id": 1,
                    "points": 100,
                    "maxPoints": 100,
                    "lastUserSolutionTime": "2019-10-02T07:20:03Z",
                    "title": "Challenge 1",
                    "level": {"id": 2, "name": "easy"},
                }
            ],
            username="user1",
        )
    ]


def test_get_ranking_error(mocked_responses):
    mocked_responses.add(
        responses.GET,
        "https://ranking.ost.hacking-lab.com/api/rankings/users/",
        body=Path("tests/testdata.user.single.json").read_text(),
        status=404,
        content_type="application/json",
    )
    with pytest.raises(ConnectionError):
        get_ranking("https://ranking.ost.hacking-lab.com/api/rankings/users/")


def test_get_challenges_with_winners():
    simple = get_user_simple()
    challenges_with_potentials = get_challenges_with_winners(simple)
    assert len(challenges_with_potentials["Challenge 1"]) == 2
    assert len(challenges_with_potentials["Challenge 2"]) == 1
    assert len(challenges_with_potentials["Challenge 3"]) == 0


def test_remove_some_potentials_noremove():
    simple = get_user_simple()
    challenges_with_potentials = get_challenges_with_winners(simple)
    with_removed = remove_some_potentials(challenges_with_potentials, [])
    assert len(with_removed["Challenge 1"]) == 2
    assert len(with_removed["Challenge 2"]) == 1
    assert len(with_removed["Challenge 3"]) == 0


def test_remove_some_potentials_nofirst():
    simple = get_user_simple()
    challenges_with_potentials = get_challenges_with_winners(simple)
    with_removed = remove_some_potentials(challenges_with_potentials, ["user1"])
    assert len(with_removed["Challenge 1"]) == 1
    assert len(with_removed["Challenge 2"]) == 0
    assert len(with_removed["Challenge 3"]) == 0
