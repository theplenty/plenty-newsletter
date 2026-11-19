#!/usr/bin/env bash
# usage: tools/shot.sh <url> <out.png> <width> <height> <scratch_dir>
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
PROFILE="$5/edge-profile-$RANDOM$RANDOM"
rm -f "$2"
"$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=8000 \
  --no-first-run --window-size="$3,$4" --user-data-dir="$(cygpath -w "$PROFILE")" \
  --screenshot="$(cygpath -w "$2")" "$1" >/dev/null 2>&1
for i in $(seq 1 60); do [ -s "$2" ] && break; sleep 0.5; done
sleep 1; ls -la "$2"
