# SMTP email credentials stub
import os

EMAIL_HOST = os.getenv('TRATROUBLE_EMAIL_HOST', 'mail.domain.tld')
EMAIL_PORT = int(os.getenv('TRATROUBLE_EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('TRATROUBLE_EMAIL_HOST_USER', '<addme>')
EMAIL_HOST_PASSWORD = os.getenv('TRATROUBLE_EMAIL_HOST_PASSWORD', '<addme>')
EMAIL_USE_TLS = os.getenv('TRATROUBLE_EMAIL_USE_TLS', 'True').lower() == 'true'

# Add the default from email address for SMTP
DEFAULT_FROM_EMAIL = os.getenv('TRATROUBLE_DEFAULT_FROM_EMAIL', 'admin@domain.tld')
