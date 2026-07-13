---
name: fusion360-mcp-simulation
description: Drive Autodesk Fusion 360 via its MCP server to programmatically build, simulate, and export parametric CAD / robot models. Also covers STATIC code+math engineering verification of a payload WITHOUT running Fusion (no MCP needed) — servo torque margins, mass/COM/stability, structural safety factors, 3D-printability, power budget. Use when a project sends Python payloads to Fusion 360 over MCP (e.g. a run_simulation.py controller + versioned optimus_*.py / model_*.py payloads), when asked to "run the vN simulation", to "analyze which version is best", or to "review/verify the engineering" of a CAD script.
---

# Fusion 360 MCP Simulation

Projects in this class build a 3D-printable / articulated model **inside** Autodesk
Fusion 360 by sending a large Python payload script to Fusion's built-in **MCP
server** over JSON-RPC. A thin host controller (`run_simulation.py`) loads the
payload, injects config, and POSTs it; the payload runs with full `adsk.core` /
`adsk.fusion` API access and writes logs/exports/screenshots to `output/`.

## Architecture (recognize it fast)
- **MCP endpoint**: `http://127.0.0.1:27182/mcp` (JSON-RPC 2.0 over HTTP POST).
  Override via `--mcp-url` or `$MCP_URL`.
- **Controller** (`src/run_simulation.py`): finds/launches Fusion, waits for MCP,
  closes docs, reads `PAYLOAD_FILE`, prepends config (`TARGET_MODULE`,
  `EXPORT_STL/STEP/URDF`, `CAPTURE_SCREENSHOTS`, dir overrides), calls the
  `fusion_mcp_execute` tool. Escapes dialogs and retries on "dialog blocking".
- **Payload** (`src/optimus_vN.py` etc.): the whole engine — geometry builders,
  joint/kinematics setup, N simulation modules, and STL/STEP/URDF/f3d exporters.
  Config is read via `globals().get(...)` so the controller can inject it.
- **Output**: `output/logs/<payload>_<ts>.txt` (the real result — often tens of
  thousands of lines), `output/exports/` (f3d/step/stl/urdf), `output/screenshots/`.

## Running a simulation
1. **Confirm MCP is reachable** before anything:
   `curl -s -m 3 http://127.0.0.1:27182/mcp -o /dev/null -w "HTTP %{http_code}\n"`
   HTTP 000 / no response = Fusion's **MCP Server add-in is not running**. The
   controller auto-*launches Fusion* but does NOT enable the add-in unless it's
   set to run on startup — user must do Tools → Scripts and Add-Ins → MCP Server
   → Run (or `--no-launch` if already up). This is a setup state, not a code bug.
2. **Verify which payload the controller will send** — see pitfall below.
3. Run in **background** (`terminal background=true, notify_on_complete=true`).
   Full "ALL modules + capture" builds take several minutes; foreground caps at
   600s. Poll the newest `output/logs/<payload>_*.txt`, not the controller stdout
   (stdout just echoes the payload text being transmitted — not results).
4. Typical invocation:
   `python src/run_simulation.py --module ALL --capture`
   Single module: `--module walk|rom|transform|robot|truck|...`. Stop mid-run by
   creating `output/stop.flag` (file-based, NOT a `--stop` CLI arg).

## Pitfalls
- **Controller hardwires `PAYLOAD_FILE` to a stale version.** `run_simulation.py`
  often pins `PAYLOAD_FILE = os.path.join(BASE_DIR, "optimus_v16.py")` while the
  newest payload is v17. "Run the vN simulation" REQUIRES patching that line first
  (`grep -n PAYLOAD_FILE src/run_simulation.py`) or you silently run the old one.
- **README / CHANGELOG lag the code by many versions.** Docs may say "v9" while
  `src/` holds v14–v17. For version questions, trust `git log --oneline`, actual
  `src/*.py` files, and in-file version markers (`grep -n "V17 NEW\|V16 NEW"`) —
  NOT the README/CHANGELOG. See references/multi-version-triage.md.
