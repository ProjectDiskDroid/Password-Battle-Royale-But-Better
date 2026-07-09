import { Redis } from '@upstash/redis';
import { Ratelimit } from '@upstash/ratelimit';

export const redis = new Redis({
  url: process.env.KV_REST_API_URL,
  token: process.env.KV_REST_API_TOKEN,
});

export const pollLimiter = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(120, '10 s'),
  prefix: 'rl:poll',
})

export const REDIS_KEY_RULES = 'password:rules';
export const REDIS_KEY_LIVING_USERS = 'password:users:alive';
export const REDIS_KEY_DEAD_USERS = 'password:users:dead';
export const REDIS_KEY_LAST_UPDATED_TIMESTAMP = 'password:lastUpdated';
export const REDIS_KEY_GAME_STATE = 'password:gameState';
export const REDIS_KEY_KILL_COUNTS = 'password:killCounts';