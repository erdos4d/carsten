#!/bin/bash
set -euxo pipefail
cd /carsten
git pull
python3 run.py