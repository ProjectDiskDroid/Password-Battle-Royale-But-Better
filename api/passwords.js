/*
REDIS DATA STRUCTURES

// Using Redis string for the user sets, instead of hash, because I'm only going to be reading ALL users or writing ALL users
// Hash excels at quickly reading/writing to a single entry, not on giant batch reads of the entire hash
// The client is going to be asking for the entire user set CONSTANTLY, so leaving as string makes it way better

// This is an array of arrays, where each round can have 1-3 rules added
KEY: REDIS_KEY_RULES
STRING: "[
	["rule description 1"], 
	["rule description 2", "rule description 3"], 
	["rule description 4"], 
	["rule description 5", "rule description 6"], 
	["rule description 7", "rule description 8"], 
]"

// This is an array of user dicts, ordered by smallest passwords
// NOTE: on the python side, this will be temporarily converted into a dict
KEY: REDIS_KEY_LIVING_USERS
STRING: "[
	{ username: [USERNAME], password: [PASSWORD], submission_timestamp: [TIME] },
	{ username: [USERNAME], password: [PASSWORD], submission_timestamp: [TIME] },
	{ username: [USERNAME], password: [PASSWORD], submission_timestamp: [TIME] },
	etc
]""

KEY: REDIS_KEY_DEAD_USERS
STRING: "[
	{ username: [USERNAME], password: [PASSWORD], submission_timestamp: [TIME], failure_message: [MESSAGE] },
	{ username: [USERNAME], password: [PASSWORD], submission_timestamp: [TIME], failure_message: [MESSAGE] },
	{ username: [USERNAME], password: [PASSWORD], submission_timestamp: [TIME], failure_message: [MESSAGE] },
	etc
]""

KEY: REDIS_KEY_GAME_STATE
STRING: "ACCEPTING_SUBMISSIONS" / "INTERMISSION"

KEY: REDIS_KEY_KILL_COUNTS
STRING: "{
    "Submitted a password that someone else already had!": 25,
    "Failed to submit a password in time.": 60,
    "Must contain {5+ Characters}": 6,
    "Must include {1+ Uppercase Letter} and {1+ Special Character}": 15
	etc
}"

*/

import {redis, pollLimiter, REDIS_KEY_RULES, REDIS_KEY_LIVING_USERS, REDIS_KEY_DEAD_USERS, REDIS_KEY_LAST_UPDATED_TIMESTAMP, REDIS_KEY_GAME_STATE, REDIS_KEY_KILL_COUNTS} from './_lib/redis.js';

 // 'UPDATE_DB_KEY' is an env variable that I set on Vercel - only a client who has this same var can update the server
const CLIENT_SECRET = process.env.UPDATE_DB_KEY;  

export default async function handler(req, res) {

	if (req.method === "GET") {
		try {

			// Get some kind of unique ID for this user, then check rate limit
			const ip = req.headers['x-forwarded-for']?.split(',')[0].trim() || req.headers['x-real-ip'] || req.socket?.remoteAddress || `anon-${Date.now()}`;  // last resort: never collide
			const { success, remaining } = await pollLimiter.limit(ip);
			if (!success) {
				return res.status(429).json({ success: false, error: 'Rate limited' });
			}

			// Do a check to see if the DB has actually been updated since the client's last call
			let clientSince = req.query.since;
			let lastUpdated = await redis.get(REDIS_KEY_LAST_UPDATED_TIMESTAMP)
			if (clientSince && lastUpdated && Number(clientSince) >= Number(lastUpdated)) {
				return res.status(200).json({ success: true, noNewData: true });
			}

			// Retrieve all rules, living users, and dead users for the client
			// Promise.all fires all three requests at the same time and waits for all of them to finish before continuing, makes it much faster
			const [rules, livingUsers, deadUsers, gameState, killCounts] = await Promise.all([
				redis.get(REDIS_KEY_RULES),
				redis.get(REDIS_KEY_LIVING_USERS),
				redis.get(REDIS_KEY_DEAD_USERS),
				redis.get(REDIS_KEY_GAME_STATE),
				redis.get(REDIS_KEY_KILL_COUNTS),
			]);

			// The client needs to display the number of living users, but we don't want to send the full array of valid answers during submissions phase (since people could copy it)
			// So we just calculate the number here for client
			// UPDATE: this isn't relevant anymore due to changes I made on stream, now we're sending the livingUsers array to the client at all times anyways (just with empty passwords during the SUBMISSION phase). Leaving this in for now, will remove if I make future updates
			let livingUsersCount = livingUsers?.length ?? 0;
		
			res.status(200).json({ 
				success: true,
				rules: rules,
				livingUsers: livingUsers,
				deadUsers: deadUsers,
				gameState: gameState,
				serverTimestamp: lastUpdated,
				killCounts: killCounts,
				livingUsersCount: livingUsersCount
			});

		} catch (error) {
			console.error('Redis GET error:', error);
			return res.status(500).json({success: false, error: 'Failed to retrieve users and/or rules! Im sowwy 😨🥵'});
		}
	}

	else if (req.method === "POST") {
		try {
			const { clientSecret, rules, livingUsers, deadUsers, gameState, killCounts } = req.body;

			console.log("VERCEL DEBUG: Got POST");

			// Check client has permission
			if (clientSecret !== CLIENT_SECRET) return res.status(401).end("Unauthorized mofo!!");

			console.log("VERCEL DEBUG: Client has permission");
			
			// Update our Redis DB with the new info
			let res_message = "Successfully updated.";
			let anythingUpdated = false;
			const pipeline = redis.multi(); // This collects multiple commands, then runs them at once

			if (rules) {
				pipeline.set(REDIS_KEY_RULES, JSON.stringify(rules));
				anythingUpdated = true;
				res_message += " Updated rules.";
				console.log("VERCEL DEBUG: Updated rules");
			}
			if (livingUsers) {
				pipeline.set(REDIS_KEY_LIVING_USERS, JSON.stringify(livingUsers));
				anythingUpdated = true;
				res_message += " Updated living users.";
				console.log("VERCEL DEBUG: Updated living users");
			}
			if (deadUsers) {
				pipeline.set(REDIS_KEY_DEAD_USERS, JSON.stringify(deadUsers));
				anythingUpdated = true;
				res_message += " Updated dead users.";
				console.log("VERCEL DEBUG: Updated dead users");
			}
			if (gameState) {
				pipeline.set(REDIS_KEY_GAME_STATE, gameState);
				anythingUpdated = true;
				res_message += " Updated game state.";
				console.log("VERCEL DEBUG: Updated game state");
			}
			if (killCounts) {
				pipeline.set(REDIS_KEY_KILL_COUNTS, JSON.stringify(killCounts));
				anythingUpdated = true;
				res_message += " Updated kill counts.";
				console.log("VERCEL DEBUG: Updated kill counts");
			}

			// If anything was updated, update a timestamp in DB
			if (anythingUpdated) {
				pipeline.set(REDIS_KEY_LAST_UPDATED_TIMESTAMP, Date.now());
			}

			await pipeline.exec();
			
			res.status(200).json({ 
				success: true,
				message: res_message,
			});

		} catch (error) {
			console.error('Redis SET error:', error);
			return res.status(500).json({success: false, error: 'Failed to update users and/or rules'});
		}
	} 

	else {
		return res.status(405).end("Method Not Allowed");
	}
	
}
