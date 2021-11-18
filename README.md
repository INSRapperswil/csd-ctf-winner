# Cyber Security Days Capture The Flag Winners

Get the winners for the Cyber Security Days CTF.

## Setup Environment

Clone the repository, change into its directory and run the following commands:

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python -m ctf`

### Testing

Just run the command `pytest` in the virtual environment. The test data in `memory.ctf` is a set containing the users `amo` and `whatthehack`.

## How It Works

### General Advice

- If teams are involved in the event, always evaluate teams first (use the `--teams` option).
- Winners are stored into the `memory.ctf` file so that they cannot win again.

### Algorithm Round

1. Fetch all participants and organize them into teams, if they are team members.
2. Get solutions, and out of it, the challenges.
3. Add potential winners to the `candidates` field of a challenge.
4. Remove all previous winners (stored in `memory.ctf`) from the `candidates` field.
5. Select winner for challenge.
6. Add winners to `memory.ctf` file.
7. Print challenges and their winners.

### Algorithm Ranking

1. After getting the users and the teams, fetch the solutions and add points to the user/team.
2. Also add the overall last submission date to the participant.
3. Sort participants by points (descending) and last submission date (ascending).
4. Print users/teams, their points and their rank. The rank is defined by the list index.
