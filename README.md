# Cyber Security Days Capture The Flag Winners

This repo contains two tools useful for the Capture The Flag.

## challenges.py

Quickly determine the flag winners. Use it this way:

```bash
./challenges.py <path to results file> "<comma-separated list with names which can't win (optional)>"
```

The results file can be obtained from https://hsr.hacking-lab.com/api/rankings/events/EVENT-ID/users/ and must be in JSON format.

## leaderboard.py

Pretty print the leaderboard. Use it this way:

```bash
./leaderboard.py <path to results file>
```

The results file can be obtained from https://hsr.hacking-lab.com/api/rankings/events/EVENT-ID/users/ and must be in JSON format.

## Setup

Clone the repository, change into its directory and run the following commands:

1. `python3 -m venv .`
2. `source bin/activate`
3. `pip install -r requirements.txt`
