#!/bin/sh
# Follow a run in the shared viewer without writing working exports into public/.
# usage: ./live.sh <run folder> [name]
set -eu
if [ "$#" -lt 1 ]; then
  echo "usage: ./live.sh <run folder> [name]" >&2
  exit 1
fi
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$#" -ge 2 ]; then
  exec node "$script_dir/serve.mjs" --run "$1" --name "$2" --live
fi
exec node "$script_dir/serve.mjs" --run "$1" --live
