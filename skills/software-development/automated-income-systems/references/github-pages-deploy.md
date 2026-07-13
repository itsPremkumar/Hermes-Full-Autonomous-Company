# GitHub Pages deployment (zero-cost hosting)

## The single most common break
GitHub Pages does NOT serve an arbitrary output folder like `public/`. It
serves ONLY:
- the branch root, OR
- a `/docs` folder at the branch root.

If your static-site generator writes to `public/`, the live site becomes
`https://USER.github.io/repo/public/index.html` and every internal link
(`index.html`, `tools.html`, `gumroad.html`) 404s because they assume the
site root. Same for product download links pointing at `products/...` that
only exist under `gumroad/products/` in the source tree.

## Correct setup
1. Generator writes everything to `docs/` (root-relative links: `index.html`,
   `tools.html`, `gumroad.html`, `products/<slug>/PRODUCT.md`).
2. `.gitignore` should ignore the built `docs/` (treat it as a build artifact),
   or commit it — either works since Pages reads the branch.
3. Repo -> Settings -> Pages -> Source: "Deploy from a branch" ->
   Branch: `main` -> Folder: `/docs` -> Save.
4. Live at `https://USER.github.io/money-engine/`.

## Gotchas
- Cross-page links must be ROOT-relative, not parent-relative (`../index.html`
  is wrong when everything sits at the site root). Fix `../` -> ``.
- Copy generated products into `docs/products/<slug>/` during the build so their
  `products/.../PRODUCT.md` download links resolve.
- First publish can take 1-2 min; wait, don't assume it failed.
- Custom domains are optional and free; not required.

## Enabling Pages via REST API (no browser)
With a GitHub PAT (from `git credential fill` or `gh`):
```bash
# Enable: source MUST be an object, not a string
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  -d '{"source":{"branch":"main","path":"/docs"}}' \
  https://api.github.com/repos/OWNER/REPO/pages
# 201/409 = enabled (409 means already on); 422 "Invalid property /source" = you passed a string
# Confirm + read served branch:
curl -s -H "Authorization: Bearer $TOKEN" https://api.github.com/repos/OWNER/REPO/pages \
  | python -c "import sys,json;d=json.load(sys.stdin);print('status:',d['status'],'| branch:',d['source']['branch'])"
```

## Branch-sync trap (silent, easy to ship)
A fresh `git init` defaults to branch `master`, but Pages is usually set to serve
`main`. If you generate content on `master` and only ever pushed `HEAD:main` once,
the live site freezes at that first commit while local keeps growing.
- **Symptom:** live article count < local `content/*.md` count.
- **Fix:** after the final generation, `git push origin master:main` (non-force).
  Never run `--force` without explicit user consent (it's an irreversible,
  blocked-by-harness action).
- Verify live count: `curl -s <site> | grep -oE 'href="[a-z0-9-]+\.html"' | grep -vE 'index|tools|gumroad|disclosure' | sort -u | wc -l`
