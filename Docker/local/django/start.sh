#!/bin/bash

set -o errexit  # stops script if there is an error

set -o pipefail

set -o nounset #ensures that uninitialized variables are not used

python manage.py migrate --no-input
python manage.py collectstatic --no-input
exec python manage.py runserver 0.0.0.0:8000
