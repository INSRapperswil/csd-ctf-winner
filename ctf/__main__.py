import click
import logging as log
from rich.logging import RichHandler
from ctf.service.AuthorizedSession import AuthorizedSession
from ctf.service.challenges import get_challenges


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
        teams = get_challenges(session, event_id=338, teams_only=evaluate_teams)
    print(teams)
    # raise NotImplementedError()


@cli.command()
@click.pass_context
def full(context: dict):
    """Get full event winner."""
    raise NotImplementedError()


if __name__ == "__main__":
    cli()
