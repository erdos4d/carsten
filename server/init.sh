#!/bin/bash
set -euxo pipefail
export LD_LIBRARY_PATH=/usr/local/lib
export PYTHONUNBUFFERED=1
cd /carsten
git pull
python3 run.py