#!python3
import json
import sys
from pathlib import Path
from operator import itemgetter
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

# Order the users by rank
users = json.loads(jsonfile.read_text())
sortedUsers = sorted(users, key=itemgetter("rank"))

# Print leaderboard
winSymbols = iter("🥇🥈🥉🥂🍻")
table = Table(
    title="Leaderboard",
    show_lines=True,
    title_style="spring_green1",
    header_style="deep_pink3"
)
table.add_column("Rank", justify="right")
table.add_column("Username")
table.add_column("Points", justify="right")
for index, user in enumerate(sortedUsers):
    table.add_row(
        f"{next(winSymbols, '')} {user['rank']}",
        user["username"],
        str(user["points"]),
        style="spring_green1" if index < 5 else None,
    )
print(table)
