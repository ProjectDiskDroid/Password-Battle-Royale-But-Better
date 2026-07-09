import re
import math
import emoji
from datetime import datetime
from python_constants import *

# ALL of the rule VALIDATOR FUNCTIONS for the game.
# Note that rules are case IN-SENSITIVE unless explicitly stated otherwise.
# These are pure str -> bool predicates - they don't know or care which round/match
# they belong to. See python_rule_pool.py for the pool that pairs these up with
# descriptions/tiers, and python_rules_manager.py for how rules get drawn each round.

# "Must include {5+ Characters}
def r_5_characters(password):
    return len(password) >= 5

# "Must include {1+ Uppercase Letter} and {1+ Special Character}",
def r_1_uppercase_1_special(password):
    if not any(char.isupper() for char in password): # Is there any uppercase char?
        return False
    if not any(not char.isalnum() for char in password): # Is a special char?
        return False
    return True

# "Must include {1+ Digit}",
def r_1_digit(password):
    # General format of any:   any(<boolean expression> for <item> in <iterable>)
    return any(char.isdigit() for char in password)

# "Must include the name of a {US State}",
def r_us_state(password):
    password = password.lower()
    return any(state in password for state in US_STATES)

# "Must contain exactly {5 Letter e's}",
def r_5_letter_e(password):
    # This is case INSENSITIVE
    password = password.lower()
    return password.count('e') == 5

# "Must include the name of a {Gen 1 Pokemon}",
def r_gen1_pokemon(password):
    # Note, it can't be a fire / water / grass type, also excluding ugly one
    password = password.lower()
    return any(pokemon in password for pokemon in GEN1_OTHER_TYPES)

# "Must include country with {French} as an official national language",
def r_french_language(password):
    password = password.lower()
    return any(country in password for country in FRENCH_SPEAKING_COUNTRIES)

# "Must contain same number of {Digits} and {Emojis}",
def r_same_digits_emojis(password):
    digit_count = sum(char.isdigit() for char in password) # True is 1 and False is 0 when summing
    emoji_count = emoji.emoji_count(password)
    return digit_count == emoji_count

# "Must include the name of {This Game}",
def r_mario64(password):
    password = password.lower()
    return "mario 64" in password or 'mario64' in password

#  "Must include number of hits it takes to kill {Both Cows}"
def r_minecraft_block(password):
    return "20" in password or "twenty" in password.lower()

# "Must contain exactly {7 Emojis}",
def r_7_emojis(password):
    return emoji.emoji_count(password) == 7

# "Must include a {Cat} and {Mouse} Emoji",
def r_include_cat_mouse(password):
    has_cat = any(kitty in password for kitty in CAT_EMOJIS)
    has_mouse = any(mouse in password for mouse in MOUSE_EMOJIS)
    return has_cat and has_mouse

# "Must contain no {Duplicate Emojis}",
def r_no_duplicate_emojis(password):
    # Unfortunately you can't just go character-by-character through a string because some emojis are multiple characters (like country flags)
    # So instead use the emoji.emoji_list() function which returns an array of dictionaries, each dict represents an emoji (up to 2 characters)
    # [
    #   {'match_start': 7, 'match_end': 8, 'emoji': '🔥'},
    #   {'match_start': 13, 'match_end': 14, 'emoji': '💀'},
    #   {'match_start': 6, 'match_end': 8, 'emoji': '🇫🇷'}
    # ]
    emoji_list = emoji.emoji_list(password) # Get the list of dicts
    seen_emojis = set()
    for emoji_data in emoji_list:
        if emoji_data['emoji'] in seen_emojis:
            return False
        seen_emojis.add(emoji_data['emoji'])
    return True

# "{Cat} and {Mouse} emojis cannot be next to each other",
def r_cat_mouse_not_next_to_each_other(password):
    # This shit gets wonky because the black cat emoji is actually 3 characters, not just 1, so you can't just check pairs of characters
    # First create the array of emojis that includes their positions
    emojis = emoji.emoji_list(password)
    # Now we compare the emoji positions against each other
    for i in range(len(emojis)-1):
        if emojis[i]['match_end'] == emojis[i+1]['match_start']: # In this case, the emojis are genuinely next to each other
            if emojis[i]['emoji'] in CAT_EMOJIS and emojis[i+1]['emoji'] in MOUSE_EMOJIS:
                return False
            if emojis[i]['emoji'] in MOUSE_EMOJIS and emojis[i+1]['emoji'] in CAT_EMOJIS:
                return False
    return True

# "Must include 1 of the {Top 10 Most Commonly Said Words} in Doug's Twitch Chat",
def r_most_common_chat_words(password):
    password = password.lower()
    return any(chat_word in password for chat_word in MOST_COMMON_TWITCH_CHAT_WORDS)

# "Must contain no {Duplicate Digits}",
def r_no_duplicate_digits(password):
    seen_digits = set()
    for char in password:
        if char.isdigit():
            if char in seen_digits:
                return False
            seen_digits.add(char)
    return True