- **Duplicate/near-identical version files** (`optimus_v_14.py`,
  `optimus_prime_v14.py`, `old_code/...`) are clutter; `diff -q` to confirm before
  recommending cleanup. Keep newest + optionally one prior for reference.
- **Payload runs in Fusion's Python, not local.** Local `python -c ast.parse` only
  checks syntax; `adsk` imports won't resolve locally and that's expected.
- **`pipeline.py` version-drift → false FAIL on every run.** The build pipeline's
  `validate_outputs()` often globs hardcoded version names
  (`version_dir.glob("BOM_v14_*.csv")`, `ASSEMBLY_GUIDE_v14_*.txt`) while the
  current payload emits `BOM_v17_*` / `ASSEMBLY_GUIDE_v17_*`. Result: a perfect run
  is reported as FAIL. Fix by making the globs **version-agnostic** (`BOM_v*_*.csv`,
  `ASSEMBLY_GUIDE_v*_*.txt`), and grep the payload for what it actually emits
  (`grep -n "BOM_FILE\|ASSEMBLY_FILE" src/optimus_vN.py`). Same drift lives in
  stale print labels ("Run Optimus Prime v14 Simulation"). This is the same
  version-pinning class as the `PAYLOAD_FILE` pitfall — audit BOTH the controller
  and the pipeline when bumping versions.
- **AST-audit the whole tree, but only the active tree must be clean.** Walking
  every `.py` for `ast.parse` typically surfaces failures — they cluster in
  `old_code/` and `*/old-codes/` archives (bad chars, unterminated strings). That's
  expected dead weight; only `src/` (controller + pipeline + capture + current
  payload) needs to parse clean. Don't flag archive parse-failures as project bugs.

## Low-RAM builds: hang vs. working
On ~6GB machines the full ALL+capture build is slow and has a **silent phase** that
looks like a hang but isn't:
- Geometry build logs steadily (tens of thousands of lines), then dumps a full-body
  `DIAG [OP_*] bodies(N)` list — right after that the script enters
  **interference/collision analysis**, an O(n²) pass over 140+ bodies that writes
  NOTHING to the log until a module completes. 5–10 min of log silence here is normal.
- To distinguish stall from progress: the process staying alive
  (`process action=poll`) + log mtime freshness (`date +%s - $(date -r "$f" +%s)`)
  + zero ERROR/CRITICAL/WARN. If the Python process is alive and error counts are 0,
  it's grinding, not dead.
- The README's "~2–3 min full run" estimate predates the v13–v17 electronics/mass/
  interference additions and is unrealistic on low-RAM — don't trust it.
- To confirm the engine works end-to-end quickly, offer a light single module
  (`--module robot --capture`) instead of ALL.

## Verification when there's no test suite
These repos have no canonical test/lint/build (the real run needs live Fusion).
For a code edit like repointing `PAYLOAD_FILE`, do **ad-hoc verification**: write a
`hermes-verify-*.py` script to an OS-safe tempfile dir, assert the changed behavior
(regex the assignment, confirm target file exists, `ast.parse` both files), run it,
clean it up, and report it explicitly as *targeted ad-hoc verification, not suite
green*. `execute_code` may be blocked (arbitrary-subprocess guard) — use
write_file + terminal `python <path>` instead. Don't re-run identical passing
verification just because a system nudge re-flags an already-deleted temp file.

See references/multi-version-triage.md for the version-analysis workflow.

## Static code+math engineering verification (no Fusion / no MCP)
A frequent ask is to **verify the engineering of a payload WITHOUT running Fusion**
(e.g. "do a rigorous physical/mechanical review of optimus_vN.py — do NOT run it").
This is pure static analysis of the Python source. No MCP, no `adsk` resolution.
Treat it as a code review with physics math bolted on.

