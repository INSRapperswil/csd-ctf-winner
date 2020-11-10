#!python3
import json
import sys
from pathlib import Path
from operator import itemgetter
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

# Order the users by rank
users = json.loads(jsonfile.read_text())
sortedUsers = sorted(users, key=itemgetter('rank'))

# Print leaderboard
winSymbols = [l for l in '🥇🥈🥉🥂🍻']
table = Table(title="[spring_green1]Leaderboard", show_lines=True)
table.add_column("[deep_pink3]Rank", justify='right')
table.add_column("[deep_pink3]Username")
table.add_column("[deep_pink3]Points", justify='right')
for index, user in enumerate(sortedUsers):
    prefix = ''
    symbol = winSymbols[index] if index < len(winSymbols) else ''
    if index < 5:
        prefix = '[spring_green1]'
    table.add_row(
        f"{symbol} {prefix}{user['rank']}", f"{prefix}{user['username']}", f"{prefix}{user['points']}")
Console().print(table)
