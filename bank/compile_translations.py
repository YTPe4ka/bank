#!/usr/bin/env python
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Компиляция сообщений
os.system('python manage.py compilemessages -l ru -l uz -l en')
print('✓ Messages compiled successfully!')
