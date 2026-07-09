import os
import time
import requests
from twitchio.ext import commands
from twitchio import *
import asyncio
import threading
import os
import keyboard
import time
import json
from dotenv import load_dotenv
from rich import print
from enum import Enum
from sqlite_helper import create_tables, save_to_db
from python_rules_manager import RulesManager

# What MATCH are we currently on? This is just for Doug's own bookkeeping now -
# rules are drawn randomly from the pool (see python_rule_pool.py / python_rules_manager.py)
# rather than indexing into a hand-authored per-match ruleset, so this number no longer
# selects anything. It's still updated manually by Doug when a new match starts.
# Starts at 0, then 1, then 2
MATCH_NUMBER = 0

# What ROUND are we currently on? Every new round introduces 1-2 new password rules
# This is incremented automatically every time the KeypressBot triggers a new round
# Needs to start as 1 and not 0, since it's saying there's a LENGTH of 1 rounds in the arrays that we'll be checking
round_number = 1

###########################################################

class GameState(Enum):
    ACCEPTING_SUBMISSIONS = "ACCEPTING_SUBMISSIONS"
    INTERMISSION = "INTERMISSION"

listening_to_chat = False # Flag that says "We're accepting pw submissions for this round"
# obswebsockets_manager = OBSWebsocketsManager()
rules_manager = RulesManager()
password_check_lock = threading.Lock()

# List of all the users who submitted (and thus are ineligible to submit again)
users_who_submitted_already = set[str]()
# List of valid passwords we've received this round (so that no one can do copy them)
previously_submitted_passwords = set[str]()

ALREADY_SUBMITTED_FAIL_MESSAGE = "Submitted a password that someone else already had!"
DIDNT_SUBMIT_FAIL_MESSAGE = "Failed to submit a password in time."
SERVER_URL = 'https://password-battle-royale-sigma.vercel.app/api/passwords' # Replace with your server URL

load_dotenv('.env.local') # Loads the local env file so you can os.getenv() it
CLIENT_SECRET = os.getenv('UPDATE_DB_KEY')

