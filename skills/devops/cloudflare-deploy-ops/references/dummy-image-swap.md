# Dummy image swap + live verification

Pattern for removing a real image (personal photo, logo) from a deployed Cloudflare
Next.js site and replacing it with a neutral placeholder, then proving the swap is
actually live.

## 1. Generate the placeholder with PIL (no external file needed)
Keep the SAME filename so no code references change.

```python
from PIL import Image, ImageDraw
W = H = 400
img = Image.new("RGB", (W, H), (230, 232, 236))   # light gray bg
d = ImageDraw.Draw(img)
cx, cy = W // 2, 150
d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(150, 156, 168))   # head
d.ellipse([cx - 130, H - 40, cx + 130, H + 160], fill=(150, 156, 168))  # body
d.rectangle([0, 0, W - 1, H - 1], outline=(200, 203, 209), width=4)      # border
img.save("public/<name>.jpeg", "JPEG", quality=90)
```

Verify locally: `python -c "from PIL import Image; print(Image.open('public/<name>.jpeg').size)"`
→ expect `(400, 400)`.

## 2. Find ALL references BEFORE changing anything
OpenGraph / JSON-LD `image` schema blocks often hardcode the absolute live URL
(e.g. `https://app.sproutern.com/premkumar.jpeg`), and `<img src="/premkumar.jpeg">`
appears in multiple pages (`about/page.tsx`, `founder/page.tsx`, …). Keeping the
filename identical means you touch NONE of them. Grep to confirm scope:
```bash
grep -rinE "premkumar\.jpeg|<img|image:" src public --include=*.tsx --include=*.ts
```

## 3. Full rebuild + redeploy
A public-asset change still requires a GREEN full build (see the OOM pitfall) — you
cannot ship it while `.open-next/.build/durable-objects/*.js` are missing. After a
clean build, redeploy the public worker and wait for `Uploaded N of N assets` +
`Deployed sproutern triggers`.

## 4. Verify the LIVE image changed (don't trust the build)
```bash
curl -s -o /tmp/live.jpg "https://app.sproutern.com/<name>.jpeg"
python -c "from PIL import Image; im=Image.open('/tmp/live.jpg'); print(im.size, im.mode)"
# assert size == (400, 400)  =>  DUMMY PLACEHOLDER is live (original photo gone)
```
Check BOTH the custom domain and `*.workers.dev` if both serve the site. The
dimension assertion is the real proof — a 200 status alone only proves an image
is served, not WHICH one.
