# SIGNUPS
# Run this one time, it'll create a list of users who type !join, then send that to vercel as our starting list of users
# Technically this could have been combined into python_game_loop, but decided to make this a separate script for simplicity

import os
import time
from twitchio.ext import commands
from twitchio import *
import asyncio
import threading
import os
import keyboard
import time
import json
from rich import print

from sqlite_helper import create_tables, save_to_db
from python_game_loop import push_update, GameState, play_round_start_audio, play_round_end_audio


listening_to_chat = False # Flag that says "We're accepting signups for this round"

# Our list of people who sign up, that we'll send to vercel once we're done
new_users = {}
# OPTIONAL TEST DATA
# new_users = { 
# 	'username1': { 'password': 'testing signup', 'submission_timestamp': 1777687011295 },
# }

class TwitchBot(commands.Bot):
    def __init__(self):
        self.CHANNEL_NAME = 'dougdoug'
        super().__init__(token=os.getenv('TWITCH_ACCESS_TOKEN'), prefix='?', initial_channels=[self.CHANNEL_NAME]) #connects to twitch channel
    
    async def event_ready(self):
        print(f'[green]Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        await self.process_message(message)

    async def process_message(self, message: Message):
        global listening_to_chat
        username = message.author.name
        message = message.content.lower()
        if listening_to_chat:
            
            # Check if they're trying to sign up
            if not message.startswith("!join") and not message.startswith('join'): 
                return

            # Add them to the new signups pool
            if username not in new_users:
                new_users[username] = { 'password': 'Signed Up!', 'submission_timestamp': int(time.time() * 1000) }
                print(f"added {username} to the new_users pool")



class KeyPressBot():
    def __init__(self):
        print("[blue]Keypress bot running!")

    def run(self):
        global listening_to_chat, new_users

        while True:

            # Wait until user presses -
            print("[yellow]\n\nPress F13 to begin SIGNUPS")
            while not keyboard.is_pressed('f13'):
                time.sleep(0.05)

            play_round_start_audio()
            
            # Push updated GameState to server, so that it knows we're now accepting submissions
            push_update(None, None, None, GameState.ACCEPTING_SUBMISSIONS, {})
            
            # Start listening to Twitch messages and processing signups
            print("[green]Listening for signup messages\n\n[cyan]Press F14 to end submissions")
            listening_to_chat = True

            # Wait until user presses = to end signups
            # However, also send updates to the server every few seconds while waiting so you can see people joining up
            start = time.time()
            seconds_per_update = 3
            while not keyboard.is_pressed('f14'):
                time.sleep(0.05)
                # Check if enough time has passed, if so, send update to server
                if time.time() - start >= seconds_per_update:
                    # Kick off the server update on a separate thread, so that it doesn't block on this keyboard press checker
                    signups_array = []
                    for username, user_info in new_users.items():
                        signups_array.append({'username': username, 'password': user_info['password'], 'submission_timestamp': user_info['submission_timestamp']})
                    threading.Thread(
                        target=push_update,
                        args=([], signups_array, [], GameState.ACCEPTING_SUBMISSIONS, {}),
                        daemon=True
                    ).start()
                    start = time.time() # reset the timer

            print("[red]Stopped signups!!")
            listening_to_chat = False
            play_round_end_audio()

            # THE ROUND IS DONE! First cleanup, then send results to the server

            # Convert the our signups dictionary into an array for the server
            new_users_array = []
            for username, user_info in new_users.items():
                new_users_array.append({'username': username, 'password': user_info['password'], 'submission_timestamp': user_info['submission_timestamp']})

            # Save user list to SQLite, just as a backup in case some shit goes wrong
            create_tables()
            save_to_db("living_users", json.dumps(new_users_array))

            # Finally, sends the list of new users to Vercel to store and display
            # We send an empty array for rules and dead_users, so that our 1st round correctly starts with those being empty
            push_update([], new_users_array, [], GameState.INTERMISSION, {})

            print(f"[green]\n   SIGNUPS ARE FINISHED  \n")


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
        time.sleep(1000)

