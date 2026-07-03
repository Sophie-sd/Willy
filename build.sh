#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input

python manage.py shell <<'EOF'
from django.core.management import call_command
from catalog.models import Product

if Product.objects.count() == 0:
    call_command('loaddata', 'catalog/fixtures/initial_data.json')
EOF
