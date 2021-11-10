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
    "-v",
    "--verbose",
    required=False,
    is_flag=True,
    help="Enable debug output.",
)
@click.pass_context
def cli(
    context: dict,
    verbose: bool,
):
    """Get the winners for the Cyber Security Days CTF."""
    context.ensure_object(dict)
    context.auto_envvar_prefix = "CTF"
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
def round(tenant: str, event: int, teams: bool, username: str, password: str):
    """Get round winners."""
    with AuthorizedSession(tenant, username, password) as session:
        users = get_users(session, event_id=event)
        challenges = get_challenges(
            session, event_id=event, teams_only=teams, users=users
        )
        challenges_with_winners = select_winners(
            challenges, teams_only=teams, users=users
        )
    print_round(challenges_with_winners)


@cli.command()
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
def ranking():
    """Get ranking and specify format optionally."""
    raise NotImplementedError()


@cli.command()
def clear():
    """Clear the previous winners."""
    file = Path("memory.ctf")
    if file.exists():
        really = click.prompt("Do you really want to clear the results?", type=bool)
        if really:
            file.unlink()
            log.info("memory deleted")
        else:
            log.warning("user does not want to delete memory")
    else:
        log.warning("no memory file found")


if __name__ == "__main__":
    cli()
