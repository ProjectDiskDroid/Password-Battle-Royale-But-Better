'''
THE RULE POOL

This is the flat, de-duplicated list of every rule that can show up in a game.
It replaces the old per-match MATCH_RULES structure - instead of hand-ordering
rules into fixed matches, RulesManager (see python_rules_manager.py) draws
randomly from this pool each round.

TO ADD A NEW RULE:
    1. Write a validator function in python_rules.py (prefixed `r_`), taking a
       password string and returning True/False.
    2. Add one dict to RULE_POOL below. That's it - no need to slot it into a
       specific match/round by hand.

Each entry:
    id            - stable unique string, used for exclusions + save/restore. Never reuse an id.
    description   - shown to players. Use {curly braces} to mark the part the frontend highlights.
    subtitle      - optional extra clarifying text.
    image         - optional image URL for picture-clue rules.
    method        - the validator function from python_rules.py.
    tier          - rough difficulty, 1 (easiest) to 5 (hardest). Controls when a rule is
                    allowed to be drawn - see _tier_ceiling_for_round in python_rules_manager.py.
    excludes      - list of other rule ids that cannot be active in the same match at the same
                    time as this one (e.g. directly contradictory rules). Optional, defaults to [].
'''

from python_rules import *

RULE_POOL = [
    {
        "id": "5_characters",
        "description": "Must contain {5+ Characters}",
        "method": r_5_characters,
        "tier": 1,
    },
    {
        "id": "1_uppercase_1_special",
        "description": "Must include {1+ Uppercase Letter} and {1+ Special Character}",
        "method": r_1_uppercase_1_special,
        "tier": 1,
    },
    {
        "id": "1_digit",
        "description": "Must include {1+ Digit}",
        "method": r_1_digit,
        "tier": 1,
    },
    {
        "id": "us_state",
        "description": "Must include the name of a {US State}",
        "subtitle": "Full names, no abbrevations",
        "method": r_us_state,
        "tier": 2,
    },
    {
        "id": "5_letter_e",
        "description": "Must contain *exactly* {5 Letter e's}",
        "method": r_5_letter_e,
        "tier": 3,
    },
    {
        "id": "gen1_pokemon",
        "description": "Must include name of a {Gen 1 Pokemon}",
        "subtitle": "Cannot be fire, water, or grass. Cannot be ugly (according to my gf)",
        "method": r_gen1_pokemon,
        "tier": 2,
    },
    {
        "id": "french_language",
        "description": "Must include country with {French} as an official national language",
        "subtitle": "Full country names. Must be official as of 2026",
        "method": r_french_language,
        "tier": 2,
    },
    {
        "id": "same_digits_emojis",
        "description": "Must contain same number of {Digits} and {Emojis}",
        "method": r_same_digits_emojis,
        "tier": 3,
    },
    {
        "id": "mario64",
        "description": "Must include the name of {This Game}",
        "image": "https://i.gyazo.com/7190a344ed514495ceb5ee7a736b01d4.png",
        "method": r_mario64,
        "tier": 2,
    },
    {
        "id": "minecraft_block",
        "description": "Must include {Number of Hits} it takes to kill {Both Cows}",
        "subtitle": "With your fists. No crits, no potions.",
        "image": "https://i.gyazo.com/1c61b6cad63e621c7717e4a4cc21dd85.png",
        "method": r_minecraft_block,
        "tier": 2,
    },
    {
        "id": "7_emojis",
        "description": "Must contain exactly {7 Emojis}",
        "subtitle": "Official emojis, not wingdings",
        "method": r_7_emojis,
        "tier": 3,
    },
    {
        "id": "include_cat_mouse",
        "description": "Must include a {Cat} and {Mouse} Emoji",
        "subtitle": "Computer Mouse doesn't count",
        "method": r_include_cat_mouse,
        "tier": 3,
    },
    {
        "id": "no_duplicate_emojis",
        "description": "Must contain {No Duplicate Emojis}",
        "method": r_no_duplicate_emojis,
        "tier": 3,
    },
    {
        "id": "cat_mouse_not_next_to_each_other",
        "description": "{Cat} and {Mouse} emojis cannot be next to each other",
        "subtitle": "They might start fighting",
        "method": r_cat_mouse_not_next_to_each_other,
        "tier": 3,
    },
    {
        "id": "most_common_chat_words",
        "description": "Must include 1 of the {Top 10 Most Commonly Said Words} from Doug's Chat",
        "subtitle": "Must be at least 5 characters long",
        "method": r_most_common_chat_words,
        "tier": 3,
    },
    {
        "id": "no_duplicate_digits",
        "description": "Must contain {No Duplicate Digits}",
        "method": r_no_duplicate_digits,
        "tier": 3,
    },
    {
        "id": "sun_moon_pokemon",
        "description": "Must include name of a {Pokemon} from ☀️🌕's generation",
        "subtitle": "No fire, water, or grass types",
        "method": r_sun_moon_pokemon,
        "tier": 3,
    },
    {
        "id": "twitch_global_emote",
        "description": "Must include a {Twitch Global Emote} that is 4+ characters",
        "subtitle": "Capitalization matters.",
        "method": r_twitch_global_emote,
        "tier": 3,
    },
    {
        "id": "even_num_characters",
        "description": "Must contain an {Even Number of Characters}",
        "subtitle": "Warning: some emojis are multiple characters (family, flags, color variants)",
        "method": r_even_num_characters,
        "tier": 2,
    },
    {
        "id": "5_capital_d",
        "description": "Must contain exactly {5 capital D} letters",
        "method": r_5_capital_d,
        "tier": 2,
    },
    {
        "id": "name_of_fast_food_chain",
        "description": "Must include name of a {Top 10 USA Fast Food Chain}",
        "subtitle": "Ranked by total market share",
        "method": r_name_of_fast_food_chain,
        "tier": 2,
    },
    {
        "id": "capitals_in_first_half",
        "description": "Any {Capital Letters} must be in {1st Half of Password}",
        "method": r_capitals_in_first_half,
        "tier": 2,
    },
    {
        "id": "proboscis_monkey_pic",
        "description": "Include the name of this {Animal}",
        "image": "https://i.gyazo.com/ceb849fe3020d66e9ee04c86f98132b3.png",
        "method": r_proboscis_monkey_pic,
        "tier": 2,
    },
    {
        "id": "tarsier_pic",
        "description": "Also include this {Animal}",
        "image": "https://i.gyazo.com/d6ad9fab92171e51be4c6b8770620cec.png",
        "method": r_tarsier_pic,
        "tier": 2,
    },
    {
        "id": "d_face_emote",
        "description": "What do you type into Twitch Chat to make {This Emote}",
        "image": "https://i.gyazo.com/56ca77098e420023f1c87e70c8df609f.png",
        "method": r_d_face_emote,
        "tier": 2,
    },
    {
        "id": "gen_alpha_slang",
        "description": "Must include one of {75 Most Popular Gen Alpha Slang}",
        "subtitle": "Based off of what Doug could find online",
        "method": r_gen_alpha_slang,
        "tier": 2,
    },
    {
        "id": "equal_D_and_digits",
        "description": "Must contain equal number of {Capital D's} and {Digits}",
        "method": r_equal_D_and_digits,
        "tier": 3,
    },
    {
        "id": "6_7_cannot_be_next_to_another",
        "description": "Why is {6} afraid of {7}? Because {7} ate {9}",
        "subtitle": "Therefore, 6 and 7 digits cannot be next to each other",
        "method": r_6_7_cannot_be_next_to_another,
        "tier": 2,
    },
    {
        "id": "digits_cannot_be_next_to_another",
        "description": "{Numbers} can not be next to each other",
        "subtitle": "Another character must be inbetween them",
        "method": r_digits_cannot_be_next_to_another,
        "tier": 4,
    },
    {
        "id": "equal_e_in_both_halves",
        "description": "Must contain equal number of {letter E} in both halves of password",
        "subtitle": "Capitalization doesn't matter",
        "method": r_equal_e_in_both_halves,
        "tier": 3,
    },
    {
        "id": "top_10_youtube_channel",
        "description": "Must include 1 of {10 biggest Youtube channels} by sub count",
        "subtitle": "Must match channel name EXACTLY",
        "method": r_top_10_youtube_channel,
        "tier": 4,
    },
    {
        "id": "dougs_biggest_channel",
        "description": "Must include name of {Doug's biggest Youtube channel} by sub count",
        "subtitle": "Must match channel name EXACTLY",
        "method": r_dougs_biggest_channel,
        "tier": 4,
    },
    {
        "id": "cute_character_v1",
        "description": "Must include a cute character like {<(^_^<)}",
        "subtitle": "Just need open/closed parenthesis. Chat must think it's REALLY cute.",
        "method": r_cute_character_v1,
        "tier": 1,
    },
    {
        "id": "banjo_kazooie",
        "description": "Must include the {Console Name} this was released on",
        "image": "https://i.gyazo.com/57b9e4e155e2b0b85c3890afebe8698f.png",
        "method": r_banjo_kazooie,
        "tier": 2,
    },
    {
        "id": "half_capital_letters",
        "description": "At least half of Password must be {Capital Letters}",
        "method": r_half_capital_letters,
        "tier": 2,
    },
    {
        "id": "pancake_ingredients",
        "description": "Must include one of the {5 Most Important Ingredients for Pancakes}",
        "method": r_pancake_ingredients,
        "tier": 2,
    },
    {
        "id": "funny_meme_numbers",
        "description": "Must include one of the {Funny Meme Numbers}",
        "method": r_funny_meme_numbers,
        "tier": 2,
    },
    {
        "id": "digits_add_to_twentyfive",
        "description": "All {Digits} must add up to {25}",
        "method": r_digits_add_to_twentyfive,
        "tier": 4,
    },
    {
        "id": "nickname_for_penis",
        "description": "Must include a nickname for {Penis}",
        "subtitle": "Doug thought of 10 and found 30 more online",
        "method": r_nickname_for_penis,
        "tier": 2,
    },
    {
        "id": "vowels_not_capitalized",
        "description": "{Vowels} cannot be capitalized",
        "subtitle": "Y is a vowel",
        "method": r_vowels_not_capitalized,
        "tier": 3,
        "excludes": ["all_vowels_capitalized"],
    },
    {
        "id": "bear_wikipedia",
        "description": "Must include the title of {This Wikipedia Page}",
        "image": "https://i.gyazo.com/49fcc5885d5a155fc1533f266460879f.png",
        "method": r_bear_wikipedia,
        "tier": 2,
    },
    {
        "id": "big_mac_ingredients",
        "description": "Must include one of the main ingredients to a {McDonald's Big Mac}",
        "subtitle": "Must use McDonald's official name",
        "method": r_big_mac_ingredients,
        "tier": 2,
    },
    {
        "id": "cute_guy_v2",
        "description": "Also, add another {cute little guy} for Twitch Chat {<(^_^<)}",
        "subtitle": "It has to be different, plus open/closed parenthesis, AND Chat must think it's cute.",
        "method": r_cute_guy_v2,
        "tier": 2,
    },
    {
        "id": "capital_letters_from_second_half_alphabet",
        "description": "All {Capital Letters} must come from {2nd Half of Alphabet}",
        "subtitle": "I dont know if this is possible",
        "method": r_capital_letters_from_second_half_alphabet,
        "tier": 5,
    },
    {
        "id": "5_digits",
        "description": "Must include {5+ Digit}",
        "subtitle": "No repeating digits",
        "method": r_5_digits,
        "tier": 2,
    },
    {
        "id": "all_vowels_capitalized",
        "description": "All {Vowels} must be {Capitalized}",
        "subtitle": "Y is a vowel",
        "method": r_all_vowels_capitalized,
        "tier": 3,
        "excludes": ["vowels_not_capitalized"],
    },
    {
        "id": "state_capital",
        "description": "Must include the name of a {USA State Capital}",
        "method": r_state_capital,
        "tier": 2,
    },
    {
        "id": "vowels_not_touching",
        "description": "{Vowels} cannot be next to each other",
        "method": r_vowels_not_touching,
        "tier": 4,
    },
    {
        "id": "michelangelo",
        "description": "Must include name of the person who made {This}",
        "image": "https://i.gyazo.com/5230534b403533527d54cdaced9d09eb.jpg",
        "method": r_michelangelo,
        "tier": 2,
    },
    {
        "id": "no_spaces",
        "description": "Must NOT contain any {Spaces}",
        "method": r_no_spaces,
        "tier": 1,
    },
    {
        "id": "3_vowels",
        "description": "Must contain at least {3 Vowels}",
        "subtitle": "Y counts as a vowel",
        "method": r_3_vowels,
        "tier": 1,
    },
    {
        "id": "starts_with_letter",
        "description": "Must {Start} with a Letter",
        "subtitle": "No leading digits or symbols",
        "method": r_starts_with_letter,
        "tier": 1,
    },
    {
        "id": "two_digit_prime",
        "description": "Must include a {Two-Digit Prime Number}",
        "subtitle": "e.g. 11, 13, 17, 19, 23...",
        "method": r_two_digit_prime,
        "tier": 2,
    },
    {
        "id": "greek_letter",
        "description": "Must include the name of a {Greek Letter}",
        "subtitle": "Full name, spelled out (e.g. \"beta\", not \"β\")",
        "method": r_greek_letter,
        "tier": 2,
    },
    {
        "id": "no_back_to_back_repeats",
        "description": "Must contain {No Back-to-Back Repeated Characters}",
        "subtitle": "Same character can't appear twice in a row",
        "method": r_no_back_to_back_repeats,
        "tier": 3,
    },
    {
        "id": "strictly_alternating_case",
        "description": "{Letters} must strictly {Alternate} between upper and lower case",
        "subtitle": "Digits/symbols/emojis don't count, only letters",
        "method": r_strictly_alternating_case,
        "tier": 4,
    },
    {
        "id": "every_vowel_at_least_once",
        "description": "Must include {Every Vowel} at least once",
        "subtitle": "a, e, i, o, and u - Y doesn't count here",
        "method": r_every_vowel_at_least_once,
        "tier": 4,
    },
    {
        "id": "exact_palindrome",
        "description": "Password must be an exact {Palindrome}",
        "subtitle": "Reads the same forwards and backwards. Capitalization doesn't matter",
        "method": r_exact_palindrome,
        "tier": 5,
    },
    {
        "id": "length_equals_digit_sum",
        "description": "Password {Length} must equal the {Sum of its Digits}",
        "subtitle": "e.g. \"11111\" has length 5 and digits summing to 5",
        "method": r_length_equals_digit_sum,
        "tier": 5,
    },
]

RULE_LOOKUP = {rule["id"]: rule for rule in RULE_POOL}