### What to extract and check (typical humanoid/CAD payload)
1. **Actuator profiles + torque margins.** Find the `ACTUATOR_PROFILES` dict
   (rated torque per servo class) and BOTH calculators if present — they often
   disagree. e.g. `estimate_servo_loads()` (hand-typed mass/lever guesses) vs
   `estimate_real_joint_torques()` (masses pulled from `comp.physicalProperties.mass`).
   Flag any joint with margin < 1.5× as under-specified (use THAT threshold even
   if the code's own `MARGINAL` cutoff is looser, e.g. 0.9×).
   - Torque formula (kgf·cm): `need = (mass_kg * 9.81 * lever_cm/100) / 0.0981`
     which simplifies to `mass_kg * lever_cm`. Verify the code uses it consistently.
   - Watch for the **servo-size vs geometry mismatch**: a joint BOM'd/assigned as
     one servo (e.g. DS3225MG) but physically built by another's builder
     (e.g. `mg996r()` MG996R-sized pocket) — the pocket won't fit the bigger servo.
2. **Joint limits sanity.** `JOINT_LIMITS` dict. Flag anatomically impossible or
   self-colliding ranges (e.g. ankle yaw 95°, hip yaw ±95°) and ranges too small
   for function (ankle pitch ±20° cannot support bipedal balance recovery).
3. **Mass / CoM / stability.** Sum `link_mass` (URDF dict) or real component masses.
   Check the ZMP/CoM check actually tests the **hard case (single-leg support)**,
   not only double-support. A biped's limiting pose is single-leg.
4. **Structural safety factors.** Bracket/plate bending check
   (`sigma = M·c/I`, rectangular cantilever). Verify the **unit conversion**:
   kgf·cm → N·mm is `×98.0665` only — a stray `×10.0` inflates stress 10× and
   makes every bracket fail. Compare SF against `MIN_SAFETY_FACTOR` (often 2.5×).
5. **3D-printability.** `CLEARANCE` (generic FDM ~0.06 cm = 0.6 mm is tight;
   prefer 0.08–0.10 cm), `BEARING_FIT_TOLERANCE`, and sub-mm features
   (tendon/wire Ø < 0.8–1.0 mm, grooves < 1.0 mm) that won't print on FDM.
6. **Electronics/power realism.** Total servo count (build it from the actual
   builder calls + BOM, don't trust the comment); real peak current is
   ~1–2.5 A per servo × count (often ~20 A, not the 10 A a budget may claim);
   servo-rail fuse must exceed peak; pack must physically fit the built bay
   (a "recommended 3S 5000 mAh" won't fit a 2S 1300 mAh bay).

### Pitfalls specific to this class
- **Material-library fallback silently poisons every mass number.** If
  `assign_material()` resolves names against Fusion's **cloud material library**
  (e.g. `get_material("PETG")`), an offline/library-less run returns `None` for
  EVERY component → every part uses Fusion's **default density (≈ steel)**, making
  `compute_total_mass_report()` / `estimate_real_joint_torques()` output
  garbage. Always ask/check whether materials actually resolved; the real-mass
  check is only as good as the material assignment. The URDF `link_mass` dict is a
  usable independent proxy when CAD masses are unverified.
- **Two calculators, one truth.** When a payload has both a hand-typed "Module 9b"
  load estimate and a "Module 13" real-mass check, the hand-typed one is usually
  optimistic by 2–3×. Lead with the real-mass check; call out the discrepancy.
- **Matching/logic bugs in safety checks.** Substring matching that computes a
  key but never uses it (falls back to a default torque) can mis-route loads.
- **Wiring maps can over-specify.** A `PCA9685` has 16 channels; a node map citing
  >16 channels, or more channels than servos actually built, is a doc bug.

### Doing the math locally (no Fusion)
Use `terminal` with `python <path>` (NOT `execute_code`, which may be guarded).
Recompute margins, bracket SFs, and mass sums independently — never just echo the
script's own logged numbers. See references/static-verify-checklist.md for the
worked formulas and the v17 bug inventory (unit-conversion error, material fallback,
servo/bracket failures) as a concrete reference.

## Low-RAM builds: hang vs. working
