// Pixelcoin API: accounts, login sessions, mining and transfers, all stored in
// Netlify Database so a wallet and the blockchain follow the user to any device.
import type { Config } from "@netlify/functions";
import { createHash, randomBytes, scrypt as scryptCb, timingSafeEqual } from "node:crypto";
import { promisify } from "node:util";
import { and, asc, desc, eq, gt, ne, sql } from "drizzle-orm";
import { db } from "../../db/index.js";
import { accounts, blocks, sessions } from "../../db/schema.js";

const scrypt = promisify(scryptCb) as (password: string, salt: Buffer, keylen: number) => Promise<Buffer>;

// Blockchain rules (same values the app used when it ran locally)
const MAX_SUPPLY = 21_000_000;
const INITIAL_REWARD = 50;
const HALVING_INTERVAL = 210000;
const INITIAL_DIFFICULTY = 4;
const ELECTRICITY_COST_PER_BLOCK = 0.15;
const MINING_LOCK_ID = 7_420_001;

// Developer wallet that the app has always created with a starting balance.
const DEVELOPER_EMAIL = "trippy1121@icloud.com";
const DEVELOPER_PASSWORD_HASH = "scrypt:ba23fa2f282bdeb15500fe32c7c750ed:ae43495c404edebcc3340fec11b114d8f5db8b54414696a7c7ddc675a7ebb65983df5012124ab6f646f1e329b001fa93fb27d44f67ac4a783203102610a95e89";
const DEVELOPER_BALANCE = 1050000;

type Account = typeof accounts.$inferSelect;
type BlockRow = typeof blocks.$inferSelect;

class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

function json(data: unknown, status = 200) {
  return Response.json(data, { status });
}

// --- Hashing helpers -------------------------------------------------------

async function hashPassword(password: string) {
  const salt = randomBytes(16);
  const hash = await scrypt(password, salt, 64);
  return `scrypt:${salt.toString("hex")}:${hash.toString("hex")}`;
}

async function verifyPassword(password: string, stored: string) {
  const [scheme, saltHex, hashHex] = stored.split(":");
  if (scheme !== "scrypt" || !saltHex || !hashHex) return false;
  const expected = Buffer.from(hashHex, "hex");
  const actual = await scrypt(password, Buffer.from(saltHex, "hex"), expected.length);
  return timingSafeEqual(actual, expected);
}

function hashToken(token: string) {
  return createHash("sha256").update(token).digest("hex");
}

function generateKeyPair() {
  return {
    publicKey: `0X${randomBytes(13).toString("hex").toUpperCase()}`,
    privateKey: randomBytes(32).toString("hex").toUpperCase(),
  };
}

// The block hash function the app has always used, kept so existing blocks
// and newly mined ones look the same.
function calculateHash(block: { index: number; timestamp: number; previousHash: string; nonce: number; miner: string; reward: number }) {
  const data = `${block.index}${block.timestamp}${block.previousHash}${block.nonce}${block.miner}${block.reward}`;
  let hash = 0;
  for (let i = 0; i < data.length; i++) {
    hash = (hash << 5) - hash + data.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash).toString(16).padStart(64, "0");
}

function calculateReward(blockHeight: number, totalMined: number) {
  if (totalMined >= MAX_SUPPLY) return 0;
  const halvings = Math.floor(blockHeight / HALVING_INTERVAL);
  return Math.min(INITIAL_REWARD / Math.pow(2, halvings), MAX_SUPPLY - totalMined);
}

function difficultyFor(chainLength: number) {
  return INITIAL_DIFFICULTY + Math.floor((chainLength - 1) / 10);
}

// --- Serializers -----------------------------------------------------------

function toWallet(account: Account) {
  return {
    email: account.email,
    publicKey: account.publicKey,
    privateKey: account.privateKey,
    balance: account.balance,
  };
}

function toStats(account: Account | null) {
  return {
    blocksMined: account?.blocksMined ?? 0,
    stats: {
      totalElectricityUsed: account?.electricityUsed ?? 0,
      totalElectricityCost: account?.electricityCost ?? 0,
    },
  };
}

function toBlock(row: BlockRow) {
  return {
    index: row.blockIndex,
    timestamp: row.timestamp,
    previousHash: row.previousHash,
    nonce: row.nonce,
    miner: row.miner,
    reward: row.reward,
    hash: row.hash,
  };
}

