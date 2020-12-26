#!/bin/bash
cd "$(dirname "$0")"
source ./.env
python3 src/clock.py $1 
