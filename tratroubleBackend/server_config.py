# Server configuration
import os

# Allowed hosts for the Django application
ALLOWED_HOSTS = os.getenv('TRATROUBLE_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Debug mode
DEBUG = os.getenv('TRATROUBLE_DEBUG', 'True').lower() == 'true'

# Secret key for Django (should be changed in production)
SECRET_KEY = os.getenv('TRATROUBLE_SECRET_KEY', 'django-insecure-%zzj%iu8eeh%wm^k-p6o*@@hoz*u4q*gjxi9b8!eah5f4pb$*q')

# CORS allowed origins (for frontend requests)
CORS_ALLOWED_ORIGINS = os.getenv('TRATROUBLE_CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:8000').split(',')
