import click
import logging as log
from pathlib import Path
from rich.logging import RichHandler
from ctf.printer import print_round
from ctf.service.AuthorizedSession import AuthorizedSession
from ctf.service.users import get_users
from ctf.service.challenges import get_challenges
from ctf.winner import select_winners


@click.group(context_settings=dict(auto_envvar_prefix="CTF"))
@click.option(
    "-t",
    "--tenant",
    required=True,
    prompt=True,
    type=click.STRING,
    show_envvar=True,
    help="The Hacking-Lab tenant.",
)
@click.option(
    "-e",
    "--event",
    required=True,
    prompt=True,
    type=click.INT,
    help="Event ID of the event to evaluate.",
)
@click.option(
    "--teams",
    required=False,
    is_flag=True,
    help="Evaluate teams instead of single participants.",
)
@click.option(
    "-u",
    "--username",
    required=True,
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
    tenant: str,
    event: int,
    teams: bool,
    username: str,
    password: str,
    verbose: bool,
):
    """Get the winners for the Cyber Security Days CTF."""
    context.ensure_object(dict)
    context.auto_envvar_prefix = "CTF"
    context.obj["TENANT"] = tenant
    context.obj["EVENT_ID"] = event
    context.obj["EVALUATE_TEAMS"] = teams
    context.obj["USERNAME"] = username
    context.obj["PASSWORD"] = password
    log.basicConfig(
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler()],
        level=log.DEBUG if verbose else None,
    )


@cli.command()
@click.pass_context
def round(context: dict):
    """Get round winners."""
    tenant = context.obj["TENANT"]
    username = context.obj["USERNAME"]
    password = context.obj["PASSWORD"]
    evaluate_teams = context.obj["EVALUATE_TEAMS"]
    with AuthorizedSession(tenant, username, password) as session:
        users = get_users(session, event_id=338)
        challenges = get_challenges(
            session, event_id=338, teams_only=evaluate_teams, users=users
        )
        challenges_with_winners = select_winners(
            challenges, teams_only=evaluate_teams, users=users
        )
    print_round(challenges_with_winners)


@cli.command()
@click.pass_context
def full(context: dict):
    """Get full event winner."""
    raise NotImplementedError()


@cli.command()
@click.pass_context
def clear(context: dict):
    """Clear the previous winners."""
    file = Path("memory.ctf")
    if file.exists():
        file.unlink()
        log.info("memory deleted")
    else:
        log.warning("no memory file found")


if __name__ == "__main__":
    cli()
