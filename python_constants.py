US_STATES = [
    "alabama", "alaska", "arizona", "arkansas", "california",
    "colorado", "connecticut", "delaware", "florida", "georgia",
    "hawaii", "idaho", "illinois", "indiana", "iowa",
    "kansas", "kentucky", "louisiana", "maine", "maryland",
    "massachusetts", "michigan", "minnesota", "mississippi", "missouri",
    "montana", "nebraska", "nevada", "new hampshire", "new jersey",
    "new mexico", "new york", "north carolina", "north dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina",
    "south dakota", "tennessee", "texas", "utah", "vermont",
    "virginia", "washington", "west virginia", "wisconsin", "wyoming",
    
    "newhampshire", "newjersey",
    "newmexico", "newyork", "northcarolina", "northdakota", "rhodeisland", "southcarolina",
    "southdakota","westvirginia",
]


# ─── GEN 1 ───────────────────────────────────────────────────────────────────
GEN1_FIRE_WATER_GRASS = [
    "bulbasaur",    # Grass/Poison
    "ivysaur",      # Grass/Poison
    "venusaur",     # Grass/Poison
    "charmander",   # Fire
    "charmeleon",   # Fire
    "charizard",    # Fire/Flying
    "squirtle",     # Water
    "wartortle",    # Water
    "blastoise",    # Water
    "vulpix",       # Fire
    "ninetales",    # Fire
    "oddish",       # Grass/Poison
    "gloom",        # Grass/Poison
    "vileplume",    # Grass/Poison
    "paras",        # Bug/Grass
    "parasect",     # Bug/Grass
    "psyduck",      # Water
    "golduck",      # Water
    "growlithe",    # Fire
    "arcanine",     # Fire
    "poliwag",      # Water
    "poliwhirl",    # Water
    "poliwrath",    # Water/Fighting
    "bellsprout",   # Grass/Poison
    "weepinbell",   # Grass/Poison
    "victreebel",   # Grass/Poison
    "tentacool",    # Water/Poison
    "tentacruel",   # Water/Poison
    "ponyta",       # Fire
    "rapidash",     # Fire
    "slowpoke",     # Water/Psychic
    "slowbro",      # Water/Psychic
    "seel",         # Water
    "dewgong",      # Water/Ice
    "shellder",     # Water
    "cloyster",     # Water/Ice
    "krabby",       # Water
    "kingler",      # Water
    "exeggcute",    # Grass/Psychic
    "exeggutor",    # Grass/Psychic
    "tangela",      # Grass
    "horsea",       # Water
    "seadra",       # Water
    "goldeen",      # Water
    "seaking",      # Water
    "staryu",       # Water
    "starmie",      # Water/Psychic
    "magmar",       # Fire
    "magikarp",     # Water
    "gyarados",     # Water/Flying
    "lapras",       # Water/Ice
    "vaporeon",     # Water
    "flareon",      # Fire
    "omanyte",      # Rock/Water
    "omastar",      # Rock/Water
    "kabuto",       # Rock/Water
    "kabutops",     # Rock/Water
    "moltres",      # Fire/Flying
]  # 58 Pokémon

