import { bigint, doublePrecision, integer, pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";

// One row per wallet account. Balances live on the server so they follow the
// account to any device.
export const accounts = pgTable("accounts", {
  id: serial().primaryKey(),
  email: text().notNull().unique(),
  passwordHash: text("password_hash").notNull(),
  publicKey: text("public_key").notNull().unique(),
  privateKey: text("private_key").notNull(),
  balance: doublePrecision().notNull().default(0),
  blocksMined: integer("blocks_mined").notNull().default(0),
  electricityUsed: doublePrecision("electricity_used").notNull().default(0),
  electricityCost: doublePrecision("electricity_cost").notNull().default(0),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Login sessions. The token is kept in the browser and sent with each request.
export const sessions = pgTable("sessions", {
  token: text().primaryKey(),
  accountId: integer("account_id")
    .notNull()
    .references(() => accounts.id, { onDelete: "cascade" }),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// The shared Pixelcoin blockchain. `blockIndex` is unique so two miners can
// never append the same height.
export const blocks = pgTable("blocks", {
  id: serial().primaryKey(),
  blockIndex: integer("block_index").notNull().unique(),
  timestamp: bigint({ mode: "number" }).notNull(),
  previousHash: text("previous_hash").notNull(),
  nonce: integer().notNull(),
  miner: text().notNull(),
  reward: doublePrecision().notNull(),
  hash: text().notNull(),
  minerAccountId: integer("miner_account_id").references(() => accounts.id, { onDelete: "set null" }),
});
