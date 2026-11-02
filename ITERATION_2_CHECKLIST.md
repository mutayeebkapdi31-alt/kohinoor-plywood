# Kohinoor Plywood Iteration 2 — Submission checklist (working status)

This checklist is intentionally honest: items not verified against a running deployment are marked No / Pending.

| No. | Task | Done? | Notes |
|---:|---|---|---|
| 1 | Notes on Greenply and CenturyPly shared before building | Yes | Reference notes included in the accompanying implementation summary; based on public product navigation, grade organization, application guidance, specs/FAQs and trust presentation. |
| 2 | No mention of “brief”, “SynexAI”, placeholders or “pending verification” anywhere on site | Partial | Removed the public Our Story references from the supplied templates. Full repository/deployment audit still required. |
| 3 | Fake phone/WhatsApp numbers removed or hidden; logo slot ready | Partial | Placeholder phone defaults now blank and phone/WhatsApp footer/product links are conditional. Existing logo mark is still a temporary slot; real SVG awaited. |
| 4 | Broken “3 trusted by generations” stat fixed or removed | Yes | Removed the unsupported statistic from homepage. |
| 5 | No asterisks or disclaimer notes anywhere | Partial | Removed the public quality disclaimer/asterisk notes in Our Story and product detail. Site-wide form/admin content audit remains. |
| 6 | New fonts live and self-hosted; Playfair and DM Sans removed; no text under 12px | No | Font CSS references changed, but licensed/local WOFF2 assets are not included. Must supply/install font files and audit small labels. |
| 7 | New full-bleed hero with material imagery or video | Partial | Full viewport hero layout, material-led background and layered 3D motif implemented. Hero imagery is still externally hosted and needs approved plywood macro photo. |
| 8 | Opening animation live: under 2 sec, first visit only, skippable, off for reduced motion | Partial | CSS/SVG intro, session-only, scroll/click skip, reduced-motion bypass added. Needs browser/device QA. |
| 9 | Italic gold headings, section labels and 01/02 numbering reduced | Partial | Global typographic overrides added; all templates still need manual editorial review. |
| 10 | New colour tokens applied site-wide | Partial | Iteration 2 tokens and overrides appended to both CSS copies; comprehensive page QA pending. |
| 11 | Every image replaced, self-hosted, WebP, used once, descriptive alt text | No | Image inventory and replacement/self-hosting remain. |
| 12 | Grouped product pages split; all products under /products/ with redirects | No | Requires product taxonomy/content confirmation and routing migration. |
| 13 | Every product page has 500+ words, spec table, FAQs and related products | No | Existing product pages remain abbreviated; product facts/docs need confirmation. |
| 14 | Every page has unique title, description, H1 and share image | No | Site-wide metadata/OG audit and per-product assets remain. |
| 15 | Product, FAQ, Breadcrumb and LocalBusiness schema pass Rich Results Test | No | Structured data implementation and external validation remain. |
| 16 | sitemap.xml and robots.txt live | No | Not verified or added. |
| 17 | Four Insights articles published | No | Not created. |
| 18 | Quote form tested end to end; leads arrive | No | Requires deployed Supabase/email/sheet destinations and test submissions. |
| 19 | Lighthouse mobile ≥90 Performance, Accessibility, SEO | No | Not run; requires deployed build and optimization. |
| 20 | Checked on real Android and iPhone | No | Device testing remains. |
| 21 | Screen recording of hero + one product page sent for approval | No | Recording/approval is a client-facing step after QA. |

## Approval gate
The hero and one representative product page should be reviewed before applying the full rollout. Confirm official logo, real contact information, product grades/specifications, certifications, warranty terms, address/hours, approved imagery and font assets before launch.