GEN1_OTHER_TYPES = [
    "caterpie",     # Bug
    "metapod",      # Bug
    "butterfree",   # Bug/Flying
    "weedle",       # Bug/Poison
    "kakuna",       # Bug/Poison
    "beedrill",     # Bug/Poison
    "pidgey",       # Normal/Flying
    "pidgeotto",    # Normal/Flying
    "pidgeot",      # Normal/Flying
    "rattata",      # Normal
    "raticate",     # Normal
    "spearow",      # Normal/Flying
    "fearow",       # Normal/Flying
    "ekans",        # Poison
    "arbok",        # Poison
    "pikachu",      # Electric
    "raichu",       # Electric
    "sandshrew",    # Ground
    "sandslash",    # Ground
    "nidoran♀",    # Poison
    "nidoran",    # Poison
    "nidorina",     # Poison
    "nidoqueen",    # Poison/Ground
    "nidoran♂",    # Poison
    "nidorino",     # Poison
    "nidoking",     # Poison/Ground
    "clefairy",     # Normal
    "clefable",     # Normal
    "jigglypuff",   # Normal
    "wigglytuff",   # Normal
    "zubat",        # Poison/Flying
    "golbat",       # Poison/Flying
    "venonat",      # Bug/Poison
    "venomoth",     # Bug/Poison
    "diglett",      # Ground
    "dugtrio",      # Ground
    "meowth",       # Normal
    "persian",      # Normal
    "mankey",       # Fighting
    "primeape",     # Fighting
    "abra",         # Psychic
    "kadabra",      # Psychic
    "alakazam",     # Psychic
    "machop",       # Fighting
    "machoke",      # Fighting
    "machamp",      # Fighting
    "geodude",      # Rock/Ground
    "graveler",     # Rock/Ground
    "golem",        # Rock/Ground
    "magnemite",    # Electric
    "magneton",     # Electric
    "farfetch'd",   # Normal/Flying
    "doduo",        # Normal/Flying
    "dodrio",       # Normal/Flying
    "grimer",       # Poison
    # "muk",          # Poison
    "gastly",       # Ghost/Poison
    "haunter",      # Ghost/Poison
    "gengar",       # Ghost/Poison
    "onix",         # Rock/Ground
    "drowzee",      # Psychic
    "hypno",        # Psychic
    "voltorb",      # Electric
    "electrode",    # Electric
    "cubone",       # Ground
    "marowak",      # Ground
    "hitmonlee",    # Fighting
    "hitmonchan",   # Fighting
    "lickitung",    # Normal
    "koffing",      # Poison
    "weezing",      # Poison
    "rhyhorn",      # Ground/Rock
    "rhydon",       # Ground/Rock
    "chansey",      # Normal
    "kangaskhan",   # Normal
    "mr. mime",     # Psychic
    "mr.mime",     # Psychic
    "scyther",      # Bug/Flying
    "jynx",         # Ice/Psychic
    "electabuzz",   # Electric
    "pinsir",       # Bug
    "tauros",       # Normal
    "ditto",        # Normal
    "eevee",        # Normal
    "jolteon",      # Electric
    "porygon",      # Normal
    "aerodactyl",   # Rock/Flying
    "snorlax",      # Normal
    "articuno",     # Ice/Flying
    "zapdos",       # Electric/Flying
    "dratini",      # Dragon
    "dragonair",    # Dragon
    "dragonite",    # Dragon/Flying
    "mewtwo",       # Psychic
    "mew",          # Psychic
]  # 93 Pokémon

# ─── GEN 7 (Sun/Moon + Ultra Sun/Ultra Moon) ─────────────────────────────────

GEN7_FIRE_WATER_GRASS = [
    "rowlet",       # Grass/Flying
    "dartrix",      # Grass/Flying
    "decidueye",    # Grass/Ghost
    "litten",       # Fire
    "torracat",     # Fire
    "incineroar",   # Fire/Dark
    "popplio",      # Water
    "brionne",      # Water
    "primarina",    # Water/Fairy
    "oricorio",     # Fire/Flying
    "wishiwashi",   # Water
    "mareanie",     # Poison/Water
    "toxapex",      # Poison/Water
    "dewpider",     # Water/Bug
    "araquanid",    # Water/Bug
    "fomantis",     # Grass
    "lurantis",     # Grass
    "morelull",     # Grass/Fairy
    "shiinotic",    # Grass/Fairy
    "salandit",     # Poison/Fire
    "salazzle",     # Poison/Fire
    "bounsweet",    # Grass
    "steenee",      # Grass
    "tsareena",     # Grass
    "wimpod",       # Bug/Water
    "golisopod",    # Bug/Water
    "pyukumuku",    # Water
    "turtonator",   # Fire/Dragon
    "bruxish",      # Water/Psychic
    "dhelmise",     # Ghost/Grass
    "tapubulu",    # Grass/Fairy
    "tapufini",    # Water/Fairy
    "kartana",      # Grass/Steel
    "blacephalon",  # Fire/Ghost
]  # 34 Pokémon

