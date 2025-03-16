from os import path, getenv
from dotenv import load_dotenv
from .base import *
from .base import BASE_DIR


local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


SECRET_KEY = getenv("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG")

SITE_NAME = getenv("SITE_NAME")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
# 0.0.0.0 -> tells server to listen for all available  ipv4 ports on the machine


ADMIN_URL = getenv("ADMIN_URL")
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")

MAX_UPLOAD_SIZE = 1 * 1024 * 1024

CSRF_TRUSTED_ORIGINS = ["hhtps://localhost:8080"]
LOCKOUT_DURATION = timedelta(minutes=1)
LOGIN_ATTEMPTS = 3

OTP_EXPIRATION = timedelta(minutes=1)
