#!/bin/bash
set -euxo pipefail
set -o allexport
. /carsten/.env
set +o allexport
export LD_LIBRARY_PATH=/usr/local/lib
export PYTHONUNBUFFERED=1
cd /carsten
git pull
python3 run.py