from aiogoogle.auth.creds import ServiceAccountCreds
from django.conf import settings

service_account_keys = {
    "type": "service_account",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    **settings.ENV_INFO,
}

creds = ServiceAccountCreds(scopes=settings.SCOPES, **service_account_keys)
