# Kohinoor Plywood — Iteration 2 implementation notes

## Implemented in this pass
- Rebuilt the homepage hero as a full-bleed, plywood-first section with a self-hosted WebP plywood-layer visual, bottom-left headline, material/category trust line, Ply Finder CTA, responsive mobile crop, and reduced-motion-aware entrance.
- Added `/products/<slug>` product detail URLs and 301 redirects from the old `/<slug>` product URLs.
- Added catalogue search across product name, grade, category and description, while preserving category filters.
- Added a responsive Products mega menu with links to the existing catalogue groups and Ply Finder.
- Reworked the catalogue and product detail layouts, added related materials, product/breadcrumb JSON-LD, canonical URLs and per-product meta descriptions.
- Added a branded 404 page.
- Sanitised the configured placeholder phone and WhatsApp numbers so they are not rendered in public templates.
- Fixed the intro so it only runs on the homepage, once per browser session, is skippable and is bypassed for reduced-motion users.
- Removed scroll-reveal animations from every section; retained restrained product hover behaviour.
- Added mobile bottom action spacing and improved menu accessibility state.

## Not complete / requires Kohinoor-supplied facts or deployment access
- The product catalogue still contains the original grouped product records. Individual stock confirmation is required before splitting Laminates/Veneers, timber species, MDF/HDHMR/particle board, block board and flush doors into separate pages.
- Product pages do not yet meet the 500–800 word target. Verified technical data, grades, IS standards, core, glue, density, available sheet sizes, warranty and use limitations are required; no specifications have been invented.
- Most non-hero images remain externally hosted in the original templates/data. The homepage hero now uses a self-hosted WebP plywood-layer visual. The remaining site-wide photography replacement still requires approved plywood/timber images.
- Zodiak/Switzer WOFF2 font files are not included. Add properly licensed font files under `public/fonts/` and define local `@font-face` rules before launch.
- Real logo SVG, verified phone/WhatsApp, showroom address, hours, map coordinates and contact destinations are still required.
- Quote submission still depends on configured Supabase credentials and the existing `quote_leads` table. Email/WhatsApp/sheet delivery and end-to-end submission must be tested in the deployed environment.
- LocalBusiness schema, full FAQ schema, social share images, four full Insights articles, Google Search Console submission, Lighthouse score and physical-device QA remain outstanding.

## Local run
Install `requirements.txt`, configure environment variables as described in `README.md`, then run `python app.py` (or `flask --app app run`).
