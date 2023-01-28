#!/bin/bash
until [ -f /.env ]; do
  sleep 5
done
set -euxo pipefail
set -o allexport
. /.env
set +o allexport
export LD_LIBRARY_PATH=/usr/local/lib
export PYTHONUNBUFFERED=1
cd /carsten
git pull
python3 run.py
