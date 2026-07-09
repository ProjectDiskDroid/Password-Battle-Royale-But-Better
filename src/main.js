import './style.css'
import { startPageBackground, setBgStarSpeed } from './animated-bg.js';

/*
// Core Logic:
    // Every 5 seconds, poll Vercel for the latest data
    // If we get new data back, update the visuals accordingly
*/

// MOCK DATA FOR REDIS

// MOCK RULES
// [
//     [
//       {
//         "description": "Must contain {5+ Characters}",
//         "subtitle": "Spaces are not allowed"
//       },
//       {
//         "description": "Must include {1+ Uppercase Letter} and {1+ Special Character}"
//       }
//     ],
//     [
//       {
//         "description": "Must include the name of a {US State}",
//         "subtitle": "2 letter abbreviations allowed"
//       }
//     ],
//     [
//       {
//         "description": "Must include {1+ Digit}"
//       },
//       {
//         "description": "Must contain *exactly* {5 Letter e's}"
//       }
//     ],
//     [
//       {
//         "description": "Must include name of a {Gen 1 Pokemon}",
//         "subtitle": "Cannot be fire, water, or leaf. Cannot be ugly (according to my gf)"
//       }
//     ],
//     [
//       {
//         "description": "Must include country with {French} as an official national language",
//         "subtitle": "Full country names, no abbreviations"
//       }
//     ]
// ]

// MOCK LIVING USERS
// [ 
// 	{
//         "username": "DougDougFan", 
//         "password": "do0😊@CAWeedleeFranceMario64😁9🤣🐈🌕😍321🐁baldGengarNotLikeThis", 
//         "submission_timestamp": "4:13:48:32" 
//     },
// 	{
//         "username": "Failboat",
//         "password": "McDondalsGOGO123saldkmmmmmmmmmmmmmmmasdjsankn",
//         "submission_timestamp": "4:13:48:32" 
//     },
// 	{
//         "username": "IAmtehlordofdougdougcommune", 
//         "password": "betoo😁😁👍👍swedenmanFrench", 
//         "submission_timestamp": "4:13:48:32" 
//     },
//     {
//         "username": "deepmindman", 
//         "password": "ZoZMZN5%<(^_^<)NiNTeNdo64ZZflouR4204PeNiSZZZZZleTTuceMbeaRZZZZZZZZZZZ<(^_^<)TTTT<(^_^<)TTTTT", "submission_timestamp": "4:13:48:32" 
//     }
// ]

// MOCK DEAD USERS
// [
//     {
//         "username": "toddhoward2", 
//         "password": "big22toiletsPIKACHU", 
//         "submission_timestamp": "7:12pm 15sec 20ms", 
//         "failure_message": "Must add a pokemon (cannot be fire or ice type)"
//     },
//     {
//         "username": "BigBoyBen", 
//         "password": "BigTractors$$58**7__66666666666669834mmmmew90wnls", 
//         "submission_timestamp": "7:12pm 16sec 40ms", 
//         "failure_message": "This shit is way way too long"
//     },
//     {
//         "username": "flatpancake99", 
//         "password": "subscribeToDougDougLMAO555", 
//         "submission_timestamp": "7:12pm 16sec 70ms", 
//         "failure_message": "Everything about this is wrong"
//     },
//     {
//         "username": "UncleRoger4444444444444444444444444", 
//         "password": "san53gomoon", 
//         "submission_timestamp": "7:12pm 23sec 10ms", 
//         "failure_message": "Why is your name so long thats not a pokemon"
//     }
// ]

// MOCK KILL COUNTS 
/*
{
    "Submitted a password that someone else already had!": 25,
    "Failed to submit a password in time.": 60,
    "Must contain {5+ Characters}": 6,
    "Must include {1+ Uppercase Letter} and {1+ Special Character}": 15,
    "Must include the name of a {US State}": 245,
    "Must include {1+ Digit}": 76,
    "Must contain *exactly* {5 Letter e's}": 30,
    "Must include name of a {Gen 1 Pokemon}": 48,
    "Must include country with {French} as an official national language": 19
} */

