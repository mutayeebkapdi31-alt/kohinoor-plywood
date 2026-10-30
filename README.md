# Kohinoor Plywood Website

A Flask + HTML/CSS/JavaScript + Supabase starter implementation based on the SynexAI Kohinoor Plywood brief.

## Important before use
- This is an implementation starter, not a final approved client release.
- The brief requires written founder approval of the UI concept before development.
- Product certification, warranty, stock, phone, address, timings, map and business claims must be verified by SynexAI / Kohinoor before publishing.
- Current image URLs are visual placeholders from Unsplash. Replace with client-approved, real product/interior photography. The brief says AI-generated imagery must not be used on the final site without approval.
- The city pages are templates with editable local copy. Confirm actual serviceability and local details before publishing each city page.

## Visual refinement update
The homepage has been refined into a more editorial, premium layout with a shorter message hierarchy, a clearer quote/WhatsApp path, application photography, a focused flagship product feature, a compact product range and a simpler final enquiry section. Product listing and detail pages now use semantic image elements with descriptive alt text and lazy loading where appropriate.

The current photography is sourced from Unsplash as temporary real-photo stock imagery. Replace it with Kohinoor-approved product, warehouse, timber-grain, workshop and finished-interior photographs before final client handover. Do not present stock photography as Kohinoor's own products or premises.

## 1. Create Supabase project
Create a project at https://supabase.com, then open SQL Editor and run `schema.sql`.

Copy the Project URL and the server-side service role key from Project Settings / API Keys. The service-role key bypasses RLS, so keep it only in the Flask server environment. Never put it in HTML, JavaScript, or a public Git repository.

## 2. Set up Python
```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the real values:
- `FLASK_SECRET_KEY`: long random secret
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `WHATSAPP_NUMBER`: digits only, include country code
- `PHONE_DISPLAY`: verified business phone
- `SITE_URL`: preview / production URL

## 3. Run locally
```bash
python app.py
```
Open http://127.0.0.1:5000

If Supabase is not configured, pages render but form submissions are not persisted. Configure Supabase before testing lead capture.

## 4. Deploy
Use a Python web host with:
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`
- Add all `.env` values as platform environment variables.
- Use a private / password-protected preview until approved.
- Do not commit `.env`.

## 5. Included routes
- `/`
- `/products`
- `/<product-slug>` for product detail pages
- `/ply-finder`
- `/professionals`
- `/become-a-dealer`
- `/about`
- `/cities/<city-slug>` (e.g. `/cities/pune`)
- `/resources`
- `/contact`
- `/quote` (POST)
- `/thank-you/quote`
- `/thank-you/dealer`
- `/sitemap.xml`
- `/robots.txt`
- `/health`

## 6. Production checklist
- Add real Kohinoor logo, approved brand palette and photography.
- Confirm product descriptions, grade names, standards, warranty and technical documents.
- Confirm address, phone, timings, WhatsApp number and map.
- Add founder-approved product data and stock / availability workflow.
- Add private admin lead dashboard or connect leads to the approved CRM / Google Sheet / email workflow.
- Configure GA4 via GTM and Meta Pixel only with approved IDs and consent approach. `main.js` pushes `whatsapp_click`, `phone_click`, and `lead_form_submit` into `dataLayer`; install GTM and map the events.
- Add canonical URLs, page-specific Open Graph images, Product / FAQ / Breadcrumb schema, and static/server-rendered city content.
- Test at 360px, 390px, tablet and desktop.
- Run Lighthouse on home and a product detail page. The PDF targets mobile PageSpeed 90+, SEO 95+, accessibility 95+, LCP <2.5s, CLS <0.1, INP <200ms. These are targets, not guaranteed results.
- Add rate limiting, CSRF protection, spam protection / CAPTCHA and server-side phone validation before production.
- Verify lead submission, Supabase RLS and access permissions.

## 7. Content and data notes
The first version stores leads and dealer applications in Supabase. Product display data is currently in `app.py` for easy initial editing. Move it into the `products` table or a structured JSON file after the approved catalogue is supplied.

## Admin dashboard

The admin area is available at `/admin/login`. It currently provides:
- A dashboard with enquiry/dealer-application totals and recent submissions.
- Enquiry and dealer-application inboxes.
- Status updates (New, Contacted, In Progress, Completed, Rejected).
- CSV export for both inboxes.

### Configure admin access

1. For your already-hosted website, run **`admin_migration.sql`** in the Supabase SQL Editor. It adds status fields without deleting existing records. (The full `schema.sql` is for a fresh database.)
2. Generate a password hash locally:

   ```bash
   python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('Choose-A-Long-Unique-Password'))"
   ```

3. Add these environment variables in your hosting provider's dashboard (do not commit them to Git):

   ```env
   ADMIN_USERNAME=your-admin-username
   ADMIN_PASSWORD_HASH=paste_the_generated_hash
   COOKIE_SECURE=true
   FLASK_SECRET_KEY=a_long_random_secret_value
   ```

4. Redeploy the app and visit `https://YOUR-DOMAIN/admin/login`.

For local HTTP development, set `COOKIE_SECURE=false`; use `true` on your HTTPS hosted site. Keep `SUPABASE_SERVICE_ROLE_KEY` server-side only. Admin access is authenticated by the Flask server and the browser never receives the Supabase service-role key.

This first admin release manages incoming enquiries and dealer applications. Product catalogue/content editing is not included yet; the public catalogue is currently defined in `PRODUCTS` inside `app.py`.


## Full admin panel on Vercel

This project exports the Flask `app` from the root `app.py`, which Vercel detects as a Python Flask application. Static assets are copied to `public/` for Vercel's static asset serving. Use Vercel's Git integration to deploy from the repository.

### 1. Apply the Supabase migration

Open **Supabase → SQL Editor**, paste and run `admin_full_migration.sql`. It adds product-management fields, creates the editable `site_content` table, adds enquiry/dealer status fields, and seeds the initial catalogue and content only when those records do not already exist. It does not delete existing enquiries or dealer applications.

### 2. Add Vercel environment variables

In **Vercel → Project → Settings → Environment Variables**, add these for Production (and Preview if you want admin access in previews):

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY` (server-side only; never use a `NEXT_PUBLIC_` prefix)
- `FLASK_SECRET_KEY` (long random secret; do not reuse the sample)
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD_HASH`
- `COOKIE_SECURE=true`
- `SITE_URL` (your production URL)
- `WHATSAPP_NUMBER` and `PHONE_DISPLAY`

Generate an admin password hash locally after installing requirements:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('Use-A-Strong-Unique-Password'))"
```

Paste the resulting hash into `ADMIN_PASSWORD_HASH`. Do not put the plain password in Vercel variables or source code. Generate `FLASK_SECRET_KEY` with `python -c "import secrets; print(secrets.token_urlsafe(48))"`.

### 3. Deploy

Commit and push the updated project to the Git repository connected to Vercel. Vercel should detect Flask automatically from `app.py` and `requirements.txt`; no custom build command or output directory is required. After deployment, open `/admin/login` on your production domain.

### Admin capabilities

- Dashboard overview
- Customer enquiry inbox with status updates and CSV export
- Dealer application inbox with status updates and CSV export
- Product create/edit/delete and publish/draft controls
- Editable homepage hero, homepage introduction, about introduction and footer copy

### Vercel notes

Vercel Functions have a read-only deployment filesystem (apart from temporary `/tmp` storage). This app stores persistent business records in Supabase, not local files. Keep all Supabase service-role credentials server-side. Vercel's function duration and request-size limits apply.
