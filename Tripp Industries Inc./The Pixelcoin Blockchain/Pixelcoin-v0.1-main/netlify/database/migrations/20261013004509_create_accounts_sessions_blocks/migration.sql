CREATE TABLE "accounts" (
	"id" serial PRIMARY KEY,
	"email" text NOT NULL UNIQUE,
	"password_hash" text NOT NULL,
	"public_key" text NOT NULL UNIQUE,
	"private_key" text NOT NULL,
	"balance" double precision DEFAULT 0 NOT NULL,
	"blocks_mined" integer DEFAULT 0 NOT NULL,
	"electricity_used" double precision DEFAULT 0 NOT NULL,
	"electricity_cost" double precision DEFAULT 0 NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "blocks" (
	"id" serial PRIMARY KEY,
	"block_index" integer NOT NULL UNIQUE,
	"timestamp" bigint NOT NULL,
	"previous_hash" text NOT NULL,
	"nonce" integer NOT NULL,
	"miner" text NOT NULL,
	"reward" double precision NOT NULL,
	"hash" text NOT NULL,
	"miner_account_id" integer
);
--> statement-breakpoint
CREATE TABLE "sessions" (
	"token" text PRIMARY KEY,
	"account_id" integer NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "blocks" ADD CONSTRAINT "blocks_miner_account_id_accounts_id_fkey" FOREIGN KEY ("miner_account_id") REFERENCES "accounts"("id") ON DELETE SET NULL;--> statement-breakpoint
ALTER TABLE "sessions" ADD CONSTRAINT "sessions_account_id_accounts_id_fkey" FOREIGN KEY ("account_id") REFERENCES "accounts"("id") ON DELETE CASCADE;