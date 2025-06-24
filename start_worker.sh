#!/bin/bash
source /home/ad1429240/api_siad_v3/venv/bin/activate
cd /home/ad1429240/api_siad_v3/app
nohup python worker.py >> /home/ad1429240/api_siad_v3/log/worker.out.log 2>> /home/ad1429240/api_siad_v3/log/worker.err.log &
