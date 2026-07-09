# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Twitch chat game ("Battle Royale Password", inspired by Neal.fun) run live by a streamer (Doug). Viewers join by typing `!join`, then submit passwords via `!p <password>` that must satisfy an increasingly complex, accumulating set of rules each round. Anyone who breaks a rule, submits a duplicate of another valid password, or misses the submission window is eliminated.

This is a hobby/stream-support project, not a product with a release process — there is no test suite, linter, or CI. Treat correctness verification as "read the code carefully" / manual testing during a live game, not automated tests.

## Three independently-run pieces

1. **Python game manager** (run locally by the streamer during the actual game) — owns all game logic and state.
2. **Vercel serverless API** (`/api/passwords.js`) — a dumb read/write proxy over Redis. Has no game logic.
3. **Vite static frontend** (`/src`) — polls the API and renders the current rules/living/dead users. Has no game logic either.

The Python side is the only "brain": it decides who lives, who dies, and what the rules are, then POSTs the full resulting state to the API. The frontend just polls and redraws. When changing game behavior, look in the Python files first — `api/` and `src/` are display/transport layers only.

## Commands

- `npm run dev` — start the Vite dev server (proxies `/api/*` to `http://localhost:3000`, see `vite.config.js`)
- `npm run build` — production build to `dist/`
- `npm run preview` — preview the production build
- Running the API locally requires the Vercel CLI (`vercel dev`) so `/api/passwords.js` is served on port 3000 for the Vite proxy to reach.
- Python scripts have no dependency manifest in-repo; required packages (inferred from imports) are `twitchio`, `requests`, `keyboard`, `python-dotenv`, `rich`, `emoji`. Run them directly, e.g. `python python_game_signups.py`.
- No test suite, linter, or type checker exists in this repo.

## Environment / secrets

- Vercel env vars `KV_REST_API_URL` / `KV_REST_API_TOKEN` (Upstash Redis) are read by `api/_lib/redis.js`.
- `UPDATE_DB_KEY` is a shared secret: the API rejects POSTs whose `clientSecret` doesn't match `process.env.UPDATE_DB_KEY`. The Python side loads the same value from a local `.env.local` via `python-dotenv`.
- The Python bot also needs `TWITCH_ACCESS_TOKEN` (env var) to connect to Twitch chat.
- Two more `.env.local` vars are optional and exist purely for local testing without touching production: `SERVER_URL` (defaults to the live Vercel URL — point it at `http://localhost:3000/api/passwords` to hit a local `vercel dev` instead) and `TWITCH_CHANNEL_NAME` (defaults to `dougdoug` — point it at a test/alt channel to avoid real viewers). Both are read in `python_game_loop.py` and reused by `python_game_signups.py`.

## Game manager architecture (Python)

Two scripts are run manually, in order, by the streamer during a live game — each spins up two threads: a TwitchIO chat bot listening for chat commands, and a `KeyPressBot` that waits on global hotkeys (F13 = start phase, F14 = end phase) so the streamer controls pacing live.