GEN7_OTHER_TYPES = [
    "pikipek",      # Normal/Flying
    "trumbeak",     # Normal/Flying
    "toucannon",    # Normal/Flying
    "yungoos",      # Normal
    "gumshoos",     # Normal
    "grubbin",      # Bug
    "charjabug",    # Bug/Electric
    "vikavolt",     # Bug/Electric
    "crabrawler",   # Fighting
    "crabominable", # Fighting/Ice
    "cutiefly",     # Bug/Fairy
    "ribombee",     # Bug/Fairy
    "rockruff",     # Rock
    "lycanroc",     # Rock
    "mudbray",      # Ground
    "mudsdale",     # Ground
    "stufful",      # Normal/Fighting
    "bewear",       # Normal/Fighting
    "comfey",       # Fairy
    "oranguru",     # Normal/Psychic
    "passimian",    # Fighting
    "sandygast",    # Ghost/Ground
    "palossand",    # Ghost/Ground
    "type: null",  # Normal
    "silvally",     # Normal
    "minior",       # Rock/Flying
    "komala",       # Normal
    "togedemaru",   # Electric/Steel
    "mimikyu",      # Ghost/Fairy
    "drampa",       # Normal/Dragon
    "jangmo-o",     # Dragon
    "hakamo-o",     # Dragon/Fighting
    "kommo-o",      # Dragon/Fighting
    "tapu koko",   # Electric/Fairy
    "tapu lele",   # Psychic/Fairy
    "tapu-koko",    # Electric/Fairy
    "tapu-lele",    # Psychic/Fairy
    "cosmog",       # Psychic
    "cosmoem",      # Psychic
    "solgaleo",     # Psychic/Steel
    "lunala",       # Psychic/Ghost
    "nihilego",     # Rock/Poison
    "buzzwole",     # Bug/Fighting
    "pheromosa",    # Bug/Fighting
    "xurkitree",    # Electric
    "celesteela",   # Steel/Flying
    "guzzlord",     # Dark/Dragon
    "necrozma",     # Psychic
    "magearna",     # Steel/Fairy
    "marshadow",    # Fighting/Ghost
    "poipole",      # Poison
    "naganadel",    # Poison/Dragon
    "stakataka",    # Rock/Steel
    "zeraora",      # Electric
]  # 52 Pokémon


# Countries with French as an official/national language
FRENCH_SPEAKING_COUNTRIES = [
    # Africa (20 countries)
    "benin",
    # "burkina faso",      # French demoted to "working language" in 2024
    "burundi",
    "cameroon",
    "central african republic",
    "centralafricanrepublic",
    "chad",
    "comoros",
    "democratic republic of the congo",
    "democraticrepublicofthecongo",
    "djibouti",
    "equatorial guinea",
    "equatorialguinea",
    "gabon",
    "guinea",
    "ivory coast",       # Côte d'Ivoire
    "ivorycoast",       # Côte d'Ivoire
    "Côte d'Ivoire"     # Proper name for Ivory Coast
    "Côted'Ivoire"     # Proper name for Ivory Coast
    "madagascar",
    # "mali",               # French demoted to "working language" in 2023
    # "niger",              # French demoted to "working language" in 2025
    "republic of the congo",
    "republicofthecongo",
    "rwanda",
    "senegal",
    "seychelles",
    "togo",

    # Europe (5 countries)
    "belgium",
    "france",
    "luxembourg",
    "monaco",
    "switzerland",

    # Americas (2 countries)
    "canada",
    "haiti",

    # Oceania (1 country)
    "vanuatu",
]


CAT_EMOJIS = [
    "😺",
    "😸",
    "😹",
    "😻",
    "😼",
    "😽",
    "🙀",
    "😿",
    "😾",
    "🐱",
    "🐯",
    "🦁",
    "🐅",
    "🐆",
    "🐈",
    "🐈‍⬛",
]

MOUSE_EMOJIS = [
    "🐁",
    "🐀",
    "🐭",
    "🐹",
    "🖱️",
]


MOST_COMMON_TWITCH_CHAT_WORDS = [
    "poggies",
    "cinema",
    "catjam",
    "rigged",
    "stream",
    "transgenderpride",
    "!word",
    "omegalul",
    "dougdoug",
    "please",
    "chair",
    "cheer100",
    "!rules",
    "about",
    "first",
    "@dougdoug",

    # "!ban",
    # "doug",
    # "this",
    # "what",
    # "that",
    # "play",
    # "they",
    # "want",
    # "game",
    # "here",
    # "more",
    # "time",
    # "kekw",
    # "it's",
    # "fuck",
    # "back",
    # "need",
    # "make",
    # "love",
    # "good",
    # "with",
    # "true",
    # "will",
    # "just",
    # "have",
    # "your",
    # "bald",
    # "chat",
    # "like",
]


