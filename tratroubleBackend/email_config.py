# Email related configuration
import os

EMAIL_VERIFICATION_DOMAIN = os.getenv('TRATROUBLE_EMAIL_VERIFICATION_DOMAIN', 'your.domain.tld')
EMAIL_VERIFICATION_APP_NAME = os.getenv('TRATROUBLE_EMAIL_VERIFICATION_APP_NAME', 'com.mydomain.myappname')
