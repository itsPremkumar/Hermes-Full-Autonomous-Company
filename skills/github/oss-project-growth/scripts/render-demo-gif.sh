#!/usr/bin/env bash
# render-demo-gif.sh — Render an autoplaying demo GIF from a REAL output video.
# Uses the project's bundled ffmpeg-static when ffmpeg is not on PATH.
# For OSS landing pages: a moving GIF converts visitors far better than a
# static diagram (especially for a video-generation tool).
#
# Usage:
#   scripts/render-demo-gif.sh <input.mp4> [output.gif] [duration_sec] [width]
#
# Examples:
#   scripts/render-demo-gif.sh output/example_short/Example.mp4 assets/demo.gif 8 480
#   scripts/render-demo-gif.sh output/two_minutes/Test.mp4 public/demo.gif 10 640
set -euo pipefail

IN="${1:?input mp4 required (e.g. output/example_short/Example.mp4)}"
OUT="${2:-assets/demo.gif}"
DUR="${3:-8}"
W="${4:-480}"

# Locate ffmpeg: prefer bundled ffmpeg-static, then PATH.
FF=""
if [ -f node_modules/ffmpeg-static/ffmpeg.exe ]; then
  FF="node_modules/ffmpeg-static/ffmpeg.exe"
elif [ -f node_modules/ffmpeg-static/ffmpeg ]; then
  FF="node_modules/ffmpeg-static/ffmpeg"
elif command -v ffmpeg >/dev/null 2>&1; then
  FF="ffmpeg"
else
  echo "ERROR: no ffmpeg found (no node_modules/ffmpeg-static, no ffmpeg on PATH)" >&2
  exit 1
fi

TMP="$(mktemp -d)"
PAL="$TMP/palette.png"

"$FF" -y -i "$IN" -t "$DUR" \
  -vf "fps=12,scale=${W}:-1:flags=lanczos,palettegen" "$PAL"
"$FF" -y -i "$IN" -i "$PAL" -t "$DUR" \
  -lavfi "fps=12,scale=${W}:-1:flags=lanczos[x];[x][1:v]paletteuse" "$OUT"

echo "wrote $OUT ($(wc -c < "$OUT") bytes)"
rm -rf "$TMP"
