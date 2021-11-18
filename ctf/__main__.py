import click
import logging as log
from pathlib import Path
from rich.logging import RichHandler
from ctf.printer import html_ranking, print_round, print_ranking
from ctf.server import run_ranking_app
from ctf.service.AuthorizedSession import AuthorizedSession
from ctf.service.users import get_teams, get_users
from ctf.service.challenges import get_challenges
from ctf.winner import select_winners


@click.group(context_settings=dict(auto_envvar_prefix="CTF"))
@click.option(
    "-u",
    "--username",
    required=True,
    prompt=True,
    type=click.STRING,
    show_envvar=True,
    allow_from_autoenv=True,
    help="The Hacking-Lab user with enough privileges to access the API.",
)
@click.option(
    "-p",
    "--password",
    required=True,
    prompt=True,
    hide_input=True,
    type=click.STRING,
    show_envvar=True,
    help="The Hacking-Lab user password. Refrain from using this parameter in the command, type the password when prompted or pass as an environment variable.",
)
@click.option(
    "-v",
    "--verbose",
    required=False,
    is_flag=True,
    help="Enable debug output.",
)
@click.pass_context
def cli(
    context: dict,
    username: str,
    password: str,
    verbose: bool,
):
    """Get the winners for the Cyber Security Days CTF."""
    context.ensure_object(dict)
    context.obj["USERNAME"] = username
    context.obj["PASSWORD"] = password
    context.obj["VERBOSE"] = verbose
    log.basicConfig(
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()],
        level=log.DEBUG if verbose else None,
    )


@cli.command()
@click.option(
    "-t",
    "--tenant",
    required=True,
    type=click.STRING,
    show_envvar=True,
    help="The Hacking-Lab tenant.",
)
@click.option(
    "-e",
    "--event",
    required=True,
    type=click.INT,
    help="Event ID of the event to evaluate.",
)
@click.option(
    "--teams",
    required=False,
    is_flag=True,
    help="Evaluate teams instead of single participants.",
)
@click.pass_context
def round(context: dict, tenant: str, event: int, teams: bool):
    """Get round winners."""
    username = context.obj["USERNAME"]
    password = context.obj["PASSWORD"]
    with AuthorizedSession(tenant, username, password) as session:
        users = get_users(session, False, event)
        challenges = get_challenges(
            session, event_id=event, teams_only=teams, users=users
        )
        if not users or not challenges:
            log.error(
                "Neither participants nor challenges for event found on this tenant. Aborting."
            )
        else:
            challenges_with_winners = select_winners(
                challenges, teams_only=teams, users=users
            )
            print_round(challenges_with_winners)


@cli.command()
@click.option(
    "-t",
    "--tenant",
    required=True,
    type=click.STRING,
    show_envvar=True,
    help="The Hacking-Lab tenant.",
)
@click.option(
    "-e",
    "--events",
    required=True,
    type=click.INT,
    help="Event ID(s) of the event(s) to evaluate.",
    multiple=True,
)
@click.option(
    "--teams",
    required=False,
    is_flag=True,
    help="Evaluate teams instead of single participants.",
)
@click.option(
    "--html",
    required=False,
    is_flag=True,
    help="Print an HTML table instead of a nice terminal output.",
)
@click.option(
    "--server",
    required=False,
    is_flag=True,
    help="Run a Flask server to show the ranking in a browser. The page will refresh itself from time to time.",
)
@click.pass_context
def ranking(
    context: dict, tenant: str, events: int, teams: bool, html: bool, server: bool
):
    """Get ranking and specify format optionally."""
    username = context.obj["USERNAME"]
    password = context.obj["PASSWORD"]
    if server:
        verbose = context.obj["VERBOSE"]
        run_ranking_app(tenant, username, password, list(events), verbose)
        return

    with AuthorizedSession(tenant, username, password) as session:
        participants = (
            get_teams(session, False, *list(events))
            if teams
            else get_users(session, False, *list(events))
        )
        if not participants:
            log.error("No users found for events. Aborting.")
        elif html:
            html_ranking(participants)
        else:
            print_ranking(participants, teams)


@cli.command()
def clear():
    """Clear the previous winners."""
    really = click.prompt("Do you really want to clear the state?", type=bool)
    if really:
        memory = Path("memory.ctf")
        teams = Path("teams.ctf")
    if memory.exists():
        memory.unlink()
        log.info("memory deleted")
    if teams.exists():
        teams.unlink()
        log.info("teams deleted")


if __name__ == "__main__":
    cli()
