#!python3
import sys
import json
from random import choice
from pathlib import Path
from rich import print
from rich.table import Table

if len(sys.argv) < 2:
    print("Missing file argument.")
    exit(1)

# File from https://hsr.hacking-lab.com/api/rankings/events/EVENT-ID/users/
jsonfile = Path(sys.argv[1])

if not jsonfile.is_file():
    print("The provided file does not exist.")
    exit(1)

# Exclude winners in second arg with comma-separated list
excluded = []
if len(sys.argv) > 2 and len(sys.argv[2]) > 0:
    excluded = sys.argv[2].split(",")

# Assign challenge winners
users = json.loads(jsonfile.read_text())
challengeWinnersPerChallenge = {}
for user in users:
    for challenge in user["challenges"]:
        challengeTitle = challenge["title"]
        challengeWinnersPerChallenge.setdefault(challengeTitle, set())
        if challenge["points"] >= challenge["maxPoints"]:
            winners = challengeWinnersPerChallenge.get(challengeTitle, set())
            username = user["username"]
            if username not in excluded:
                winners.add(user["username"])
            challengeWinnersPerChallenge.setdefault(challengeTitle, winners)

# Select winner and print results
winSymbols = "🏆🥂🍾🥇🎈🎇🎆🎉✨🎊🏅🍻🚀"
looseSymbols = "🤔🤨😮🙄😫🤐😵"
table = Table(
    title="Challenge Winners",
    show_lines=True,
    title_style="spring_green1",
    header_style="deep_pink3",
)
table.add_column("Challenge")
table.add_column("Winner")
for challenge in challengeWinnersPerChallenge:
    allChallengeWinners = tuple(challengeWinnersPerChallenge[challenge])
    if len(allChallengeWinners) > 0:
        winner = f"{choice(winSymbols)} [spring_green1]{choice(allChallengeWinners)}"
    else:
        winner = f"{choice(looseSymbols)} Unresolved"
    table.add_row(challenge, winner)
print(table)
