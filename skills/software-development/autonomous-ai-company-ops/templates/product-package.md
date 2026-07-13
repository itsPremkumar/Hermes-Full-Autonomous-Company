# Gumroad product package skeleton

Create `income-engine/gumroad/products/<product-id>/` with two files:

## PRODUCT.md (the deliverable the buyer downloads)
```
# <Product Title>
**Product ID:** <id>
**Price:** $<n>
**Category:** <category>

## What buyers get
- <file or asset list>

## Who it's for
<audience>

## The problem it solves
<one honest paragraph — NO income guarantees, no hype (Charter S0.3)>
```

## LISTING.txt (copy-paste into Gumroad's product form)
```
TITLE:       <Product Title>
PRICE:       $<n>
CATEGORY:    <Gumroad category>
FILE:        upload PRODUCT.md as "Software / File"

DESCRIPTION (copy below the line):
------------------------------------------------------------------------
<honest 3-5 sentence description; mention what it does and who it's for;
 state it saves time on a real task — not that it makes money by itself>
------------------------------------------------------------------------

PUBLISH STEPS:
1. Gumroad > Products > New product
2. Name = TITLE; Price = $n; Category = above
3. Add file: upload PRODUCT.md (access = "Software / File")
4. Paste DESCRIPTION
5. Publish  (HUMAN-ONLY step — agent never clicks Publish)
```

## Then
- Add the product to `digital-products/product-catalog.json` (update total + stats).
- The agent may NOT publish — that is the principal's action (PRE-52, Charter S0).
