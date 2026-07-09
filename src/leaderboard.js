import './leaderboard.css'
import { startPageBackground } from './animated-bg.js';

// ADDS THE PERSISTENT (CROSS-MATCH) LEADERBOARD RECEIVED BY THE SERVER TO THE DOM
function handleNewLeaderboard(leaderboard) {
    const players = leaderboard.players || {};
    const lifetimeKillCounts = leaderboard.lifetimeKillCounts || {};

    const topWinners = Object.entries(players)
        .filter(([, stats]) => stats.wins > 0)
        .sort((a, b) => b[1].wins - a[1].wins)
        .slice(0, 15);

    const winnersFragment = document.createDocumentFragment();
    topWinners.forEach(([username, stats], index) => {
        const entry = document.createElement('div');
        entry.classList.add('leaderboard-entry');

        const rankEl = document.createElement('span');
        rankEl.classList.add('leaderboard-rank');
        rankEl.textContent = `#${index + 1}`;
        entry.append(rankEl);

        const nameEl = document.createElement('span');
        nameEl.classList.add('leaderboard-name');
        nameEl.textContent = username;
        entry.append(nameEl);

        const winsEl = document.createElement('span');
        winsEl.classList.add('leaderboard-wins');
        winsEl.textContent = `🏆 ${stats.wins} win${stats.wins === 1 ? '' : 's'}`;
        entry.append(winsEl);

        const playedEl = document.createElement('span');
        playedEl.classList.add('leaderboard-played');
        playedEl.textContent = `${stats.matchesPlayed} played`;
        entry.append(playedEl);

        winnersFragment.append(entry);
    });

    const winnersContainer = document.getElementById("leaderboard-winners");
    winnersContainer.innerHTML = '';
    if (topWinners.length === 0) {
        winnersContainer.append(emptyState("No wins recorded yet."));
    } else {
        winnersContainer.append(winnersFragment);
    }

    const topKillers = Object.entries(lifetimeKillCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 15);

    const killersFragment = document.createDocumentFragment();
    topKillers.forEach(([reason, count], index) => {
        const entry = document.createElement('div');
        entry.classList.add('leaderboard-entry');

        const rankEl = document.createElement('span');
        rankEl.classList.add('leaderboard-rank');
        rankEl.textContent = `#${index + 1}`;
        entry.append(rankEl);

        const reasonEl = document.createElement('span');
        reasonEl.classList.add('leaderboard-kill-reason');
        // Strip the {curly brace} highlight markup - plain text here, no highlighting needed
        reasonEl.textContent = reason.replace(/\{([^}]+)\}/g, '$1');
        entry.append(reasonEl);

        const countEl = document.createElement('span');
        countEl.classList.add('leaderboard-kill-count');
        countEl.textContent = `☠️ ${count}`;
        entry.append(countEl);

        killersFragment.append(entry);
    });

    const killersContainer = document.getElementById("leaderboard-killers");
    killersContainer.innerHTML = '';
    if (topKillers.length === 0) {
        killersContainer.append(emptyState("No deaths recorded yet."));
    } else {
        killersContainer.append(killersFragment);
    }
}

function emptyState(text) {
    const el = document.createElement('div');
    el.classList.add('leaderboard-empty-state');
    el.textContent = text;
    return el;
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

        if (!data.success || data.noNewData) {
            return;
        }

        if (data.leaderboard) {
            handleNewLeaderboard(data.leaderboard);
        }

        lastCheckTimestamp = data.serverTimestamp;

    } catch (error) {
        console.error('Leaderboard polling error:', error);
    }
}, TIME_PER_POLL);

startPageBackground(document.body);
