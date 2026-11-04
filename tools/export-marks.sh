#!/bin/zsh
# Renders every SVG in brand/marks/ to a transparent 1024px PNG in brand/marks/png/.
# Needs Google Chrome and python3. Run from anywhere: zsh tools/export-marks.sh
set -e
cd "${0:A:h}/.."

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT=4832
SIZE=1024

python3 -m http.server $PORT --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER=$!
trap "kill $SERVER" EXIT
sleep 1

mkdir -p brand/marks/png
for svg in brand/marks/*.svg; do
  name="${svg:t:r}"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --default-background-color=00000000 \
    --window-size=$SIZE,$SIZE --virtual-time-budget=10000 \
    --screenshot="$PWD/brand/marks/png/$name.png" \
    "http://127.0.0.1:$PORT/tools/render.html?m=$name" >/dev/null 2>&1
  echo "brand/marks/png/$name.png"
done