# "Include name of a {Pokemon} from this game's generation: ☀️🌕",
def r_sun_moon_pokemon(password):
    password = password.lower()
    return any(pokemon in password for pokemon in GEN7_OTHER_TYPES)

# "Must include {Twitch Global Emote}",
def r_twitch_global_emote(password):
    return any(emote in password for emote in TWITCH_GLOBAL_EMOTES)

# "Must contain an {Even Number of Characters}",
def r_even_num_characters(password):
    return len(password) % 2 == 0

# "Must contain exactly {5 capital D} letters",
def r_5_capital_d(password):
    return password.count('D') == 5

# "Must include name of a {Top 10 American Fast Food Chain} by valuation",
def r_name_of_fast_food_chain(password):
    password = password.lower()
    return any(chain in password for chain in TOP_FAST_FOOD_CHAINS)

# "All {Capital Letters} must be in {1st Half of Password}",
def r_capitals_in_first_half(password):
    # First get the 2nd half of password
    halfway_index = len(password) // 2 # "//" is integer division, will automatically round down
    second_half = password[halfway_index:]
    return not any(char.isupper() for char in second_half)

# "Include the name of this {Animal}",
def r_proboscis_monkey_pic(password):
    password = password.lower()
    return any(monkey in password for monkey in VALID_MONKEYS)

# "Also include this {Animal}",
def r_tarsier_pic(password):
    return 'tarsier' in password.lower()

# "What do you type into Twitch Chat to make {This Emote}",
def r_d_face_emote(password):
    return 'D:' in password

# "Must include one of {100 Most Popular Gen Alpha Slang}",
def r_gen_alpha_slang(password):
    password = password.lower()
    return any(slang in password for slang in GEN_ALPHA_SLANG)

# "Must contain equal number of {Capital D's} and {Digits}",
def r_equal_D_and_digits(password):
    letter_d_count = password.count('D')
    digit_count = sum(char.isdigit() for char in password)
    return letter_d_count == digit_count

# "Why is {6} afraid of {7}? Because {7} ate {9}", 6 and 7 digits cannot be next to each other
def r_6_7_cannot_be_next_to_another(password):
    for i in range(len(password)-1):
        if password[i] == '6' and password[i+1] == '7':
            return False
        if password[i] == '7' and password[i+1] == '6':
            return False
    return True

# "{Numbers} can not be next to each other",
def r_digits_cannot_be_next_to_another(password):
    for i in range(len(password)-1):
        if password[i].isdigit() and password[i+1].isdigit():
            return False
    return True

