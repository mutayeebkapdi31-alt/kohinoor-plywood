-- ============================================================
-- KOHINOOR PLYWOOD - FULL ADMIN DATABASE MIGRATION
-- Existing tables:
--   public.quote_leads
--   public.dealer_applications
--   public.site_events
--
-- Safe, additive migration. Does not delete existing records.
-- ============================================================

-- 1. Required extension
create extension if not exists pgcrypto;


-- 2. PRODUCTS TABLE
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

-- Add management fields if missing
alter table public.products
    add column if not exists grade text;

alter table public.products
    add column if not exists best_for text;

alter table public.products
    add column if not exists thickness text;

alter table public.products
    add column if not exists warranty text;

alter table public.products
    add column if not exists badge text;

alter table public.products
    add column if not exists image_url text;

alter table public.products
    add column if not exists sort_order integer not null default 100;

alter table public.products
    add column if not exists updated_at timestamptz not null default now();


-- 3. EXISTING CUSTOMER ENQUIRIES TABLE
-- Your actual table is quote_leads, NOT leads.

alter table public.quote_leads
    add column if not exists status text not null default 'New';

alter table public.quote_leads
    add column if not exists created_at timestamptz not null default now();

alter table public.quote_leads
    add column if not exists updated_at timestamptz not null default now();

create index if not exists quote_leads_created_at_idx
    on public.quote_leads (created_at desc);

create index if not exists quote_leads_status_idx
    on public.quote_leads (status);


-- 4. EXISTING DEALER APPLICATIONS TABLE

alter table public.dealer_applications
    add column if not exists status text not null default 'New';

alter table public.dealer_applications
    add column if not exists created_at timestamptz not null default now();

alter table public.dealer_applications
    add column if not exists updated_at timestamptz not null default now();

create index if not exists dealer_applications_created_at_idx
    on public.dealer_applications (created_at desc);

create index if not exists dealer_applications_status_idx
    on public.dealer_applications (status);


-- 5. PRODUCT INDEX

create index if not exists products_sort_order_idx
    on public.products (sort_order, name);


-- 6. WEBSITE CONTENT TABLE

create table if not exists public.site_content (
    id uuid primary key default gen_random_uuid(),
    content_key text unique not null,
    title text not null default '',
    body text not null default '',
    updated_at timestamptz not null default now()
);


-- 7. ENABLE ROW LEVEL SECURITY

alter table public.products enable row level security;
alter table public.quote_leads enable row level security;
alter table public.dealer_applications enable row level security;
alter table public.site_content enable row level security;


-- 8. PRODUCT PUBLIC READ POLICY

drop policy if exists
    "Public can read published products"
    on public.products;

create policy "Public can read published products"
    on public.products
    for select
    to anon, authenticated
    using (published = true);

grant select on public.products to anon, authenticated;


-- 9. WEBSITE CONTENT PUBLIC READ POLICY

drop policy if exists
    "Public can read website content"
    on public.site_content;

create policy "Public can read website content"
    on public.site_content
    for select
    to anon, authenticated
    using (true);

grant select on public.site_content to anon, authenticated;


-- 10. INITIAL PRODUCT CATALOGUE
-- Products are intentionally unpublished until specifications
-- and warranty claims are verified by Kohinoor.

insert into public.products
(slug, name, category, description, grade, best_for,
 thickness, warranty, badge, image_url, sort_order, published)