- **`python_game_signups.py`** — signup phase. Listens for `!join`/`join`, builds a dict of new users, and on F14 POSTs the initial `livingUsers` list to the server. Imports `push_update`/`GameState` from `python_game_loop.py` (signups is really a thin wrapper around the same push mechanism).
- **`python_game_loop.py`** — the core round loop and the source of truth for the POST protocol:
  - `MATCH_NUMBER` and `round_number` (how many rounds of rules are active) are **module-level globals set/incremented manually**. `round_number` drives which rules are in play; `MATCH_NUMBER` is now just Doug's own bookkeeping label (rules are drawn randomly, not selected by match number — see `python_rule_pool.py` below). There's no separate persisted "current match" state beyond the rule pool's own SQLite backup (see below), so if you resume a game after a restart you must still reset `MATCH_NUMBER`/`round_number` by hand to match reality.
  - Setting `round_number = 1` and pressing F13 triggers `RulesManager.start_new_match()`, which wipes the previously-drawn rules so the new match draws a fresh random set instead of excluding rules already used by the last match.
  - On each F13→F14 cycle: pulls current state from the server, opens the chat submission window, validates each submitted password against `RulesManager.is_valid_password()` for **all rules up to the current round** (rules accumulate, they don't replace each other), tracks first-come-first-served password uniqueness via `previously_submitted_passwords` to catch copiers, and at F14 auto-fails anyone who never got a valid submission in that round.
  - `push_update()` is the single POST helper — the same function used by every script that talks to the server, including `python_restore_from_backup.py`.
  - Deliberately sends an empty `livingUsers` array at the start of a round (until people re-submit) so chat can't see who's still alive / read off currently-valid passwords mid-round — copying is only preventable if valid passwords aren't visible.
- **`python_rules.py`** — home for the rule *validator functions* only (prefixed `r_`), pure `str -> bool` predicates with no knowledge of rounds/matches/tiers. To add a new rule: write one of these, then add a matching entry to `RULE_POOL` in `python_rule_pool.py` — no other file needs to change.
- **`python_rule_pool.py`** — `RULE_POOL` is a flat list of every rule in the game (replaces the old per-match `MATCH_RULES` nested structure). Each entry is a dict with a stable `id`, `description` (uses `{curly braces}` to mark the part the frontend highlights), optional `subtitle`/`image`, `method` (the validator function), a `tier` (1–5 rough difficulty, controls when a rule is eligible to be drawn), and an optional `excludes` list of other rule ids that can never be active in the same match at the same time (e.g. directly contradictory rules like "vowels cannot be capitalized" vs "all vowels must be capitalized").
- **`python_rules_manager.py`** — `RulesManager` draws rules **randomly** from `RULE_POOL` instead of following a hand-authored sequence, one round at a time and lazily (the first time a round number is asked about), then locks that draw in for the rest of the match. Difficulty still ramps up over a match via an increasing tier ceiling per round (`_tier_ceiling_for_round`), and `excludes` is checked against every rule already active anywhere earlier in the match — not just the current round — since rules accumulate. `id`/`method`/`excludes`/`tier` are stripped out before a rule is sent to the client (`get_rule_descriptions`), same as before. Draws are persisted to SQLite (`rule_pool_state` key) after every round so that restarting the Python process mid-match restores the exact same previously-drawn rules instead of re-rolling them (which would desync from what chat already saw/satisfied) — `start_new_match()` clears this state to start a fresh draw.
- **`python_constants.py`** — large lookup lists (state names, Pokémon by generation, emoji sets, etc.) referenced by the `r_*` validators. Case handling is inconsistent by design per-rule (see comments in `python_rules.py` — most matching is case-insensitive, some rules explicitly care about case).
- **`sqlite_helper.py`** — a single generic key/value table (`passwords`, columns `key`/`value`). Mostly a local emergency backup written after every round and not read during normal operation, with one exception: the `rule_pool_state` key written by `RulesManager` *is* read back on startup, to restore already-drawn rounds after a restart.
- **`python_restore_from_backup.py`** — one-shot recovery script: reads the last-saved rules/living/dead users out of SQLite and re-POSTs them to the server if the Vercel/Redis state gets corrupted mid-match. Also restores the leaderboard if a backup of it exists locally, but won't block the restore if it doesn't (unlike rules/living/dead users, which are required).
- **Leaderboard** — unlike everything else Python tracks, this *persists across matches* rather than resetting each one. `update_leaderboard()` in `python_game_loop.py` is called exactly once per match, at the moment it concludes (0 or 1 `living_users` remaining after a round) — guarded by the `leaderboard_finalized_this_match` flag (reset on `round_number == 1`) so replaying extra rounds after a match is already decided can't double-count a result. It tracks per-username `wins`/`matchesPlayed`, plus an all-time `lifetimeKillCounts` (same shape as the existing per-round `killCounts`, just never reset). Fetched from the server each round via `get_passwords()`, only pushed back to the server (and backed up to SQLite under the `"leaderboard"` key) on the round where a match actually finishes.

## API / data model (`api/passwords.js`, `api/_lib/redis.js`)

Redis stores each piece of state as a plain JSON *string* under its own key (not a hash) — see the large comment block at the top of `api/passwords.js` for the exact shapes of `REDIS_KEY_RULES`, `REDIS_KEY_LIVING_USERS`, `REDIS_KEY_DEAD_USERS`, `REDIS_KEY_GAME_STATE`, `REDIS_KEY_KILL_COUNTS`, `REDIS_KEY_LEADERBOARD`. String was chosen over hash deliberately because the access pattern is always "read/write the whole collection," never a single field.

- `GET` — rate-limited per-IP (120 req/10s via `@upstash/ratelimit`), supports `?since=<timestamp>` so the client can skip a response body (`noNewData: true`) when nothing changed since its last poll — checked against `REDIS_KEY_LAST_UPDATED_TIMESTAMP`.
- `POST` — requires `clientSecret` to match `UPDATE_DB_KEY`; only the Python game manager should ever POST. Any subset of fields (`rules`, `livingUsers`, `deadUsers`, `gameState`, `killCounts`, `leaderboard`) can be updated independently; whichever are present get pipelined into Redis together (`redis.multi()`), and the last-updated timestamp is bumped only if something actually changed. Falsy fields (including `null`) are silently skipped rather than clearing the stored value — this is why Python only sends a non-null `leaderboard` on the round a match actually concludes.
- There is no schema validation on POST bodies — the Python side is trusted to send well-formed data.

## Frontend (`src/main.js`, `src/style.css`, `src/animated-bg.js`)

- **Two-page Vite build**: `index.html` (the game, `src/main.js`) and `leaderboard.html` (the persistent leaderboard, `src/leaderboard.js`) are separate entry points, both listed in `vite.config.js`'s `build.rollupOptions.input` — forgetting to list a new page there means `npm run build` silently drops it from `dist/`. The two pages don't share JS; `index.html` just links to `/leaderboard.html` (opens in a new tab) rather than embedding it, since the leaderboard doesn't reset with the game and was cluttering the live match view.
- `src/theme.css` holds the shared design tokens (`--bg`, `--text`, `--primary`, `--font`, etc.) and base `body`/`:root` rules — both `src/style.css` (game page) and `src/leaderboard.css` (leaderboard page) `@import` it so the two pages stay visually consistent. Theme is dark background with a purple accent color, font is JetBrains Mono everywhere (loaded via Google Fonts `<link>` in each HTML file, referenced through `var(--font)`).
- Polls `/api/passwords` every 2 seconds (`TIME_PER_POLL`), tracking `lastCheckTimestamp` to use the `?since=` short-circuit. Both pages poll independently — `leaderboard.js` only reads `data.leaderboard`.
- Rendering is plain DOM manipulation (`document.createElement`, `DocumentFragment`) — no framework, no virtual DOM. Each `handleNew*` function fully wipes and rebuilds its container from scratch on every update; there's no diffing.
- Rule descriptions use `{curly brace}` markup that gets regex-replaced into `<span class="rule-highlight">` — this convention is defined in `python_rules.py` rule descriptions and consumed in `handleNewRules()`. `leaderboard.js` strips the same markup (plain text, no highlighting) since death-cause reasons reuse rule descriptions verbatim.
- `animated-bg.js` (the star-tunnel background, reused on both pages) and the title letter animation (via CDN-loaded `letterizejs`/`animejs` in `main.js`, game page only) are cosmetic and can be treated as a black box — noted in the README as effectively AI-generated and not well understood by the maintainer.
- Game state (`ACCEPTING_SUBMISSIONS` vs `INTERMISSION`) drives CSS classes and background animation speed/opacity via `handleNewGameState()` on the game page.
