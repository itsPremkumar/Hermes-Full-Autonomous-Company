# Fresher LaTeX Resume — improvement checklist (from this session)

User had a working LaTeX resume that UNDERSELLS them. Fixes that moved the needle:

1. **"student" -> "graduate"** + add grad year (B.Tech IT 2021-2025). Recruiters filter on status.
2. **Lead with the 2 mandatory flagships** (user-designated real, user-backed repos):
   - `Automated-Video-Generator` — TypeScript/Node/Remotion/FFmpeg; 20 stars; 150+ commits;
     Electron app + MCP server; green CI. (User originally described it as just
     "Python, Node.js, FFmpeg" — wildly understated.)
   - `sproutern-open-source` — Next.js/TS; live platform; 367 tests green; CI green.
3. **Add proof numbers** to every project: stars, commits, test counts, forks.
4. **Skills = REAL stack**, not the textbook list. Drop "Google Cloud, MATLAB"; add
   TypeScript, TensorFlow, Flutter, Docker, GitHub Actions, Next.js, Firebase.
5. **Add OSCG 2026 Mentor** as top achievement (a real differentiator the user omitted).
6. **CGPA** line only if >=7.5 (placeholder, user fills).
7. **Drop weak projects** to hold ONE page (e.g. MATLAB/SVM waste classification) unless
   breadth requested.
8. **Keep the user's LaTeX style** (packages, geometry, fancyhdr, titlerule) — only change
   content so it compiles in their existing setup.

Deliverable: `RESUME_improved.tex` (compile -> PDF in user's TeX editor/Overleaf; agent
cannot run LaTeX here).
