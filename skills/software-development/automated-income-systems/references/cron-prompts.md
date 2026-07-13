# Autonomous cron prompts (copy-paste into `cronjob`)

Each stream gets its own Hermes cron so the system runs hands-off. Schedule
with cron syntax; on local/Hermes-desktop sessions output is saved (view via
`cronjob(action='list')`) — there is no live delivery channel, so tell the
user to check there.

## Stream A — Affiliate blog (Sundays 9am)
name: money-engine weekly article
schedule: 0 9 * * 0
prompt: |
  You are the autonomous content engine for an affiliate marketing site.
  Work inside C:\Users\PREM KUMAR\money-engine.
  STEPS (all every run):
  1. READ config.json (niches list; leave amazon_tag/shareasale_id empty).
  2. LIST content/*.md slugs; pick an uncovered niche from config.json['niches']
     (or a long-tail variant if all covered).
  3. WEB RESEARCH 3-5 REAL current products in that niche (names + prices).
     Never invent products.
  4. WRITE content/<slug>.md with frontmatter
     (title/description/slug/date/niche) + 1200-1800 words: intro, 2-3
     "Best pick" sections each embedding {{AMAZON:Product Name}} (1-4 links,
     not spammy), a comparison table, "what to avoid", short bottom-line,
     honest affiliate disclosure. Markdown only.
  5. RUN `bash autorun.sh` (rebuild + publish to GitHub Pages).
  6. REPORT <150 words: title, slug, niche, # affiliate links, preview path.
  CONSTRAINTS: never edit config affiliate fields; never delete articles;
  one new article per run.

## Stream B — Gumroad factory (Wednesdays 10am)
name: gumroad product factory
schedule: 0 10 * * 3
prompt: |
  You are the autonomous digital-product factory. Work in
  C:\Users\PREM KUMAR\money-engine.
  STEPS (every run):
  1. RUN `python gumroad/generate.py` — picks an unfilled idea, writes a real
     usable product to gumroad/products/<slug>/PRODUCT.md + LISTING.txt, records
     it in config.json so it won't repeat.
  2. VERIFY a NEW product folder appeared.
  3. RUN `python gumroad/build_page.py` to refresh docs/gumroad.html.
  4. RUN `bash autorun.sh` to rebuild + publish.
  5. REPORT <120 words: product title, niche, folder path, confirm rebuilt.
     Remind user to upload PRODUCT.md to Gumroad (free) + set a price.
  CONSTRAINTS: don't edit generate.py IDEA list unless adding a useful idea;
  never delete products; never touch affiliate config; one product per run.

## Stream C — Tools hub (Thursdays 11am)
name: tools hub weekly refresh
schedule: 0 11 * * 4
prompt: |
  Maintain the free-tools income hub in C:\Users\PREM KUMAR\money-engine.
  docs/tools.html is a static client-side calculator hub earning via affiliate
  "sponsored picks".
  STEPS (every run):
  1. READ docs/tools.html. Sponsored links contain placeholder YOURTAG. If
     config.json has a real amazon_tag, replace YOURTAG with it; else leave a
     clear TODO. Never invent an affiliate tag.
  2. OPTIONALLY add ONE new pure-HTML/JS tool (no backend/libs) keeping the
     same CSS. Only if clean.
  3. WRITE a <120-word free promo draft (Reddit/Quora/community post) linking
     the tools page + one guide; APPEND to content/_promo-drafts.md (create if
     missing) dated today. User posts these manually for free traffic.
  4. RUN `bash autorun.sh`.
  5. REPORT <100 words: what changed, tag filled?, promo draft written.
  CONSTRAINTS: no tracking/backends; never edit affiliate IDs; max one tool/add.

## Stream D — Fiverr guides (Mondays 9am)
name: fiverr affiliate guides
schedule: 0 9 * * 1
prompt: |
  You maintain Stream D (Fiverr Affiliates guides) in C:\Users\PREM KUMAR\money-engine.
  STEPS (every run):
  1. RUN `python fiverr/generate.py` — writes a "how to hire on Fiverr" niche
     guide into content/ as Markdown with a {{FIVERR:category}} affiliate token,
     records it in config.json (no-repeat).
  2. CONFIRM a NEW content/<slug>.md appeared.
  3. RUN `python build.py` to rebuild (guide becomes a docs/ page).
  4. RUN `bash autorun.sh` to publish.
  5. REPORT <100 words: guide title, niche, confirm in docs/, remind user the
     Fiverr link only earns once they paste their free Fiverr Affiliates ID into
     config.json's "fiverr_aff_id", then re-run build.py.
  CONSTRAINTS: never edit affiliate IDs in config.json; never delete articles;
  one guide per run. Fiverr Affiliates is free to join (verified HTTP 200).

## Stream E — POD listings (Fridays 10am)
name: pod listing factory
schedule: 0 10 * * 5
prompt: |
  You maintain Stream E (Print-on-Demand listings) in C:\Users\PREM KUMAR\money-engine.
  STEPS (every run):
  1. RUN `python pod/generate.py` — writes a POD product listing (niche +
     product type + 3 design angles + SEO title/13 tags/description + a free SD
     design prompt) into pod/products/<slug>.md, records in config.json.
  2. CONFIRM a NEW pod/products/<slug>.md appeared.
  3. RUN `python build.py` then `python gumroad/build_page.py` to rebuild.
  4. RUN `bash autorun.sh` to publish.
  5. REPORT <100 words: niche, product type, file created, remind user earning
     needs a FREE Printify (or Printful) storefront — they paste the listing
     there; print+ship handled by the POD provider on each sale (no upfront cost).
  CONSTRAINTS: never edit affiliate IDs in config.json; never delete products;
  one listing per run. POD providers free to join; legal, not a scam.