values
(
    'bwp-plywood',
    'Kohinoor Gold',
    'Plywood',
    'A plywood range for applications where moisture resistance matters.',
    'Verify grade',
    'Kitchens and high-use interiors',
    'Confirm available sizes',
    'Confirm with company',
    'Flagship range',
    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85',
    1,
    false
),
(
    'bwr-plywood',
    'Kohinoor Premium',
    'Plywood',
    'A versatile plywood range for interior applications.',
    'Verify grade',
    'Kitchens, wardrobes and furniture',
    'Confirm available sizes',
    'Confirm with company',
    'Everyday performance',
    'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=85',
    2,
    false
),
(
    'mr-plywood',
    'Kohinoor Classic',
    'Plywood',
    'A plywood option for general interior and furniture applications.',
    'Verify grade',
    'Bedrooms, wardrobes and living spaces',
    'Confirm available sizes',
    'Confirm with company',
    'Interior essential',
    'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=85',
    3,
    false
),
(
    'calibrated-plywood',
    'Calibrated Plywood',
    'Plywood',
    'Plywood designed for consistent thickness and precision fabrication.',
    'Confirm with company',
    'Modular furniture and interiors',
    'Confirm available sizes',
    'Confirm with company',
    'Precision finish',
    'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1200&q=85',
    4,
    false
),
(
    'marine-plywood',
    'Marine Plywood',
    'Plywood',
    'A specialist plywood option for applications requiring enhanced moisture performance.',
    'Confirm with company',
    'Specialist applications',
    'Confirm available sizes',
    'Confirm with company',
    'Specialist application',
    'https://images.unsplash.com/photo-1600607687644-c7171b42498f?auto=format&fit=crop&w=1200&q=85',
    5,
    false
),
(
    'flexible-plywood',
    'Flexible Plywood',
    'Plywood',
    'A flexible panel option for curved furniture and interior details.',
    'Confirm with company',
    'Curved counters, columns and furniture',
    'Confirm available sizes',
    'Confirm with company',
    'Design flexibility',
    'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=85',
    6,
    false
),
(
    'shuttering-plywood',
    'Kohinoor Shield',
    'Plywood',
    'A shuttering plywood range for construction and formwork requirements.',
    'Confirm with company',
    'Construction and formwork',
    'Confirm available sizes',
    'Confirm with company',
    'For construction',
    'https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1200&q=85',
    7,
    false
),
(
    'blockboards',
    'Block Boards & Flush Doors',
    'Boards & Doors',
    'Board and flush-door options for furniture and interior projects.',
    'Confirm with company',
    'Doors, shelves and furniture',
    'Confirm available sizes',
    'Confirm with company',
    'Doors and boards',
    'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=85',
    8,
    false
),
(
    'laminates-veneers',
    'Laminates & Veneers',
    'Surfaces',
    'Decorative surface options for furniture and finished interiors.',
    'Confirm collection',
    'Cabinet fronts, furniture and wall panels',
    'Confirm available sizes',
    'Confirm with company',
    'Finishing touches',
    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85',
    9,
    false
),
(
    'timber-mdf-hdhmr',
    'Timber, MDF & Boards',
    'Boards & Timber',
    'Timber and engineered-board options for interior and furniture projects.',
    'Confirm materials',
    'Interior fit-outs and furniture',
    'Confirm available sizes',
    'Varies by material',
    'One-stop sourcing',
    'https://images.unsplash.com/photo-1600210492493-0946911123ea?auto=format&fit=crop&w=1200&q=85',
    10,
    false
),
(
    'hardware',
    'Hardware & Accessories',
    'Hardware',
    'Hardware and accessory options for furniture installation and fit-outs.',
    'Confirm brands',
    'Furniture installation and fit-outs',
    'Multiple options',
    'Varies by brand',
    'Finishing essentials',
    'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=85',
    11,
    false
)
on conflict (slug) do nothing;


-- 11. INITIAL WEBSITE CONTENT

insert into public.site_content
(content_key, title, body)
values
(
    'home_hero',
    'Built on trust. Made for generations.',
    'The right material makes all the difference. Find plywood, boards, veneers and expert guidance for the spaces you build.'
)
on conflict (content_key) do nothing;


insert into public.site_content
(content_key, title, body)
values
(
    'home_intro',
    'Good work begins with what is underneath.',
    'For over four decades, Kohinoor Timber Traders has helped craftspeople, designers and homeowners choose materials with confidence.'
)
on conflict (content_key) do nothing;


insert into public.site_content
(content_key, title, body)
values
(
    'about_intro',
    'Forty years in the trade. Generations of trust.',
    'A family-run material business that grew from timber trading into a source for plywood and interior materials.'
)
on conflict (content_key) do nothing;


insert into public.site_content
(content_key, title, body)
values
(
    'footer_text',
    '',
    'Four decades of material knowledge, honest guidance and dependable supply.'
)
on conflict (content_key) do nothing;


-- 12. VERIFICATION
-- Check that all expected tables exist.

select
    table_name
from information_schema.tables
where table_schema = 'public'
and table_name in (
    'quote_leads',
    'dealer_applications',
    'site_events',
    'products',
    'site_content'
)
order by table_name;

-- ============================================================
-- END OF KOHINOOR ADMIN MIGRATION
-- ============================================================