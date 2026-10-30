# Kohinoor Plywood website

A responsive Flask + HTML/CSS/JavaScript + Supabase starter implementation based on the SynexAI Kohinoor Plywood brief.

## Before development / client use
The brief requires written founder approval of the UI concept before development, and approval of the alternative Flask + Supabase stack. Treat this project as a proposed implementation until those approvals are received.

## Features included
- Responsive home page, navigation and mobile enquiry bar
- Product listing and structured product detail pages
- Interactive Ply Finder with pre-filled quote form
- Professionals, dealer application, about/quality, city pages and buying guides
- Two-step quote form
- Supabase persistence for quote leads, dealer applications and event tracking
- SEO metadata, sitemap.xml, robots.txt, canonical links and JSON-LD
- WhatsApp and telephone enquiry links
- Reduced-motion support

## 1. Run locally
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```
Edit `.env`, then:
```bash
python app.py
```
Open http://127.0.0.1:5000

## 2. Configure Supabase
1. Create a Supabase project.
2. Open SQL Editor and run `supabase/schema.sql`.
3. Copy the Project URL and service-role key into `.env`.
4. Keep the service-role key server-side only. Never put it in `static/js/` or templates.
5. Set a strong `FLASK_SECRET_KEY`.

If Supabase is not configured, the pages still run, but submissions will not be persisted. Configure it before accepting real leads.

## 3. Brand content that must be confirmed
Replace the placeholders in `.env`: phone, WhatsApp number, email, address and opening hours.
Confirm the official logo, brand colours, real product images, dealer details, certificates, warranty terms and product specifications with SynexAI/founders.
The brief says certification and warranty figures go live only after certificates have been reviewed. The figures in the product content are therefore not represented as independently verified claims.
All external photography currently used is illustrative placeholder photography. Replace it with approved client-owned/licensed imagery before launch. Do not use AI-generated images on the final site without founder approval.

## 4. Deploy
Use a private/unlisted/password-protected preview. Example start command:
`gunicorn app:app`
Set all environment variables in the hosting dashboard. Do not commit `.env`.

## 5. QA checklist
- Test at 360px, 390px, tablet and desktop widths.
- Test every quote, dealer, WhatsApp and call CTA.
- Confirm inserts appear in Supabase tables.
- Verify phone/email/address and all product claims.
- Test keyboard navigation, labels, focus states and reduced motion.
- Run Lighthouse on Home and a product page; targets in the brief are goals, not guaranteed scores.
- Add GA4/Google Tag Manager and Meta Pixel IDs only after the client/founders provide them.
- Add email notification / Google Sheets / CRM webhook integration after approved credentials and destinations are supplied.

## 6. Project structure
- `app.py`: Flask routes and server-side Supabase writes
- `templates/`: server-rendered pages
- `static/css/style.css`: responsive visual system
- `static/js/main.js`: menus, forms, finder and event tracking
- `supabase/schema.sql`: database tables and RLS