TWITCH_GLOBAL_EMOTES = [
    "4Head",
    "ANELE",
    "AmbessaLove",
    "AnotherRecord",
    "ArgieB8",
    "ArsonNoSexy",
    "AsexualPride",
    "AsianGlow",
    "BCWarrior",
    "BabyRage",
    "BatChest",
    "BegWan",
    "BigBrother",
    "BigPhish",
    "BigSad",
    "BisexualPride",
    "BlackLivesMatter",
    "BlargNaut",
    "BloodTrail",
    "BrainSlug",
    "BratChat",
    "BrokeBack",
    "BuddhaBar",
    "CaitThinking",
    "CarlSmile",
    "ChefFrank",
    "Cinheimer",
    "CoolCat",
    "CoolStoryBob",
    "CorgiDerp",
    "CrreamAwk",
    "CurseLit",
    "DAESuppy",
    "DBstyle",
    "DansGame",
    "DarkMode",
    "DatSheffy",
    "DendiFace",
    "DinoDance",
    "DogFace",
    "DoritosChip",
    "DxCat",
    "EarthDay",
    "EkkoChest",
    "EleGiggle",
    "EntropyWins",
    "ExtraLife",
    "FBBlock",
    "FBCatch",
    "FBChallenge",
    "FBPass",
    "FBPenalty",
    "FBRun",
    "FBSpiral",
    "FBtouchdown",
    "FUNgineer",
    "FailFish",
    "FeelsVi",
    "FeverFighter",
    "FootBall",
    "FootGoal",
    "FootYellow",
    "FrankerZ",
    "FreakinStinkin",
    "FutureMan",
    "GRASSLORD",
    "GayPride",
    "GenderFluidPride",
    "GingerPower",
    "GivePLZ",
    "GlitchCat",
    "GlitchLit",
    "GlitchNRG",
    "GoatEmotey",
    "GoldPLZ",
    "GrammarKing",
    "HSCheers",
    "HSWP",
    "HassaanChop",
    "HeyGuys",
    "HolidayCookie",
    "HolidayLog",
    "HolidayPresent",
    "HolidaySanta",
    "HolidayTree",
    "HotPokket",
    "ImTyping",
    "IntersexPride",
    "InuyoFace",
    "ItsBoshyTime",
    "JKanStyle",
    "Jebaited",
    "Jebasted",
    "JinxLUL",
    "JonCarnage",
    "KAPOW",
    "Kappa",
    "Kappa",
    "KappaClaus",
    "KappaPride",
    "KappaRoss",
    "KappaWealth",
    "Kappu",
    "Keepo",
    "KevinTurtle",
    "Kippa",
    "KomodoHype",
    "KonCha",
    "Kreygasm",
    "LaundryBasket",
    "LesbianPride",
    "MVGame",
    "Mau5",
    "MaxLOL",
    "MercyWing1",
    "MercyWing2",
    "MikeHogu",
    "MingLee",
    "ModLove",
    "MorphinTime",
    "MrDestructoid",
    "MyAvatar",
    "NewRecord",
    "NinjaGrumpy",
    "NomNom",
    "NonbinaryPride",
    "NotATK",
    "NotLikeThis",
    "OSFrog",
    "OhMyDog",
    "OneHand",
    "OpieOP",
    "OptimizePrime",
    "PJSalt",
    "PJSugar",
    "PMSTwin",
    "PRChase",
    "PanicVis",
    "PansexualPride",
    "PartyHat",
    "PartyTime",
    "PeoplesChamp",
    "PermaSmug",
    "PewPewPew",
    "PicoMause",
    "PinkMercy",
    "PipeHype",
    "PixelBob",
    "PizzaTime",
    "PogChamp",
    "Poooound",
    "PopCorn",
    "PopNemo",
    "PowerUpL",
    "PowerUpR",
    "PraiseIt",
    "PrimeMe",
    "PunOko",
    "PunchTrees",
    "RaccAttack",
    "RalpherZ",
    "RedCoat",
    "ResidentSleeper",
    "RitzMitz",
    "RlyTho",
    "RuleFive",
    "SMOrc",
    "SSSsss",
    "SUBprise",
    "SUBtember",
    "SabaPing",
    "SeemsGood",
    "SeriousSloth",
    "ShadyLulu",
    "ShazBotstix",
    "Shush",
    "SingsMic",
    "SingsNote",
    "SipTime",
    "SmoocherZ",
    "SoBayed",
    "SoonerLater",
    "Squid1",
    "Squid2",
    "Squid3",
    "Squid4",
    "StinkyCheese",
    "StinkyGlitch",
    "StoneLightning",
    "StrawBeary",
    "SuperVinlin",
    "SwiftRage",
    "TBAngel",
    "TF2John",
    "TPFufun",
    "TPcrunchyroll",
    "TTours",
    "TWITH",
    "TakeNRG",
    "TearGlove",
    "TehePelo",
    "ThankEgg",
    "TheIlluminati",
    "TheRinger",
    "TheTarFu",
    "TheThing",
    "ThunBeast",
    "TinyFace",
    "TombRaid",
    "TooSpicy",
    "TransgenderPride",
    "TriHard",
    "TwitchConHYPE",
    "TwitchLit",
    "TwitchRPG",
    "TwitchSings",
    "TwitchUnity",
    "TwitchVotes",
    "UWot",
    "UnSane",
    "UncleNox",
    "VirtualHug",
    "VoHiYo",
    "VoteNay",
    "VoteYea",
    "WTRuck",
    "WeDidThat",
    "WholeWheat",
    "WutFace",
    "Yagoo",
    "YouDontSay",
    "YouWHY",
    "bleedPurple",
    "cmonBruh",
    "copyThis",
    "duDudu",
    "imGlitch",
    "mcaT",
    "panicBasket",
    "pastaThat",
    "riPepperonis",
    "twitchRaid",
]

