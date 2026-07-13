# Fusion 360 MCP Python Script Debugging — condensed notes

Distilled from auditing a 5300-line Fusion 360 MCP script (`optimus_v17.py`) that
builds a 3D-printable humanoid robot and simulates 9+ kinematic modules. The script
runs *inside* Fusion 360 via the MCP server (`http://127.0.0.1:27182/mcp`), so it
cannot be executed or unit-tested outside Fusion. Verification is static + log-based.

## Environment realities
- **No canonical test/lint/build.** The only entry point is
  `python src/run_simulation.py --module ALL --capture` which drives Fusion. A full
  ALL run with interference analysis on a 6 GB laptop takes **30–60+ min** and the
  interference phase looks frozen (log not written for minutes) but is alive.
- Launch with `terminal(background=True, notify_on_complete=True)`; poll the log file
  (`output/logs/optimus_v17_*.txt`) — never block waiting.
- To stop: there is **no `--stop` CLI flag**. Create `output/stop.flag`
  (`touch output/stop.flag`, or PowerShell `New-Item -Path output\stop.flag -ItemType File -Force`).
  The engine polls for it each frame. (Many stale READMEs tell users `--stop` — that's
  a doc bug, not a feature.)

## The no-op collision pattern (key tell)
`analyzeInterference` on the *entire* assembly returns the model's permanent resting
contacts (~14,800 touching face pairs) every call. If a "Joint ROM" module logs the
**same 5 static body pairs** for *every* joint and *every* angle, the collision check
is **non-functional** — it never isolated the moving joint. Fix: capture a neutral
baseline collision set once, then report only NEW pairs (`pairs - baseline`). Or make
the sweep function actually move the joint and measure delta.

## Material / mass gotcha (corrupts all physics)
`assign_material()` resolves against the **Fusion cloud material library**. Offline it
returns `None` → every part falls back to Fusion's default density (often steel,
~7.85 g/cm³) → every mass/torque/structural number is 5–8× wrong. Fix: assign an
explicit known density via a **custom material** (`design.materials.addCustomMaterial`,
whose `.physicalProperties.density` IS writable) keyed by role (PETG 1.24, ABS 1.04,
TPU 1.15, steel 7.85 g/cm³). The mass report logs a WARN when this happens — treat it
as a hard blocker for any physics claim.

## Physics caveats worth checking
- `StructuralValidator.check_bracket`: `M_Nmm = torque_kgcm * 98.0665` converts
  kgf·cm→N·mm. A stray extra `* 10.0` inflates stress 10× (false FAILs). Watch units.
- Servo torque margins: use 1.5× rule. Hip/knee at MG996R (9.4 kg·cm) are marginal for a
  ~4.5 kg humanoid — the geometry pockets must fit whatever servo the BOM claims (a
  DS3225 won't fit an MG996R-sized pocket). Don't silently up-rate the BOM.
- Ankle carries full body weight in single-support; validate it (often missing).
- Power: 28+ servos realistically draw ~20 A peak, not 10 A. Size fuses/battery to real
  draw; a 3S pack won't fit a 2S bay without enlarging it.
- Sub-mm features (tendon/spring wires <0.8 mm, retaining-ring grooves <0.7 mm) won't
  print on FDM — raise to printable minimums.

## Visual verification without a live viewport
Fusion's viewport can't be screenshotted from the terminal. Inspect the PNGs the script
writes (`output/screenshots/`, `images/`) with `vision_analyze`. Note: old renders may
be uniform gray even when the code applies colors — confirm via the log
(`Final colors: N applied, 0 skipped`) rather than assuming a color bug.
