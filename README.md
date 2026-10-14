# NOTE: THIS IS A FORK OF DOUGDOUG'S ORIGINAL REPO, I HAVE MERELY ADDED MORE PROMPTS, A LEADERBOARD TO TRACK USERS TOTAL WINS AND MORE


# Battle Royale Password

A Twitch game where viewers submit passwords that must following an increasingly complex set of rules. Inspired by Neal.fun!

This is shared for educational purposes, feel free to use it however you'd like, no need for permission. Currently there are no future development plans so major pull requests will probably not be reviewed, but feel free to go make your own fork!


## Gameplay

- Each Match begins with a signup phase, where viewers join by typing !join
- Each Match then cycles through ~10 rounds of rules
- During each round, the remaining users must submit a password that passes ALL the current rules. If their password breaks any rules, or they copy another valid password, or they do not submit in time, they are eliminated from the game.
- This continues until someone has achieved a Dick Bear password

## Infrastructure

### Client
- Vanilla HTML, css, js that pings the server for the latest info and displays a title, the current rules, the current "living users", and the current "dead users"
- Pings the server at a set interval to ask for latest info

### Server
- Vercel server. Takes POST requests that will update the game data, and takes GET requests to send latest data to client
- Stores data in a REDIS database. This was setup using Upstash for Redis on the Vercel website

### Python Game Manager
- Local python scripts that store the rules and manage the state of the actual game. These are run by the game manager (e.g. Doug) during the game itself
- Reads twitch chat messages, processes living and dead users, and sends updates to the server

## Specific Files

Anything starting with "python" are the python game manager classes

**`python_game_signups.py`**
- Runs the signups phase

**`python_game_loop.py`**
- Runs the core game loop

**`python_rules.py`**
- Stores all the rule definitions and validation functions

**`python_constants.py`**
- List of all the constants that we'll check against (e.g. list of all State Capitals)

**`python_restore_from_backup.py`**
**`sqlite_helper.py`**
- These are optional, we store backups of the latest user info in SQLite just as a sort of emergency in case something went wrong on the server

Vercel API

**`/api/passwords.js`**
- Vercel API route that handles GET and POST request with the latest data

**`/api/_lib/passwords.js`**
- Quick helper function for Redis DB

Client Frontend

**`index.html`**
- Defines the layout of the frontend

**`/src/style.css`**
- My very very good and very professional CSS styling file

**`/src/main.js`**
- Grabs latest info from server, updates the visuals

**`/src/animated-bg.js`**
- Runs the star tunnel animated background, this is one thing that's basically just written by Ai, I'm still confused by it because of my smooth brain



## Setting this up for yourself

Currently this isn't something you can just play with your friends, you'd need to set up a Vercel server yourself, THEN would need to run the python scripts locally on a PC while your friends look at the website. If you're interested in this, here's the general steps:

1. Create a Twitch Access token
  - Basically you need permission from Twitch in order to read messages from a Twitch chat. You can create an auth token pretty easily here: https://twitchtokengenerator.com/

2. Install python and the various dependencies of these scripts

3. Install Node.js (not technically necessary, but you'd use this to run and test the web app locally)

3. Create a new app on Vercel, using this codebase as the project code

4. Set up the Redis DB. This can be done within Vercel via the Storage tab, I used Upstash for Redis on a Pay As You Go plan. If you do the same setup, it should all connect together pretty easily.

5. Once Vercel is set up, create a new environment variable on Vercel called UPDATE_DB_KEY. You can set it to whatever you want. Then link your local project to Vercel and pull the environment variables. In plain english, you need to set a value that gives someone permission to update the database - you then need to make sure your python code has access to that value so that it can update the server.

6. Once your Vercel website is up and running, you (the game master) would start and run the game by running `python_game_signups.py` and then `python_game_loop.py` locally. The players would participate by typing messages into the Twitch channel that you're listening to, and/or looking at the Vercel website

If you're new to programming you'll probably need some help for the steps above, but fortunately ChatGPT or Claude or your Ai of choice can explain what's going on in each of these steps and walk you through it. It's not insanely hard, but it'll take a bit of work. Good luck!
