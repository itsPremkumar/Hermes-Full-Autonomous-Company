# Digital Product Catalog Template
## For packaging AI-agent artifacts into sellable products

### Product Line Structure
Each product follows this template. Create one `product-N-name/` directory per product.

```
digital-products/
├── product-catalog.json           # Master catalog (prices, IDs, metadata)
├── store.html                     # Store landing page (GitHub Pages)
├── package.py                     # ZIP packager (run before listing)
├── dist/                          # Output ZIPs (gitignored)
├── product-1-video-scripts/
│   ├── README.md                  # Product description + listing copy
│   └── scripts-all.md             # Actual deliverable content
└── product-2-playbook/
    ├── README.md
    └── ...
```

### Catalog JSON Schema
```json
{
  "store": {
    "name": "Company Name — Digital Products",
    "tagline": "Tagline",
    "platform": "Gumroad",
    "currency": "USD",
    "worldwide_shipping": true,
    "instant_delivery": true
  },
  "products": [
    {
      "id": "prem-50-viral-scripts",
      "title": "50 Viral Short-Form Video Scripts",
      "tagline": "Done-for-You YouTube Shorts / Reels / TikTok Scripts",
      "price_usd": 12,
      "category": "Content / Templates",
      "file_formats": ["PDF", "Markdown", "CSV", "JSON"],
      "status": "ready",
      "product_dir": "product-1-video-scripts"
    }
  ],
  "pricing_summary": {
    "lowest_price": 9,
    "highest_price": 29,
    "median_price": 17,
    "bundle_price": 99,
    "bundle_savings_percent": 40,
    "total_if_bought_separately": 144
  }
}
```

### ZIP Packager (Python, run before listing)
```python
import zipfile, os

dist = os.path.join(base, 'dist')
os.makedirs(dist, exist_ok=True)

# Map zip names to source directories
products = {
    'product-name.zip': ['product-1-name'],
}

for zip_name, dirs in products.items():
    zpath = os.path.join(dist, zip_name)
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as zf:
        for d in dirs:
            dpath = os.path.join(base, d)
            for root, _, files in os.walk(dpath):
                for f in files:
                    fpath = os.path.join(root, f)
                    arcname = os.path.relpath(fpath, base)
                    zf.write(fpath, arcname)

# Also create a master bundle
bundle_path = os.path.join(dist, 'all-products-bundle.zip')
with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(os.path.join(base, 'product-catalog.json'), 'product-catalog.json')
    zf.write(os.path.join(base, 'store.html'), 'store.html')
    for d in sorted(os.listdir(base)):
        dpath = os.path.join(base, d)
        if os.path.isdir(dpath) and d.startswith('product-'):
            for root, _, files in os.walk(dpath):
                for f in files:
                    fpath = os.path.join(root, f)
                    arcname = os.path.relpath(fpath, base)
                    zf.write(fpath, arcname)
```

### Store Page HTML Structure
- Dark theme (`#0b0f17` bg, `#121826` panel, `#5b9dff` accent)
- Stats bar (product count, price range, categories)
- Product grid (cards with price badge, title, tagline, format badges)
- Bundle CTA section (prominent, shows savings)
- Link to Gumroad / Ko-fi for checkout

### Pricing Guidelines
| Product Tier | Price | Positioning |
|---|---|---|
| Micro (script pack, guide) | $9–$12 | Lowest friction, high volume |
| Standard (template pack, tool) | $15–$19 | Core products |
| Premium (playbook, kit) | $29 | Most value, proof-driven |
| Bundle (all products) | $99 | 35–40% discount vs separate |
