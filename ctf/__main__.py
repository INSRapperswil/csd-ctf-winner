import click
from ctf.challenge import print_challenges_and_their_winners


@click.group()
@click.option(
    "-r", "--ranking", required=True, prompt=True, help="Host running Hacking-Lab."
)
@click.pass_context
def cli(context: dict, ranking: str):
    """Get the winners for the Cyber Security Days CTF."""
    context.ensure_object(dict)
    context.obj["RANKING_URL"] = ranking


@cli.command()
@click.pass_context
def challenge(context: dict):
    """Get challenge winners."""
    ranking_url = context.obj["RANKING_URL"]
    print_challenges_and_their_winners(ranking_url)


@cli.command()
@click.pass_context
def event(context: dict):
    """Get full event winner."""
    raise NotImplementedError()


if __name__ == "__main__":
    cli()
