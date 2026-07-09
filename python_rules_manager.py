'''
RulesManager - draws a random ruleset for each round instead of following a
hand-authored per-match script (see python_rule_pool.py for the pool itself
and the reasoning behind tiers/excludes).

Randomization is done LAZILY, one round at a time, the first time that round
number is asked about (via get_rule_descriptions or is_valid_password). Once
a round's rules are drawn they're locked in for the rest of the match - the
same round number will always return the same rules.

Rounds are generated with an increasing "tier ceiling" so the game still
ramps up in difficulty even though the specific rules are randomized, and a
rule already used earlier in the match is never drawn again. Two rules that
are marked as mutually exclusive (see "excludes" in the pool) will never be
drawn into the same round.

Whenever a brand new match starts, call start_new_match() to wipe the drawn
rules and let the pool start fresh.
'''

import json
import random
from rich import print
from python_rule_pool import RULE_POOL, RULE_LOOKUP
from sqlite_helper import get_all_values, save_to_db

RULE_POOL_STATE_KEY = "rule_pool_state"

# Rules per round mirrors the old hand-authored matches: round 1 is always a single
# easy rule, every round after that has a 50/50 chance of throwing in a 2nd rule.
def _num_rules_for_round(round_number: int) -> int:
    if round_number <= 1:
        return 1
    return random.choice([1, 2])

# Controls how hard the rules drawn for a given round are allowed to be.
# Ramps up over the course of a match, same shape as the old hand-authored matches.
def _tier_ceiling_for_round(round_number: int) -> int:
    if round_number <= 1:
        return 1
    if round_number <= 3:
        return 2
    if round_number <= 6:
        return 3
    if round_number <= 9:
        return 4
    return 5


class RulesManager():
    def __init__(self):
        print("[blue]Rules Manager now running")
        self.generated_rounds: dict[int, list[dict]] = {}  # round_number -> list of rule dicts (with "method")
        self.used_rule_ids: set[str] = set()
        self._load_persisted_state()

    # Wipes any drawn rules - call this whenever a genuinely new match is starting
    # (e.g. when Doug resets round_number back to 1 for a fresh game).
    def start_new_match(self):
        self.generated_rounds = {}
        self.used_rule_ids = set()
        save_to_db(RULE_POOL_STATE_KEY, json.dumps(self._to_persisted_dict()))
        print("[blue]Rules pool reset for new match")

    # Draws the rules for a single round, respecting tier ceiling, "used already this
    # match", and mutual-exclusion constraints.
    #
    # Exclusions are checked against every rule active ANYWHERE in the match so far
    # (not just this round) - rules accumulate round over round, so a rule drawn in
    # round 3 is still in effect in round 8. If exclusions were only checked within a
    # single round, two contradictory rules could end up both active at once just by
    # landing in different rounds.
    def _generate_round(self, round_number: int) -> list[dict]:
        tier_ceiling = _tier_ceiling_for_round(round_number)
        num_rules = _num_rules_for_round(round_number)

        active_excludes = set()
        for rule_id in self.used_rule_ids:
            active_excludes.update(RULE_LOOKUP[rule_id].get("excludes", []))

        def conflicts_with_active(rule) -> bool:
            if rule["id"] in active_excludes:
                return True
            return any(excluded_id in self.used_rule_ids for excluded_id in rule.get("excludes", []))

        candidates = [
            rule for rule in RULE_POOL
            if rule["id"] not in self.used_rule_ids
            and rule["tier"] <= tier_ceiling
            and not conflicts_with_active(rule)
        ]
        # Fallback: if we've drained the pool at/under this tier ceiling, allow any unused,
        # non-conflicting rule regardless of tier
        if len(candidates) < num_rules:
            candidates = [
                rule for rule in RULE_POOL
                if rule["id"] not in self.used_rule_ids and not conflicts_with_active(rule)
            ]

        random.shuffle(candidates)
        chosen: list[dict] = []
        for rule in candidates:
            if len(chosen) >= num_rules:
                break
            conflicts_with_chosen = any(
                rule["id"] in already_chosen.get("excludes", []) or already_chosen["id"] in rule.get("excludes", [])
                for already_chosen in chosen
            )
            if conflicts_with_chosen:
                continue
            chosen.append(rule)

        self.used_rule_ids.update(rule["id"] for rule in chosen)
        return chosen

    # Makes sure every round from 1 up through round_number has been drawn, generating
    # (and persisting) any that are still missing.
    def _ensure_rounds_generated(self, round_number: int):
        newly_generated = False
        for round_num in range(1, round_number + 1):
            if round_num not in self.generated_rounds:
                self.generated_rounds[round_num] = self._generate_round(round_num)
                newly_generated = True
        if newly_generated:
            save_to_db(RULE_POOL_STATE_KEY, json.dumps(self._to_persisted_dict()))

    # Fields on a pool entry that are purely internal to rule selection and should
    # never be sent to the frontend (which only reads description/subtitle/image).
    _INTERNAL_ONLY_FIELDS = ("id", "method", "excludes", "tier")

    # Puts all of the current rule descriptions (up to current round number) in an array
    # Basically the drawn rules, minus the internal-only selection metadata
    def get_rule_descriptions(self, round_number: int):
        self._ensure_rounds_generated(round_number)
        output = []
        for round_num in range(1, round_number + 1):
            round_rules = [
                {k: v for k, v in rule.items() if k not in self._INTERNAL_ONLY_FIELDS}
                for rule in self.generated_rounds[round_num]
            ]
            output.append(round_rules)
        return output

    # Runs the password through all drawn rules up to the current round
    # If any of the "validity" functions fail, we return False and the reason why
    def is_valid_password(self, round_number: int, password: str):
        self._ensure_rounds_generated(round_number)
        for round_num in range(1, round_number + 1):
            for rule in self.generated_rounds[round_num]:
                if not rule["method"](password):
                    return False, rule["description"]
        return True, None

    # --- persistence, so restarting the game manager mid-match doesn't re-roll rounds that
    # have already been played (which would desync from what chat already saw/satisfied) ---

    def _to_persisted_dict(self) -> dict:
        return {
            str(round_num): [rule["id"] for rule in rules]
            for round_num, rules in self.generated_rounds.items()
        }

    def _load_persisted_state(self):
        try:
            rows = get_all_values()
        except Exception:
            return  # DB/table doesn't exist yet (e.g. very first run) - nothing to restore
        for row in rows:
            if row["key"] == RULE_POOL_STATE_KEY:
                data = json.loads(row["value"])
                self.generated_rounds = {}
                self.used_rule_ids = set()
                for round_str, rule_ids in data.items():
                    self.generated_rounds[int(round_str)] = [RULE_LOOKUP[rid] for rid in rule_ids if rid in RULE_LOOKUP]
                    self.used_rule_ids.update(rule_ids)
                if self.generated_rounds:
                    print(f"[blue]Restored {len(self.generated_rounds)} previously-drawn round(s) from local backup")
                return
