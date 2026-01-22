#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

# Install dependencies
<<<<<<< HEAD:BE/batch_processor/build.sh
pip install -r ../requirements.txt
=======
pip install -r requirements.txt
>>>>>>> stage:api/build.sh

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