# "Must have equal number of {letter E} in both halves of password",
def r_equal_e_in_both_halves(password):
    password = password.lower()
    first_half = password[:(len(password) // 2)]
    second_half = password[(len(password) // 2):]
    return first_half.count('e') == second_half.count('e')

# "Must include 1 of {10 biggest Youtube channels} by sub count" "Capitalization must match channel name. Remove any spaces.",
def r_top_10_youtube_channel(password):
    return any(channel in password for channel in BIGGEST_YOUTUBE_CHANNELS)

# "Must include name of {Doug's biggest Youtube channels}",
def r_dougs_biggest_channel(password):
    return 'DougDoug' in password

# "Must include a cute character like {<(^_^<)}"
# For rule, this just means seeing an open and closed parenthesis
def r_cute_character_v1(password):
    return '(' in password and ')' in password

# "Must include console that {This Game} was released on",
def r_banjo_kazooie(password):
    password = password.lower()
    return 'nintendo 64' in password or 'nintendo64' in password or 'nintendo_64' in password or 'n64' in password

# "At least half of Password must be {Capital Letters}" (i.e. half of ALL characters must be uppercase letters)
def r_half_capital_letters(password):
    upper_count = sum(char.isupper() for char in password)
    return upper_count >= (len(password) // 2)

# "Must include one of the {5 Most Important Ingredients for Pancakes}",
def r_pancake_ingredients(password):
    password = password.lower()
    return any(ingredient in password for ingredient in PANCAKE_INGREDIENTS)

# "Must include one of the {Funny Meme Numbers}",
def r_funny_meme_numbers(password):
    return any(meme in password for meme in FUNNY_MEME_NUMBERS)

# "All {Digits} must add up to {25}",
def r_digits_add_to_twentyfive(password):
    count = 0
    for char in password:
        if char.isdigit():
            count += int(char)
    return count == 25

# "Must include a nickname for {Penis}",
def r_nickname_for_penis(password):
    password = password.lower()
    return any(penis in password for penis in PENIS_NICKNAMES)

# "{Vowels} cannot be capitalized",
def r_vowels_not_capitalized(password):
    return not any(vowel in password for vowel in UPPERCASE_VOWELS)

# "Must include the title of {This Wikipedia Page}",
def r_bear_wikipedia(password):
    return 'bear' in password.lower()

# "Must include one of the ingredients to a {McDonald's Big Mac}",
def r_big_mac_ingredients(password):
    password = password.lower()
    return any(ingredient in password for ingredient in BIG_MAC_INGREDIENTS)

# "Also, include another {cute little guy} for Twitch Chat {<(^_^<)}",
# For rule, this just means seeing ANOTHER open and closed parenthesis
def r_cute_guy_v2(password):
    return password.count('(') >= 2 and password.count(')') >= 2

# "All {Capital Letters} must be in {2nd Half of Alphabet}",
def r_capital_letters_from_second_half_alphabet(password):
    BANNED_HALF = 'ABCDEFGHIJKLM'
    for char in password:
        if char in BANNED_HALF:
            return False
    return True

# "Must include {5+ Digit}"
def r_5_digits(password):
    digit_count = sum(char.isdigit() for char in password)
    return digit_count >= 5

# "All {Vowels} must be {Capitalized}"
def r_all_vowels_capitalized(password):
    return not any(lower_vowel in password for lower_vowel in LOWERCASE_VOWELS)

# "Must include the name of a {USA State Capital}"
def r_state_capital(password):
    password = password.lower()
    return any(capital in password for capital in US_CAPITALS)

# "{Vowels} cannot be next to each other"
def r_vowels_not_touching(password):
    password = password.lower()
    for i in range(len(password)-1):
        if password[i] in ALL_VOWELS and password[i+1] in ALL_VOWELS:
            return False
    return True

# "Must include name of the person who made {This}"
def r_michelangelo(password):
    return "michelangelo" in password.lower()

# "Must NOT contain any {Spaces}"
def r_no_spaces(password):
    return ' ' not in password

# "Must contain at least {3 Vowels}"
def r_3_vowels(password):
    password = password.lower()
    return sum(char in ALL_VOWELS for char in password) >= 3

# "Must {Start} with a Letter"
def r_starts_with_letter(password):
    return password[0].isalpha()

# "Must include a {Two-Digit Prime Number}"
def r_two_digit_prime(password):
    TWO_DIGIT_PRIMES = ('11', '13', '17', '19', '23', '29', '31', '37', '41', '43',
                         '47', '53', '59', '61', '67', '71', '73', '79', '83', '89', '97')
    return any(prime in password for prime in TWO_DIGIT_PRIMES)

# "Must include the name of a {Greek Letter}"
def r_greek_letter(password):
    password = password.lower()
    return any(letter in password for letter in GREEK_LETTERS)

# "Must contain {No Back-to-Back Repeated Characters}"
def r_no_back_to_back_repeats(password):
    for i in range(len(password) - 1):
        if password[i] == password[i+1]:
            return False
    return True

# "{Letters} must strictly {Alternate} between upper and lower case"
def r_strictly_alternating_case(password):
    # Non-letter characters (digits, symbols, emojis) don't break the alternation - only letters count
    last_was_upper = None
    for char in password:
        if not char.isalpha():
            continue
        is_upper = char.isupper()
        if last_was_upper is not None and is_upper == last_was_upper:
            return False
        last_was_upper = is_upper
    return True

# "Must include {Every Vowel} at least once"
def r_every_vowel_at_least_once(password):
    password = password.lower()
    # Deliberately just the classic 5 vowels here, not "y" (unlike most other vowel rules in this file)
    return all(vowel in password for vowel in 'aeiou')

# "Password must be an exact {Palindrome}"
def r_exact_palindrome(password):
    password = password.lower()
    return password == password[::-1]

# "Password {Length} must equal the {Sum of its Digits}"
def r_length_equals_digit_sum(password):
    digit_sum = sum(int(char) for char in password if char.isdigit())
    return len(password) == digit_sum

# "{First and Last Character} must match"
def r_bookend_match(password):
    return len(password) >= 2 and password[0].lower() == password[-1].lower()

# "No character may appear more than {3 Times} in the password"
def r_frequency_cap(password):
    password_lower = password.lower()
    return all(password_lower.count(char) <= 3 for char in set(password_lower))

# "Password {Length} must be a {Fibonacci Number}"
def r_fibonacci_length(password):
    length = len(password)
    if length < 1:
        return False
    def is_perfect_square(x):
        root = math.isqrt(x)
        return root * root == x
    return is_perfect_square(5 * length * length + 4) or is_perfect_square(5 * length * length - 4)

# "Must include the name of a {Chess Piece}"
def r_chess_piece(password):
    password = password.lower()
    return any(piece in password for piece in CHESS_PIECES)

# "Must include a {Periodic Table Element Symbol} - capitalization must match"
def r_element_symbol(password):
    return any(symbol in password for symbol in ELEMENT_SYMBOLS)

# "Must contain a valid {Roman Numeral}, at least 2 characters long"
def r_roman_numeral(password):
    password = password.upper()
    roman_pattern = re.compile(r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')
    n = len(password)
    for i in range(n):
        for j in range(i + 2, n + 1):
            substring = password[i:j]
            if all(char in 'MDCLXVI' for char in substring) and roman_pattern.fullmatch(substring):
                return True
    return False

# "Must include {Today's Day of the Week}"
def r_todays_day(password):
    password = password.lower()
    today = datetime.now().strftime('%A').lower()
    return today in password

# "Sum of all character codes must be an {Even Number}"
def r_ascii_parity(password):
    return sum(ord(char) for char in password) % 2 == 0
