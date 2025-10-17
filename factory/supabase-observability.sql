-- Factory observability tables
-- Run in Supabase SQL editor

create table if not exists public.factory_apps (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null,
  repo text,
  created_at timestamptz default now()
);

create table if not exists public.factory_ai_events (
  id uuid primary key default gen_random_uuid(),
  app text not null,
  service text not null,
  status text not null,
  fallback_used boolean default false,
  processing_time_ms integer,
  metadata jsonb,
  created_at timestamptz default now()
);

create table if not exists public.factory_ai_errors (
  id uuid primary key default gen_random_uuid(),
  app text not null,
  service text not null,
  status text not null,
  fallback_used boolean default false,
  processing_time_ms integer,
  error text,
  metadata jsonb,
  created_at timestamptz default now()
);

create table if not exists public.factory_test_runs (
  id uuid primary key default gen_random_uuid(),
  app text not null,
  pipeline text not null,
  status text not null,
  details text,
  created_at timestamptz default now()
);

create table if not exists public.factory_generic_events (
  id uuid primary key default gen_random_uuid(),
  app text not null,
  name text not null,
  payload jsonb,
  created_at timestamptz default now()
);

alter table public.factory_ai_events enable row level security;
alter table public.factory_ai_errors enable row level security;
alter table public.factory_test_runs enable row level security;
alter table public.factory_generic_events enable row level security;

create policy "Allow inserts from anon" on public.factory_ai_events
  for insert
  to anon
  with check (true);

create policy "Allow inserts from anon" on public.factory_ai_errors
  for insert
  to anon
  with check (true);

create policy "Allow inserts from anon" on public.factory_test_runs
  for insert
  to anon
  with check (true);

create policy "Allow inserts from anon" on public.factory_generic_events
  for insert
  to anon
  with check (true);
