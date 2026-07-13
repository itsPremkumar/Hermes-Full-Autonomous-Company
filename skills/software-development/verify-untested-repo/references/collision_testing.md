# Collision / self-interference testing in assembled-model simulators

Recurring bug pattern seen in CAD/simulation rigs (Fusion 360 `analyzeInterference`,
URDF self-collision, etc.): a "ROM / collision sweep" function that calls the
interference check on the **entire assembled model every time**, instead of isolating
the joint under test. Result: it always reports the model's permanent resting contacts
(thousands of touching-face pairs between adjacent bodies) and can NEVER detect a
joint-limit self-collision. Looks like it "works" (big collision counts) but is noise.

## How to detect it
- In the run log, the SAME handful of body pairs (e.g. `Body1 <-> Body4..8`) appear for
  EVERY joint and EVERY angle, with a near-identical count. That's the tell.
- The function that "runs the sweep" is a no-op stub: it only logs "running for X" and
  moves nothing.

## The fix (delta vs baseline)
1. Before sweeping, capture a **neutral-pose baseline** = set of all interfering body
   pairs at rest.
2. After moving a joint to a limit, re-run interference and report only pairs that are
   **NEW** vs the baseline (`new_pairs = pairs - baseline`).
3. A `0` delta = no self-collision at that pose; `>0` = real self-collision introduced.
4. Make the sweep function actually step the joint (e.g. 12 steps from neutral to each
   limit) and record the first angle where a NEW collision appears — that IS the true
   mechanical ROM limit.

## Unit-conversion trap (separate but adjacent)
`kgf·cm -> N·mm` = `× 98.0665` (9.80665 N/kgf × 10 mm/cm, already combined). A literal
`* 98.0665 * 10.0` double-counts and inflates bending stress 10×, causing false
structural FAILs. The factor 98.0665 already includes the ×10.

## Offline material fallback trap
If mass comes from `physicalProperties.mass` but material assignment falls back to a
cloud library that's unavailable offline, Fusion substitutes its DEFAULT density
(often steel ~7.85 g/cm³) — making a PETG robot read ~5-8× too heavy and invalidating
every torque/CoM/structural number. Assign an explicit known density (custom material)
so mass is real even offline; assert `no_material_count == 0` before trusting the report.
