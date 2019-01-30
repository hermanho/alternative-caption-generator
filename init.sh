#!/bin/bash
set -e

echo "Starting ..."
python3.6 ./app/bin/download_model.py --model-dir ./app/etc
python3.6 ./app/medium_show_and_tell_caption_generator/httpapp.py