# Top 15 fast food chains in the US by market share (U.S. systemwide sales)
# Source: QSR Magazine's QSR 50 2025 report — annual ranking by U.S. systemwide sales,
# collected directly from restaurant companies (March–May 2025), covering 2024 performance.
# Note: KFC had only $4.9B in U.S. systemwide sales (ranked ~15th) and Tim Hortons has
# negligible US presence (~600 locations), so neither is a major US market share player.
TOP_FAST_FOOD_CHAINS = [
    "mcdonald's",       # ~$53.5B U.S. systemwide sales — #1 by a huge margin
    "mcdonalds",       # ~$53.5B U.S. systemwide sales — #1 by a huge margin
    "starbucks",        # ~$29B U.S. systemwide sales
    "chick-fil-a",      # ~$22.7B U.S. systemwide sales
    "chickfila",      # ~$22.7B U.S. systemwide sales
    "taco bell",        # ~$15.9B U.S. systemwide sales
    "tacobell",        # ~$15.9B U.S. systemwide sales
    "wendy's",          # ~$12.3B U.S. systemwide sales
    "wendys",          # ~$12.3B U.S. systemwide sales
    "burger king",      # ~$10.5B U.S. systemwide sales
    "burgerking",      # ~$10.5B U.S. systemwide sales
    "subway",           # ~$10.2B U.S. systemwide sales
    "chipotle",         # ~$11.3B U.S. systemwide sales
    "domino's",         # ~$9.0B U.S. systemwide sales
    "dominos",         # ~$9.0B U.S. systemwide sales
    "dunkin'",          # ~$7.5B U.S. systemwide sales
    "pizza hut",        # ~$5.5B U.S. systemwide sales
    "pizzahut",        # ~$5.5B U.S. systemwide sales
    "popeyes",          # ~$6.0B U.S. systemwide sales
    "kfc",              # ~$4.9B U.S. systemwide sales (international — British-origin, US parent Yum! Brands; ~3,500 US locations)
    "panda express",    # ~$5.9B U.S. systemwide sales
    "pandaexpress",    # ~$5.9B U.S. systemwide sales
    "sonic drive-in",   # ~$5.0B U.S. systemwide sales
    "sonicdrive-in",   # ~$5.0B U.S. systemwide sales
]

VALID_MONKEYS = ['proboscis monkey', 'proboscismonkey', 'proboscis_monkey', 'proboscis-monkey']