// ADDS ANY NEW RULES RECEIVED BY THE SERVER TO THE DOM
function handleNewRules(newRules, killCounts) {
    
    const fragment = document.createDocumentFragment(); // Create a new fragment
    
    newRules.forEach((roundRules) => {
        const newRoundRules = document.createElement('div');
        newRoundRules.classList.add('round-rules');

        roundRules.forEach((nextRule) => {
            const newRule = document.createElement('div');
            newRule.classList.add('rule');

            const newRuleTitle = document.createElement('div');
            newRuleTitle.classList.add('rule-title');

            // The rule text is written like this for readability:
            // "Must contain at least {5 Characters}"
            // This line will swap the {} character with a span with the highlight class
            let highlightedDescription = nextRule.description.replace(/\{([^}]+)\}/g, '<span class="rule-highlight">$1</span>')
            newRuleTitle.innerHTML = highlightedDescription;
            newRule.append(newRuleTitle);

            if (nextRule.subtitle) {
                const subtitleEl = document.createElement('div');
                subtitleEl.classList.add('rule-subtitle');
                subtitleEl.textContent = nextRule.subtitle
                newRule.append(subtitleEl);
            }

            if (nextRule.image) {
                const imageEl = document.createElement('img');
                imageEl.classList.add('rule-img');
                imageEl.src = nextRule.image;
                newRule.append(imageEl);
            }

            // If this rule has a killcount, display it
            if (killCounts && nextRule.description in killCounts) {
                const kills = killCounts[nextRule.description];
                const killCountEl = document.createElement('div');
                killCountEl.classList.add('rule-killcount');
                killCountEl.textContent = `☠️${kills}`;
                newRule.append(killCountEl);
            }

            newRoundRules.append(newRule);
        });

        fragment.append(newRoundRules)
    });

    const rulesContainer = document.getElementById("rules-container");
    rulesContainer.innerHTML = ''; // wipe it
    rulesContainer.append(fragment); // Transfers all the children from fragment

    // Add in the special killers if they're available
    const special_killers = document.createElement('div');
    special_killers.classList.add('special-killers-container');
    const ALREADY_SUBMITTED = "Submitted a password that someone else already had!"
    const DIDNT_SUBMIT = "Failed to submit a password in time."
    if (killCounts && ALREADY_SUBMITTED in killCounts) {
        const copiedKiller = document.createElement('div');
        copiedKiller.classList.add('special-killer');
        copiedKiller.textContent = `☠️ Copied: ${killCounts[ALREADY_SUBMITTED]} ☠️`;
        special_killers.append(copiedKiller);
    }
    if (killCounts && DIDNT_SUBMIT in killCounts) {
        const tooSlowKiller = document.createElement('div');
        tooSlowKiller.classList.add('special-killer');
        tooSlowKiller.textContent = `☠️ Too Slow: ${killCounts[DIDNT_SUBMIT]} ☠️`;
        special_killers.append(tooSlowKiller);
    }
    rulesContainer.append(special_killers)
}

// ADDS ANY NEW LIVING USERS RECEIVED BY THE SERVER TO THE DOM
function handleNewLivingUsers(newLivingUsers) {
    
    const fragment = document.createDocumentFragment(); // Create a new fragment
    
    newLivingUsers.forEach((nextUser) => {
        const newLivingUser = document.createElement('div');
        newLivingUser.classList.add('living-user');

        // Add a "highlighter" color splash
        const colorSplashEl = document.createElement('div');
        colorSplashEl.classList.add('living-user-color-splash');
        newLivingUser.append(colorSplashEl);

        const titleContainerEl = document.createElement('div');
        titleContainerEl.classList.add('living-user-title-container');

        const userNameDiv = document.createElement('div');
        userNameDiv.classList.add('living-user-name');
        userNameDiv.textContent = nextUser.username;
        titleContainerEl.append(userNameDiv);

        // Convert the timestamp to readable format
        // Current format is Unix milliseconds, e.g. 1746123456789
        const date = new Date(nextUser.submission_timestamp);
        const h = date.getHours();
        const m = date.getMinutes().toString().padStart(2, '0');
        const s = date.getSeconds().toString().padStart(2, '0');
        const ms = date.getMilliseconds().toString().padStart(3, '0');
        const ampm = h >= 12 ? 'pm' : 'am';
        const hour = h % 12 || 12;
        const formattedTimestamp = `${hour}:${m}${ampm} ${s}:${ms}`;

        const timestampEl = document.createElement('div');
        timestampEl.classList.add('living-user-timestamp');
        timestampEl.textContent = formattedTimestamp;
        titleContainerEl.append(timestampEl);

        newLivingUser.append(titleContainerEl);

        const passwordEl = document.createElement('div');
        passwordEl.classList.add('living-user-password');
        passwordEl.textContent = nextUser.password;
        
        newLivingUser.append(passwordEl);

        // Show score, but only when mouse is over the Living User
        const scoreEl = document.createElement('div');
        scoreEl.classList.add('living-user-score');
        scoreEl.textContent = `${nextUser.password.length}`;
        newLivingUser.append(scoreEl);

        fragment.append(newLivingUser);
    });

    const livingUsersContainer = document.getElementById("living-users-container");
    livingUsersContainer.innerHTML = ''; // wipe it
    livingUsersContainer.append(fragment); // Transfers all the children from fragment
}

