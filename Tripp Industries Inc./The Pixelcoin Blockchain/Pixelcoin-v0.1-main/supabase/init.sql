-- Supabase initialization SQL for Pixelcoin app
-- Creates basic `users`, `wallets`, and `blocks` tables expected by the Netlify Functions.

-- Enable UUID generation (pgcrypto)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table (simple email-based users)
CREATE TABLE IF NOT EXISTS public.users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

-- Wallets table
CREATE TABLE IF NOT EXISTS public.wallets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES public.users(id) ON DELETE CASCADE,
  address text,
  balance numeric DEFAULT 0,
  data jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

-- Blocks table (basic blockchain record)
CREATE TABLE IF NOT EXISTS public.blocks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "index" integer,
  timestamp timestamptz DEFAULT now(),
  previous_hash text,
  hash text,
  nonce integer,
  data jsonb DEFAULT '{}'::jsonb,
  created_at timestamptz DEFAULT now()
);

-- Recommended: Add RLS policies and proper auth in production.

-- Indexes
CREATE INDEX IF NOT EXISTS idx_blocks_index ON public.blocks ("index");
CREATE INDEX IF NOT EXISTS idx_wallets_user_id ON public.wallets (user_id);
