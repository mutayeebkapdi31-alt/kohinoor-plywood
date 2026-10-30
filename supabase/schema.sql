-- Run in Supabase SQL Editor. These tables store website enquiries and events.
create extension if not exists pgcrypto;

create table if not exists public.quote_leads (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  phone text not null,
  customer_type text not null,
  product text not null,
  thickness text,
  quantity text,
  finish text,
  delivery_location text not null,
  address text,
  source_page text,
  created_at timestamptz not null default now()
);

create table if not exists public.dealer_applications (
  id uuid primary key default gen_random_uuid(),
  contact_name text not null,
  business_name text not null,
  phone text not null,
  email text,
  city text,
  gst_number text,
  current_brands text,
  monthly_volume text,
  created_at timestamptz not null default now()
);

create table if not exists public.site_events (
  id uuid primary key default gen_random_uuid(),
  event_name text not null,
  page text,
  created_at timestamptz not null default now()
);

alter table public.quote_leads enable row level security;
alter table public.dealer_applications enable row level security;
alter table public.site_events enable row level security;

-- No public policies are intentionally created.
-- Flask writes using the service-role key on the server only.
-- Never expose SUPABASE_SERVICE_ROLE_KEY in HTML or JavaScript.
