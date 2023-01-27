#!/bin/bash
set -euxo pipefail
export LD_LIBRARY_PATH=/usr/local/lib
cd /carsten
git pull
python3 run.py