// --- Data access -----------------------------------------------------------

async function ensureDeveloperAccount() {
  await db
    .insert(accounts)
    .values({ email: DEVELOPER_EMAIL, passwordHash: DEVELOPER_PASSWORD_HASH, balance: DEVELOPER_BALANCE, ...generateKeyPair() })
    .onConflictDoNothing({ target: accounts.email });
}

async function ensureGenesisBlock() {
  const genesis = { index: 0, timestamp: Date.now(), previousHash: "0", nonce: 0, miner: "genesis", reward: 0 };
  await db
    .insert(blocks)
    .values({ ...genesis, blockIndex: 0, hash: calculateHash(genesis) })
    .onConflictDoNothing({ target: blocks.blockIndex });
}

async function accountFromRequest(req: Request): Promise<Account | null> {
  const header = req.headers.get("authorization") || "";
  const token = header.startsWith("Bearer ") ? header.slice(7).trim() : "";
  if (!token) return null;
  const [row] = await db
    .select({ account: accounts })
    .from(sessions)
    .innerJoin(accounts, eq(sessions.accountId, accounts.id))
    .where(eq(sessions.token, hashToken(token)))
    .limit(1);
  return row?.account ?? null;
}

async function requireAccount(req: Request) {
  const account = await accountFromRequest(req);
  if (!account) throw new HttpError(401, "Please log in again");
  return account;
}

async function startSession(account: Account) {
  const token = randomBytes(32).toString("hex");
  await db.insert(sessions).values({ token: hashToken(token), accountId: account.id });
  return { token, wallet: toWallet(account) };
}

async function readCredentials(req: Request) {
  const body = await req.json().catch(() => ({}));
  const email = String(body.email ?? "").trim().toLowerCase();
  const password = String(body.password ?? "");
  if (!email || !password) throw new HttpError(400, "Please fill in all fields");
  return { email, password };
}

// --- Route handlers --------------------------------------------------------

async function signup(req: Request) {
  const { email, password } = await readCredentials(req);
  await ensureDeveloperAccount();
  const [account] = await db
    .insert(accounts)
    .values({ email, passwordHash: await hashPassword(password), ...generateKeyPair() })
    .onConflictDoNothing({ target: accounts.email })
    .returning();
  if (!account) throw new HttpError(409, "Wallet with this email already exists");
  return json(await startSession(account), 201);
}

async function login(req: Request) {
  const { email, password } = await readCredentials(req);
  await ensureDeveloperAccount();
  const [account] = await db.select().from(accounts).where(eq(accounts.email, email)).limit(1);
  if (!account) throw new HttpError(404, "Wallet not found");
  if (!(await verifyPassword(password, account.passwordHash))) throw new HttpError(401, "Invalid password");
  return json(await startSession(account));
}

async function logout(req: Request) {
  const header = req.headers.get("authorization") || "";
  const token = header.startsWith("Bearer ") ? header.slice(7).trim() : "";
  if (token) await db.delete(sessions).where(eq(sessions.token, hashToken(token)));
  return json({ ok: true });
}

async function session(req: Request) {
  const account = await requireAccount(req);
  return json({ wallet: toWallet(account) });
}

async function getChain(req: Request) {
  await ensureGenesisBlock();
  const account = await accountFromRequest(req);
  const rows = await db.select().from(blocks).orderBy(asc(blocks.blockIndex));
  const totalMined = rows.reduce((sum, b) => sum + b.reward, 0);
  return json({
    chain: rows.map(toBlock),
    totalMined,
    difficulty: difficultyFor(rows.length),
    balance: account?.balance ?? 0,
    ...toStats(account),
  });
}

