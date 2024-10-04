# ecommerce/wsgi.py
import sys
import os
from django.core.wsgi import get_wsgi_application
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_wsgi_application()
