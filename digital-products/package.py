import zipfile, os

base = r'C:\one\paperclip-company\digital-products'
dist = os.path.join(base, 'dist')
os.makedirs(dist, exist_ok=True)

products = {
    'prem-50-viral-scripts.zip': ['product-1-video-scripts'],
    'prem-agent-playbook.zip': ['product-2-playbook'],
    'prem-remotion-templates.zip': ['product-3-remotion-templates'],
    'prem-monetization-kit.zip': ['product-4-monetization-kit'],
    'prem-cold-outreach.zip': ['product-5-outreach'],
    'prem-job-board-guide.zip': ['product-6-job-board'],
    'prem-pricing-templates.zip': ['product-7-pricing-templates'],
    'prem-30-day-launch.zip': ['product-8-launch-plan'],
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
    print(f"  {zip_name:35s} {os.path.getsize(zpath)/1024:6.1f} KB")

bundle_path = os.path.join(dist, 'prem-all-products-bundle.zip')
with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in ['product-catalog.json', 'store.html']:
        zf.write(os.path.join(base, f), f)
    for d in sorted(os.listdir(base)):
        dpath = os.path.join(base, d)
        if os.path.isdir(dpath) and d.startswith('product-'):
            for root, _, files in os.walk(dpath):
                for f in files:
                    fpath = os.path.join(root, f)
                    arcname = os.path.relpath(fpath, base)
                    zf.write(fpath, arcname)

print(f"\n  {'prem-all-products-bundle.zip':35s} {os.path.getsize(bundle_path)/1024:6.1f} KB")
print(f"\nDone! Products packaged in: {dist}")