class TwitchBot(commands.Bot):

    def __init__(self):
        self.CHANNEL_NAME = 'dougdoug'
        super().__init__(token=os.getenv('TWITCH_ACCESS_TOKEN'), prefix='?', initial_channels=[self.CHANNEL_NAME]) #connects to twitch channel
    
    async def event_ready(self):
        self.broadcaster = await self.fetch_users(names=[self.CHANNEL_NAME])
        print(f'[green]Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        await self.process_message(message)

    async def process_message(self, message: Message):
        global MATCH_NUMBER, round_number, living_users, dead_users, listening_to_chat
        try:
            username = message.author.name
            message = message.content

            if listening_to_chat:
                if not message.lower().startswith("!p ") or len(message) < 4: 
                    # This person isn't submitting a password, just ignore them
                    return

                new_password = message[3:].strip()  # drop the "!p ", the rest of their message is the password (minus whitespace)

                with password_check_lock: # Used to prevent race conditions with previously_submitted_passwords

                    # Step 1 - check if they're dead or if they've already submitted this round
                    if (username not in living_users) or (username in users_who_submitted_already):
                        return # Not eligible to submit, ignore their message

                    # Step 2 - Determine their fate
                    valid = True
                    if new_password in previously_submitted_passwords: 
                        # Auto fail if they used someone's existing password
                        valid = False
                        failure_reason = ALREADY_SUBMITTED_FAIL_MESSAGE
                    else:
                        # Actually check if their password follows all the rules
                        valid, failure_reason = rules_manager.is_valid_password(round_number, new_password)

                    # Step 3 - Update their info accordingly
                    if valid:
                        # PASSWORD ACCEPTED - update their info
                        living_users[username]['password'] = new_password
                        living_users[username]['submission_timestamp'] = int(time.time() * 1000)
                        previously_submitted_passwords.add(new_password)
                    else:
                        # PASSWORD DENIED
                        living_users.pop(username, None) # Remove them from living users list 
                        dead_users.insert(0, {'username': username, 'password': new_password, 'submission_timestamp': int(time.time() * 1000), 'failure_message': failure_reason })

                    users_who_submitted_already.add(username) # Either way, add them to the list of people who've submitted this round
        except Exception as e:
            print(f"[red]Error processing message from {username}: {e}")



class KeyPressBot():
    def __init__(self):
        create_tables()
        print("[blue]Keypress bot running!")

    def run(self):
        global listening_to_chat, MATCH_NUMBER, round_number, living_users, dead_users

        while True:

            # Wait until user presses -
            print("[yellow]\n\nPress F13 to begin!")
            while not keyboard.is_pressed('f13'):
                time.sleep(0.05) # Add this to reduce CPU usage

            play_round_start_audio()

            # Round 1 means a brand new match is starting - wipe the drawn rule pool so
            # this match gets a fresh random draw instead of reusing/excluding rules from
            # whatever match was played before it.
            if round_number == 1:
                rules_manager.start_new_match()

            # First ping Vercel for current scores
            _, latest_living_users, dead_users = get_passwords()
            latest_living_users = latest_living_users or [] # If null, set it to an empty array
            dead_users = dead_users or [] # If null, set it to an empty array
            print("[blue]Got latest info from server...")

            # The server stores living_users as an array - convert it into a dict for fast username lookup
            # Server format: [ { username: my_username, password: my_password, submission_timestamp: my_timestamp }, ... ]
            # New format: { my_username: { password: my_password }, ... }
            living_users = {}
            for user in latest_living_users:
                living_users[user['username']] = {'password': user['password']}
                # Note: the living users will NOT have a submission_timestamp field, that gets assigned when they submit a new valid password this round
                #       This lets us quickly check whether someone actually submitted anything at the end of the round,
                #       i.e. if there's still no submission_timestamp field, they didn't submit a password, and we auto fail them

            # Now grab the full rule descriptions based on this round number - this will be an array of arrays
            rule_descriptions = rules_manager.get_rule_descriptions(round_number)

            # Send the ruleset to Vercel so clients can see it
            # We also send an empty list of empty users, because once a round starts we don't want to display the "living users" until they've actually submitted a new valid pw.
            # Basically: we always show ALL people who failed, and we only show living people once they've successfully submitted in a round. One a new round begin again, they must earn their way back in.
            push_update(rule_descriptions, [], None, GameState.ACCEPTING_SUBMISSIONS, calculate_kill_counts(dead_users))  

            # Empty the check sets
            users_who_submitted_already.clear()
            previously_submitted_passwords.clear()

            # NOW THE ROUND TRULY BEGINS!

            # Start listening to Twitch messages and processing passwords
            print("[green]Listening to Twitch messages\n\n[cyan]Press F14 to end submissions")
            listening_to_chat = True

            # Wait until user presses = to end the round
            # However, also send updates to the server every few seconds while waiting
            start = time.time()
            seconds_per_update = 3
            while not keyboard.is_pressed('f14'):
                time.sleep(0.05)
                # Check if enough time has passed, if so, send update to server
                if time.time() - start >= seconds_per_update:
                    with password_check_lock:
                        dead_snapshot = list(dead_users) # Create a copy of the dead users to avoid any race conditions with the twitch chat updates
                        living_users_array = []
                        for username, user_info in living_users.items():
                            if "submission_timestamp" in user_info:
                                living_users_array.append({'username': username, 'password': " ", 'submission_timestamp': user_info['submission_timestamp']})
                       
                    # Kick off the server update on a separate thread, so that it doesn't block on this keyboard press checker
                    threading.Thread(
                        target=push_update,
                        args=(rule_descriptions, living_users_array, dead_snapshot, GameState.ACCEPTING_SUBMISSIONS, calculate_kill_counts(dead_snapshot)),
                        daemon=True
                    ).start()
                    start = time.time() # reset the timer

            print("[red]Stopped listening!!")
            listening_to_chat = False
            play_round_end_audio()

            # THE ROUND IS DONE! First cleanup, then send results to the server

            # Go through living_users, and fail anyone who did NOT submit a new password this round
            # Just check for a submission_timestamp field, since that's only present if they got a valid PW in
            for username, user_info in list(living_users.items()):
                if "submission_timestamp" not in user_info:
                    dead_guy = living_users.pop(username) # Remove them from living users list 
                    dead_users.insert(0, {'username': username, 'password': dead_guy['password'], 'submission_timestamp': int(time.time() * 1000), 'failure_message': DIDNT_SUBMIT_FAIL_MESSAGE })

            # Convert the living_users dictionary back into an array for server and storage
            living_users_array = []
            for username, user_info in living_users.items():
                living_users_array.append({'username': username, 'password': user_info['password'], 'submission_timestamp': user_info['submission_timestamp']})

            # Sort the living_users_array in order of password length
            living_users_array.sort(key=lambda u: len(u['password']))

            # Save everything to SQLite, just as a backup in case some shit goes wrong
            save_to_db("rules", json.dumps(rule_descriptions))
            save_to_db("living_users", json.dumps(living_users_array))
            save_to_db("dead_users", json.dumps(dead_users))

            # Finally, sends the updated list of users & scores to Vercel to store
            push_update(rule_descriptions, living_users_array, dead_users, GameState.INTERMISSION, calculate_kill_counts(dead_users))
            
            # Now that this round is finished, increment round number
            print(f"[yellow]FINISHED ROUND {round_number}")
            round_number += 1

            



# Creates a dict mapping each failure reason to the number of deaths
# This is passed as a separate piece of info because there are 2 ways to die that aren't part of a rule (submitting someone else's submission, or not submitting in time)
# Therefore we send this as a distinct piece of data to the server, and the client will display it appropriately
# Sorta janky but fuck it we ball, this was added last minute so architecture's a bit funky
def calculate_kill_counts(dead_users):
    # First figure out how many deaths in each category
    kill_counts = {}
    for user in dead_users:
        failure_message = user['failure_message']
        kill_counts[failure_message] = kill_counts.get(failure_message, 0) + 1
    return kill_counts

def get_passwords():
    r = requests.get(SERVER_URL)
    r.raise_for_status() # Checks the response code and raises an exception if it's 4xx or 5xx
    data = r.json() # requests method that parses the JSON body back into native python data types, so after this we're all set to use the data
    rules = data["rules"]
    living_users = data["livingUsers"]
    dead_users = data["deadUsers"]
    return rules, living_users, dead_users

def push_update(rules, living_users, dead_users, game_state=GameState.INTERMISSION, kill_counts={}):
    r = requests.post(
        SERVER_URL,
        json = {
			'clientSecret': CLIENT_SECRET,
			'rules': rules,
			'livingUsers': living_users,
			'deadUsers': dead_users,
            'gameState': game_state.value,
            'killCounts': kill_counts,
		}
    )
    r.raise_for_status()
    print('Updated scores (status:', r.status_code, ')')


# Optional sound effect help functions - you'll need to replace these with your own audio player and sounds
def play_round_start_audio():
    print("Playing start round audio!")
    # audio_manager.play_audio("sounds/se_menu_challenger_siren-30.wav", False, False, False)
    # audio_manager.play_audio("sounds/se_menu_watchfull_rise_crowd_l-40.wav", False, False, False)

def play_round_end_audio():
    print("Playing end round audio!")
    # audio_manager.play_audio("sounds/se_menu_tournament_winner_cheer_long-40.wav", False, False, False)
    # audio_manager.play_audio("sounds/se_menu_challenger_join-30.wav", False, False, False)

def play_valid_password_sound():
    print("Playing valid password submission audio!")
    # audio_manager.play_audio("sounds/se_menu_edgechallenge_cursor-30.wav", False, False, False)

def play_invalid_password_sound():
    print("Playing invalid password submission audio!")
    # audio_manager.play_audio("sounds/se_menu_movieedit_undo-30.wav", False, False, False)

def startTwitchBot():
    global twitchbot
    asyncio.set_event_loop(asyncio.new_event_loop()) # Create and set the event loop for this thread
    twitchbot = TwitchBot()
    twitchbot.run() # Kicks off the Twitchio connection

def start_bot(bot):
    bot.run()

if __name__=='__main__':
    
    # Thread that listens to chat messages
    chat_bot_thread = threading.Thread(target=startTwitchBot)
    chat_bot_thread.start()

    # Thread that listens for hotkey presses from Doug
    keypress_bot = KeyPressBot()
    keypress_bot_thread = threading.Thread(target=start_bot, args=(keypress_bot,))
    keypress_bot_thread.start()
    
    while True:
        time.sleep(1000) # there is probably a better way to handle main thread but fuck it that is a problem for a future project