# From 3 websites:
# https://parade.com/living/gen-alpha-slang
# https://www.purewow.com/family/gen-alpha-slang-phrases
GEN_ALPHA_SLANG = [
    "67",
    "6-7",
    "6 7",
    "bet",
    "mid",
    "low-key",
    "lowkey",
    "low key",
    "cap",
    "nocap",
    "chicken jockey",
    "chickenjockey",
    "brainrot",
    "brain rot",
    "unc",
    "skibidi",
    "rizz",
    "sus",
    "flex",
    "sigma",
    "mew",
    "mewing",
    "delulu",
    "baka",
    "fanumtax",
    "ohio",
    "chat",
    "chicken banana",
    "chickenbanana",
    "mog",
    "mogging",
    "framemog",
    "calltaylor",
    "aura",
    "aurafarm",
    "aura farm",
    "aura farming",
    "aurafarming",
    "negative tilt",
    "negativetilt",
    "hunter eyes",
    "huntereyes",
    "starvemaxxing",
    "looksmaxxing",
    "cook",
    "goat",
    "goated",
    "rizz",
    "gyatt",
    "gyat",
    "bruh",
    "salty",
    "ate",
    "noob",
    "zang",
    "yeet",
    "lit",
    "bop",
    "just put the fries in the bag bro",
    "simp",
    "ick",
    "cringe",
    "opp",
    "w",
    "l",
    "twin",
    "its giving",
    "itsgiving",
    "pookie",
    "hits different",
    "not gonna lie",
    "notgonnalie",
    "og",
    "drip",
    "tea",
    "sheesh",
    "madlit",
    "vibe",
    "alpha",
    "bussin",
    "glaze",
    "chad",
    "mog",
    "dogwater",
    "dog water",
    "fam",
    "yapping",
]

# Giving them the top 15 just for wiggle room in case it changes
BIGGEST_YOUTUBE_CHANNELS = [
    "MrBeast",                    # ~484M subscribers
    "T-Series",                   # ~312M subscribers (Indian music/film label)
    "Cocomelon - Nursery Rhymes", # ~201M subscribers (kids' animated content)
    "SET India",                  # ~189M subscribers (Indian TV network)
    "Vlad and Niki",              # ~149M subscribers (kids' content)
    "✿ Kids Diana Show",            # ~138M subscribers (kids' content)
    "Stokes Twins",               # ~137M subscribers (challenge/entertainment)
    "Like Nastya",                # ~131M subscribers (kids' content)
    "김프로KIMPRO",                # ~131M subscribers (shorts/entertainment)
    "Zee Music Company",          # ~122M subscribers (Indian music label)
]


PANCAKE_INGREDIENTS = [
    "flour", "baking powder", "bakingpowder", "salt", "sugar", "eggs", "milk", "butter", "egg"
]

FUNNY_MEME_NUMBERS = [
    "420",
    "67",
    "69",
    "80085",
    "8008513",
    "1337", # LEET
    "42", # Meaning of the universe
]

# With help from stanford
# https://web.stanford.edu/~eckert/PDF/PenisTesticlesSlang.pdf 
PENIS_NICKNAMES = [
    "dong",
    "weiner",
    "cock",
    "shaft",
    "dick",
    "schlong",
    "knob",
    "stick",
    "baton",
    "member",
    "plumbus",
    "wang",
    "rod",
    "tool",
    "pecker",
    "peter",
    "sausage",
    "trouser snake",
    "trousersnake",
    "willy",
    "snake",
    "banana",
    "willy",
    "willie",
    "weewee",
    "winkie",
    "peepee",
    "boner",
    "ding dong",
    "dingdong",
    "dork",
    "fuck stick",
    "fuckstick",
    "hog",
    "johnson",
    "knob",
    "love muscle",
    "lovemuscle",
    "manhood",
    "manmeat",
    "meat stick",
    "meatstick",
    "prick",
    "tally whacker",
    "peen",
]

UPPERCASE_VOWELS = {'A', 'E', 'I', 'O', 'U', 'Y'}

