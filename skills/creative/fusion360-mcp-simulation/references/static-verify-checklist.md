# Static Engineering Verification — checklist & worked reference

For verifying a Fusion 360 CAD payload (e.g. `optimus_vN.py`) WITHOUT running
Fusion. Pure static code+math review. Lead with independent recomputation; never
just echo the script's own logged numbers.

## Unit conversions & formulas (verify the code uses these exactly)
- kgf·cm torque needed to hold a static load:
  `need = mass_kg * 9.81 * (lever_cm/100) / 0.0981` → **simplifies to `mass_kg * lever_cm`**.
- kgf·cm → N·mm bending moment: **`M = torque_kgcm * 98.0665`** (one 98.0665 only).
  A `* 98.0665 * 10.0` is a ×10 bug that inflates stress 10×.
- Rectangular cantilever bending stress: `sigma = M·c / I`, where
  `I = w·t³/12` (w, t in mm), `c = t/2`. SF = `yield_MPa / sigma`.
  Printed-PLA/PETG yield is de-rated vs bulk (PETG ~18, ABS ~14, PLA ~20 MPa
  in the v17 file) to account for FDM layer anisotropy.
- Safety-factor pass line is usually `MIN_SAFETY_FACTOR = 2.5` for dynamically
  loaded biped joints. Joint torque margin pass line is usually **1.5×** even when
  the code's own MARGINAL cutoff is looser (0.9×) — apply 1.5× per the request.

## Recompute locally (terminal `python <path>`, not execute_code)
```python
def torque_kgcm(mass_kg, lever_cm): return mass_kg * lever_cm
def bracket_sf(torque_kgcm, w_cm, t_cm, yield_mpa=18.0):
    M = torque_kgcm * 98.0665                 # NOT *10
    I = (w_cm*10.0)*(t_cm*10.0)**3/12.0
    c = (t_cm*10.0)/2.0
    return yield_mpa / (M*c/I)
```
Build the URDF `link_mass` dict sum as an independent mass proxy when CAD masses
(`comp.physicalProperties.mass`) are unverified.

## v17 (optimus_v17.py) bug inventory — concrete reference
Surfaced in a real review; reuse as a pattern-recognition checklist.
- **L748** `M_Nmm = torque_kgcm * 98.0665 * 10.0` → stray ×10. Even corrected,
  hip/waist/knee brackets SF = 0.96 / 1.44 / 2.07 (< 2.5) → FAIL; 0.45 cm
  (4.5 mm) printed plates too thin.
- **L1066 `assign_material()`** resolves via `get_material()` against the Fusion
  **cloud library**; offline → `None` for every part → Fusion default (≈steel)
  density → all mass/torque/structural numbers invalid. Assert `no_material_count==0`.
- **L3497–3584** Hip Yaw×2 + Hip Pitch×2 BOM'd as DS3225MG but built by `mg996r()`
  (MG996R-sized pockets) → size/geometry mismatch.
- **L4658 `estimate_servo_loads()`** hand-typed masses, `MARGINAL` at ≥0.9× (L4688);
  optimistic ~3× vs the real-mass check. Disagrees with `estimate_real_joint_torques()`
  (~2× on hip). Real-mass margins: hip 1.21×, knee 1.05×, waist 1.35× — all <1.5×.
- **L253 JOINT_LIMITS**: ankle yaw 95° (self-collide), hip yaw ±95° (anatomical
  absurd), ankle pitch ±20° (unwalkable).
- **L61/70** `CLEARANCE=0.06 cm` (0.6 mm, tight); `BEARING_FIT_TOLERANCE=0.008`.
  **L73–74,189** sub-mm features (tendon/wire Ø 0.4 mm, circlip groove 0.7 mm)
  won't print on FDM.
- **L2453/5175** power claims ~10 A peak; real ~20 A (26 servos × ~1 A). Servo
  rail fused 5 A (blows). Bay built for 2S 1300 mAh (L208) but recommends 3S 5000
  mAh (won't fit). Runtime ~4–5 min, not >20 min.
- **L5140–5166** wiring map: 34 channels referenced vs 27 built; PCA9685 max 16 ch.

## Report structure that worked
(a) joint-by-joint torque margin table with PASS/MARGINAL/FAIL verdict;
(b) total mass estimate + CoM/stability assessment;
(c) prioritized top 8–10 improvements, each citing the exact file + line(s) to change.
Be quantitative; cite line numbers.
