# Sole purpose of this is to read from our DB and send latest info to the server, just in case something gets corrupted mid match
# Currently, python client will write the most updated values to sqlite after every round
# So we just pull those values, parse them, push them to server

import json
import sys
from rich import print
from python_game_loop import push_update
from sqlite_helper import get_all_values

stored_rules = None
stored_living_users = None
stored_dead_users = None
stored_leaderboard = None  # Optional - unlike the other 3, restoring it isn't required to proceed

storage = get_all_values()
for row in storage:
    if row['key'] == "rules":
        stored_rules = json.loads(row['value'])
    elif row['key'] == "living_users":
        stored_living_users = json.loads(row['value'])
    elif row['key'] == "dead_users":
        stored_dead_users = json.loads(row['value'])
    elif row['key'] == "leaderboard":
        stored_leaderboard = json.loads(row['value'])

print(f"\nGot the following values:\n\nRules:\n{stored_rules}\n\nLiving Users:\n{stored_living_users}\n\nDead Users:\n{stored_dead_users}\n\nLeaderboard:\n{stored_leaderboard}\n\n")

# If any of the 3 REQUIRED values are null or missing from DB, flag it here
# This might be okay, but should double check that you're okay pushing that to server and wiping anything there
if None in (stored_rules, stored_living_users, stored_dead_users):
    sys.exit(1)

push_update(stored_rules, stored_living_users, stored_dead_users, leaderboard=stored_leaderboard)

print(f"[green] Sent update to server!\n")