# From https://www.mcdonalds.com/us/en-us/product/big-mac.html#accordion-c921f9207b-item-283bee7dbd
BIG_MAC_INGREDIENTS = [
    "big mac bun",
    "100% beef patty",
    "shredded lettuce",
    "big mac sauce",
    "pasteurized process american cheese",
    "pickle slices",
    "onions",

    "bigmacbun",
    "100%beefpatty",
    "shreddedlettuce",
    "bigmacsauce",
    "pasteurizedprocessamericancheese",
    "pickleslices",

    "enriched flour",
    "enrichedflour",
    "wheat flour",
    "wheatflour",
    "malted barley flour",
    "maltedbarleyflour",
    "niacin",
    "reduced iron",
    "reducediron",
    "thiamine mononitrate",
    "thiaminemononitrate",
    "riboflavin",
    "folic acid",
    "water",
    "sugar",
    "yeast",
    "soybean oil",
    "sesame seeds",
    "sesameseeds",
    "potato starch",
    "salt",
    "dextrose",
    "corn starch",
    "cornstarch",
    "modified food starch",
    "vinegar",
    "vegetable proteins",
    "pea, potato, rice and/or faba bean",
    "sunflower and/or canola oil",
    "maltodextrin",
    "wheat gluten",
    "natural flavors",
    "naturalflavors",
    "dough conditioners (enzymes, ascorbic acid)",
    "100% pure usda inspected beef",
    "sweet relish",
    "sweetrelish",
    "diced pickles",
    "dicedpickles",
    "high fructose corn syrup",
    "distilled vinegar",
    "corn syrup",
    "cornsyrup",
    "xanthan gum",
    "calcium chloride",
    "spice extractives",
    "egg yolks",
    "distilled vinegar",
    "spices",
    "onion powder",
    "onionpowder",
    "propylene glycol alginate",
    "garlic powder",
    "garlicpowder",
    "vegetable protein (hydrolyzed corn, soy and wheat)",
    "caramel color",
    "turmeric",
    "extractives of paprika",
    "soy lecithin",
    "soylecithin",
    "milk",
    "cream",
    "sodium citrate",
    "cheese cultures",
    "citric acid",
    "enzymes",
    "soy lecithin",
    "color added",
    "cucumbers",
    "distilled vinegar",
    "calcium chloride",
    "alum",
    "potassium sorbate (preservative)",
    "natural flavors",
    "polysorbate 80",
    "extractives of turmeric (color)",
]

US_CAPITALS = [
    "montgomery",      # Alabama
    "juneau",          # Alaska
    "phoenix",         # Arizona
    "little rock",     # Arkansas
    "littlerock",     # Arkansas
    "sacramento",      # California
    "denver",          # Colorado
    "hartford",        # Connecticut
    "dover",           # Delaware
    "tallahassee",     # Florida
    "atlanta",         # Georgia
    "honolulu",        # Hawaii
    "boise",           # Idaho
    "springfield",     # Illinois
    "indianapolis",    # Indiana
    "des moines",      # Iowa
    "desmoines",      # Iowa
    "topeka",          # Kansas
    "frankfort",       # Kentucky
    "baton rouge",     # Louisiana
    "batonrouge",     # Louisiana
    "augusta",         # Maine
    "annapolis",       # Maryland
    "boston",          # Massachusetts
    "lansing",         # Michigan
    "saint paul",      # Minnesota
    "saintpaul",      # Minnesota
    "jackson",         # Mississippi
    "jefferson city",  # Missouri
    "jeffersoncity",  # Missouri
    "helena",          # Montana
    "lincoln",         # Nebraska
    "carson city",     # Nevada
    "carsoncity",     # Nevada
    "concord",         # New Hampshire
    "trenton",         # New Jersey
    "santa fe",        # New Mexico
    "santafe",        # New Mexico
    "albany",          # New York
    "raleigh",         # North Carolina
    "bismarck",        # North Dakota
    "columbus",        # Ohio
    "oklahoma city",   # Oklahoma
    "oklahomacity",   # Oklahoma
    "salem",           # Oregon
    "harrisburg",      # Pennsylvania
    "providence",      # Rhode Island
    "columbia",        # South Carolina
    "pierre",          # South Dakota
    "nashville",       # Tennessee
    "austin",          # Texas
    "salt lake city",  # Utah
    "saltlakecity",  # Utah
    "montpelier",      # Vermont
    "richmond",        # Virginia
    "olympia",         # Washington
    "charleston",      # West Virginia
    "madison",         # Wisconsin
    "cheyenne"         # Wyoming
]

LOWERCASE_VOWELS = {'a', 'e', 'i', 'o', 'u', 'y'}

ALL_VOWELS = {'a', 'e', 'i', 'o', 'u', 'y'}

GREEK_LETTERS = [
    "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
    "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho",
    "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega",
]