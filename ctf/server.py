from typing import List
from flask import Flask
from flask import render_template
from ctf.service.AuthorizedSession import AuthorizedSession
from ctf.service.users import get_teams, get_users

_app = Flask("ctf")
_session = None
_event_ids = []


def run_ranking_app(
    tenant: str, username: str, password: str, event_ids: List[int], verbose: bool
) -> None:
    global _session, _event_ids
    _session = AuthorizedSession(tenant, username, password)
    _event_ids = event_ids
    _app.run(debug=verbose)


@_app.route("/")
def _ranking():
    users = get_users(_session, *_event_ids)
    teams = get_teams(_session, *_event_ids)
    return render_template(
        "ranking.html", singleplayers=users[:9], multiplayers=teams[:8]
    )