async function mine(req: Request) {
  const account = await requireAccount(req);
  const body = await req.json().catch(() => ({}));
  const sinceIndex = Number.isInteger(body.sinceIndex) ? body.sinceIndex : -1;
  await ensureGenesisBlock();

  const result = await db.transaction(async (tx) => {
    // Only one block can be mined at a time across all users.
    await tx.execute(sql`select pg_advisory_xact_lock(${MINING_LOCK_ID})`);

    const [tip] = await tx.select().from(blocks).orderBy(desc(blocks.blockIndex)).limit(1);
    const [{ totalMined }] = await tx
      .select({ totalMined: sql<number>`coalesce(sum(${blocks.reward}), 0)::float8` })
      .from(blocks);
    const chainLength = tip.blockIndex + 1;
    const reward = calculateReward(chainLength, totalMined);
    if (reward === 0) throw new HttpError(400, "Maximum supply reached!");

    const candidate = {
      index: tip.blockIndex + 1,
      timestamp: Date.now(),
      previousHash: tip.hash,
      nonce: 0,
      miner: account.publicKey,
      reward,
    };
    const target = "0".repeat(difficultyFor(chainLength));
    let hash = "";
    while (!hash.startsWith(target)) {
      candidate.nonce++;
      hash = calculateHash(candidate);
    }

    const [block] = await tx
      .insert(blocks)
      .values({
        blockIndex: candidate.index,
        timestamp: candidate.timestamp,
        previousHash: candidate.previousHash,
        nonce: candidate.nonce,
        miner: candidate.miner,
        reward,
        hash,
        minerAccountId: account.id,
      })
      .returning();

    const [updated] = await tx
      .update(accounts)
      .set({
        balance: sql`${accounts.balance} + ${reward - ELECTRICITY_COST_PER_BLOCK}`,
        blocksMined: sql`${accounts.blocksMined} + 1`,
        electricityUsed: sql`${accounts.electricityUsed} + ${ELECTRICITY_COST_PER_BLOCK}`,
        electricityCost: sql`${accounts.electricityCost} + ${ELECTRICITY_COST_PER_BLOCK * 0.05}`,
      })
      .where(eq(accounts.id, account.id))
      .returning();

    return { block, updated, totalMined: totalMined + reward, chainLength: chainLength + 1 };
  });

  // Include any blocks other miners added since this device last synced.
  const newBlocks = await db
    .select()
    .from(blocks)
    .where(gt(blocks.blockIndex, sinceIndex))
    .orderBy(asc(blocks.blockIndex));

  return json({
    block: toBlock(result.block),
    newBlocks: newBlocks.map(toBlock),
    reward: result.block.reward - ELECTRICITY_COST_PER_BLOCK,
    electricityCost: ELECTRICITY_COST_PER_BLOCK,
    totalMined: result.totalMined,
    difficulty: difficultyFor(result.chainLength),
    balance: result.updated.balance,
    wallet: toWallet(result.updated),
    ...toStats(result.updated),
  });
}

async function send(req: Request) {
  const account = await requireAccount(req);
  const body = await req.json().catch(() => ({}));
  const recipientAddress = String(body.recipientAddress ?? "").trim();
  const amount = Number(body.amount);
  if (!Number.isFinite(amount) || amount <= 0) throw new HttpError(400, "Amount must be greater than 0");

  const updated = await db.transaction(async (tx) => {
    const [recipient] = await tx
      .select()
      .from(accounts)
      .where(and(eq(accounts.publicKey, recipientAddress), ne(accounts.id, account.id)))
      .limit(1);
    if (!recipient) throw new HttpError(404, "Recipient wallet not found");

    // Only deduct when the balance covers the amount, so two transfers at
    // once can't overdraw the wallet.
    const [sender] = await tx
      .update(accounts)
      .set({ balance: sql`${accounts.balance} - ${amount}` })
      .where(and(eq(accounts.id, account.id), sql`${accounts.balance} >= ${amount}`))
      .returning();
    if (!sender) throw new HttpError(400, "Insufficient balance");

    await tx
      .update(accounts)
      .set({ balance: sql`${accounts.balance} + ${amount}` })
      .where(eq(accounts.id, recipient.id));
    return sender;
  });

  return json({ wallet: toWallet(updated) });
}

// --- Router ----------------------------------------------------------------

const routes: Record<string, (req: Request) => Promise<Response>> = {
  "POST /api/auth/signup": signup,
  "POST /api/auth/login": login,
  "POST /api/auth/logout": logout,
  "GET /api/session": session,
  "GET /api/chain": getChain,
  "POST /api/mine": mine,
  "POST /api/wallet/send": send,
};

export default async (req: Request) => {
  const { pathname } = new URL(req.url);
  const handler = routes[`${req.method} ${pathname.replace(/\/$/, "")}`];
  if (!handler) return json({ error: "Not found" }, 404);
  try {
    return await handler(req);
  } catch (err) {
    if (err instanceof HttpError) return json({ error: err.message }, err.status);
    console.error(err);
    return json({ error: "Something went wrong" }, 500);
  }
};

export const config: Config = {
  path: "/api/*",
};
