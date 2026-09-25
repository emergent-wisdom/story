#!/bin/sh
# Refresh a run's data file every minute while the agent works: node extract.mjs reads a snapshot, never the live server.
# usage: MEANING_MODEL_DIR=/path/to/meaning-model ./live.sh <run folder> <name>
while true; do
  node extract.mjs --run "$1" --out "public/data/$2.json" > /dev/null 2>> live.log || true
  sleep 60
done
