-- Run in Supabase SQL Editor.
-- The Flask server writes with the service-role key, which must remain server-side.
create extension if not exists pgcrypto;

create table if not exists public.leads (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  phone text not null,
  customer_type text not null,
  product text,
  thickness text,
  quantity text,
  finish text,
  location text,
  address text,
  message text,
  source_page text,
  created_at timestamptz not null default now()
);

create table if not exists public.dealer_applications (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  phone text not null,
  business text,
  city text not null,
  gst text,
  brands text,
  monthly_volume text,
  created_at timestamptz not null default now()
);

create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null,
  category text not null,
  description text,
  specifications jsonb not null default '{}'::jsonb,
  published boolean not null default false,
  created_at timestamptz not null default now()
);

alter table public.leads enable row level security;
alter table public.dealer_applications enable row level security;
alter table public.products enable row level security;

-- No anon/authenticated policies are created for leads or dealer applications.
-- Do not expose the service-role key to browsers. Access leads only through trusted server code.
-- Add a narrowly scoped SELECT policy for published products only if using browser-side reads.
create policy "Public can read published products"
on public.products for select to anon, authenticated
using (published = true);
grant select on public.products to anon, authenticated;


-- Admin inbox support. Safe to run on an existing project.
alter table public.leads add column if not exists status text not null default 'New';
alter table public.dealer_applications add column if not exists status text not null default 'New';
create index if not exists leads_created_at_idx on public.leads (created_at desc);
create index if not exists dealer_applications_created_at_idx on public.dealer_applications (created_at desc);