// ADDS ANY NEW DEAD USERS RECEIVED BY THE SERVER TO THE DOM
function handleNewDeadUsers(newDeadUsers) {
    
    const fragment = document.createDocumentFragment(); // Create a new fragment
    
    newDeadUsers.forEach((nextUser) => {
        const newDeadUser = document.createElement('div');
        newDeadUser.classList.add('dead-user');

        // Add a red color splash
        const colorSplashEl = document.createElement('div');
        colorSplashEl.classList.add('dead-user-color-splash');
        newDeadUser.append(colorSplashEl);

        const userNameEl = document.createElement('div');
        userNameEl.classList.add('dead-user-name');
        userNameEl.textContent = nextUser.username;

        newDeadUser.append(userNameEl);

        const infoContainerEl = document.createElement('div');
        infoContainerEl.classList.add('dead-user-info-container');

        const passwordEl = document.createElement('div');
        passwordEl.classList.add('dead-user-password');
        passwordEl.textContent = nextUser.password;
        infoContainerEl.append(passwordEl);

        const reasonEl = document.createElement('div');
        reasonEl.classList.add('dead-user-reason');
        reasonEl.textContent = nextUser.failure_message;
        infoContainerEl.append(reasonEl);

        newDeadUser.append(infoContainerEl);

        // Show score, but only when mouse is over the User
        const scoreEl = document.createElement('div');
        scoreEl.classList.add('dead-user-score');
        scoreEl.textContent = `${nextUser.password.length}`;
        newDeadUser.append(scoreEl);

        fragment.append(newDeadUser);
    });

    const deadUsersContainer = document.getElementById("dead-users-container");
    deadUsersContainer.innerHTML = ''; // wipe it
    deadUsersContainer.append(fragment); // Transfers all the children from fragment

    // Lastly, update the "X DEATHS" subtitle
    const deathsSubtitle = document.getElementById("deaths-subtitle");
    deathsSubtitle.textContent = `${newDeadUsers.length} DEATHS`;
}

const TIME_PER_POLL = 2000;
let lastCheckTimestamp = null;

setInterval(async () => {
    try {
        let requestUrl = '/api/passwords';
        if (lastCheckTimestamp) {
            requestUrl = `/api/passwords?since=${lastCheckTimestamp}`;
        }
        const response = await fetch(requestUrl);
        const data = await response.json();

        // If request failed, or if there wasn't new data, just return
        if (!data.success || data.noNewData) {
            return;
        }

        let newRules = data.rules;
        let killCounts = data.killCounts;
        if (newRules) {
            handleNewRules(newRules, killCounts);
        }

        let newLivingUsers = data.livingUsers;
        if (newLivingUsers) {
            handleNewLivingUsers(newLivingUsers);
        }

        let newDeadUsers = data.deadUsers;
        if (newDeadUsers) {
            handleNewDeadUsers(newDeadUsers);
        }

        // If the game state is different from before, update the visuals
        let newGameState = data.gameState;
        if (newGameState && newGameState !== currentGameState) {
            currentGameState = newGameState;
            handleNewGameState(newGameState);
        }

        // The number of living users, displayed as a subtitle
        // This data field exists because the Living Users array will be empty during the ACCEPTING SUBISSIONS phase, to prevent cheating
        let livingUsersCount = data.livingUsersCount;
        if (livingUsersCount != null) {
            const roundSubtitle = document.getElementById("round-subtitle");
            roundSubtitle.textContent = `${livingUsersCount} ALIVE`;
        }
        
        // Update our timestamp to prevent the server from pulling the DB unnecessarily in the future
        lastCheckTimestamp = data.serverTimestamp;
        
    } catch (error) {
        console.error('Server polling error error:', error);
    }
}, TIME_PER_POLL);


///////////////////////////
//      ANIMATIONS
///////////////////////////


startPageBackground(document.body);

// ADDS GAME STATE RECEIVED BY THE SERVER
function handleNewGameState(newGameState) {
    const animatedBg = document.querySelector('.animated-bg');
    const titlesContainer = document.getElementById("titles-container");
    titlesContainer.classList.remove('titles-state-accepting', 'titles-state-intermission');
    if (newGameState === "ACCEPTING_SUBMISSIONS") {
        titlesContainer.classList.add('titles-state-accepting');
        document.body.classList.add('accepting-submissions');
        document.body.classList.remove('accepting-submissions');
        animatedBg.style.opacity = 1.0;
        setBgStarSpeed(8);
    } else if (newGameState === "INTERMISSION") {
        titlesContainer.classList.add('titles-state-intermission');
        animatedBg.style.opacity = 0.2;
        setBgStarSpeed(1.5);
    }
}

let currentGameState = "ACCEPTING_SUBMISSIONS"
handleNewGameState(currentGameState);

import Letterize from "https://cdn.skypack.dev/letterizejs@2.0.0";
import anime from "https://esm.sh/animejs@3.2.1";

// Animate the title using Letterize and Anime libraries
// Example here: https://wojciechkrakowiak.github.io/letterize/examples/
const titleAnimation = new Letterize({targets: "#title", className: "letter"});
var animation = anime.timeline({
    targets: titleAnimation.listAll,
    delay: anime.stagger(50),
    loop: true
});
animation
    .add({translateY: -3, scale: 1.03, duration: 1000})
    .add({duration: 1000}) // pause for 1 second with no property changes
    .add({translateY: 0, scale: 1, duration: 1000});


///////////////////////////
//      TESTING
///////////////////////////

// document.addEventListener('keydown', (event) => {
//     if (event.shiftKey && event.key === "ArrowLeft") {
//         currentGameState = "INTERMISSION"
//         handleNewGameState(currentGameState);
//     } else if (event.shiftKey && event.key === "ArrowRight") {
//         currentGameState = "ACCEPTING_SUBMISSIONS"
//         handleNewGameState(currentGameState);
//     }
// });
