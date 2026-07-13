# Affiliate token pattern (auto-income-system)

Content files carry placeholder tokens; `build.py::expand_affiliate` swaps them
from `config.json`. This keeps content stream-agnostic and lets the user drop
in their own IDs with zero content edits.

## Tokens (regex in build.py)
- `{{AMAZON:Keyword}}`  -> `https://www.amazon.com/s?k=<urlencoded kw>[&tag=<amazon_tag>]`
- `{{FIVERR:category}}` -> `https://www.fiverr.com/categories/<cat>[?source=affiliate_fiverr&aff_id=<fiverr_aff_id>]`
- `{{SHAREASALE:id:keyword}}` -> `https://www.shareasale.com/r.cfm?b=<id>[&u=<shareasale_id>&m=featured]`

## Empty-tag fallback (CRITICAL)
When the config field is `""`, emit the **plain link with NO affiliate param**.
Never append a stray `&tag=` or leave a `YOURTAG` placeholder in a path that
gets published. The placeholder `YOURTAG` is acceptable ONLY inside static
HTML (tools.html) where it's a visible TODO, never in a generated href.

## Generator-side gotcha: f-string brace doubling
A generator that builds content with `f"""…"` and must EMIT a literal
`{{FIVERR:cat}}` must write `{{{{FIVERR:{cat}}}}}` — f-strings reduce
`{{`->`{`, so four braces yield the two needed. Writing `{{FIVERR:{cat}}}`
yields a SINGLE-brace `{FIVERR:cat}` that `expand_affiliate` never matches.
CHECK: after generating, `grep -o 'FIVERR[^)]*' content/*.md` must show a
DOUBLE brace. If single — the token is dead and the link won't earn.

## Verify expansion
Set `"amazon_tag":"premkuma-20"`, rebuild, grep rendered html for
`tag=premkuma-20`. Then reset the field to `""`. Same for fiverr_aff_id.
