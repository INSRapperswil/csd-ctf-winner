#!python3
import sys
import json
from random import choice
from pathlib import Path
from rich.console import Console
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
    excluded = sys.argv[2].split(',')

# Assign challenge winners
users = json.loads(jsonfile.read_text())
challengeWinnersPerChallenge = {}
for user in users:
    for challenge in user['challenges']:
        challengeTitle = challenge['title']
        challengeWinnersPerChallenge.setdefault(challengeTitle, set())
        if challenge['points'] >= challenge['maxPoints']:
            winners = challengeWinnersPerChallenge.get(challengeTitle, set())
            username = user['username']
            if username not in excluded:
                winners.add(user['username'])
            challengeWinnersPerChallenge.setdefault(challengeTitle, winners)

# Select winner and print results
winSymbols = [l for l in '🏆🥂🍾🥇🎈🎇🎆🎉✨🎊🏅🍻🚀']
looseSymbols = [l for l in '🤔🤨😮🙄😫🤐😵']
table = Table(title="[spring_green1]Challenge Winners", show_lines=True)
table.add_column("[deep_pink3]Challenge")
table.add_column("[deep_pink3]Winner")
for challenge in challengeWinnersPerChallenge:
    winner = f"{choice(looseSymbols)} Unresolved"
    allChallengeWinners = tuple(challengeWinnersPerChallenge[challenge])
    if len(allChallengeWinners) > 0:
        winner = f"{choice(winSymbols)} [spring_green1]{choice(allChallengeWinners)}"
    table.add_row(challenge, winner)
Console().print(table)
