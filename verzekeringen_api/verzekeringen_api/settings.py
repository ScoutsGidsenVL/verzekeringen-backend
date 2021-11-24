"""
Django settings for verzekeringen_api project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os, logging, logging.config
from environs import Env


# Get a pre-config logger
logger = logging.getLogger(__name__)


# Load the .env file
env = Env()
env.read_env()


# Load the appropriate environment file
# In .env, define as only variable ENVIRONMENT
# Set it to 'development' or 'production' and define the appropriate variables
# in .env.development and .env.production
# Default: development
#
# For testing the application outside of a docker, config rules can be defined
# in .env.development.local
# environments = [".env.development.local", ".env.development", ".env.production"]
# environment_conf = env.str("ENVIRONMENT", default="development")
# environment_loaded = False

# if environment_conf:
#     try:
#         env = Env()
#         env.read_env(".env." + environment_conf)

#         environment_loaded = True
#         logger.debug("Environment file loaded: .env.%s", environment_conf)
#     except Exception:
#         logger.warn(
#             "WARN: Environment file .env.%s not found ! Defaulting to next configured default environment.",
#             environment_conf,
#         )

#     if not environment_loaded:
#         for environment in environments:
#             if environment == ".env." + environment_conf:
#                 pass

#             try:
#                 env = Env()
#                 env.read_env(".env." + environment)

#                 logger.debug("Environment file loaded: .env." + environment)
#                 environment_loaded = True
#             except Exception:
#                 pass


LOGGING_CONFIG = None
LOGGING_LEVEL = env.str("LOGGING_LEVEL", "INFO")
LOGGING_LEVEL_ROOT = env.str("LOGGING_LEVEL_ROOT", "ERROR")
# LOGGING_LEVEL = "DEBUG"
# LOGGING_LEVEL_ROOT = "DEBUG"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(levelname)-7s - %(name)-12s - %(message)s",
        },
        "simple": {
            "format": "%(levelname)-8s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOGGING_LEVEL,
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": LOGGING_LEVEL,
            "filename": "verzekeringen-api.debug.log",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOGGING_LEVEL_ROOT,
    },
    "loggers": {
        "mozilla_django_oidc": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "scouts-auth": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        # @TODO
        "scouts_auth": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "groupadmin": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "inuits": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING)

logging.info("LOGGING_LEVEL: %s", LOGGING_LEVEL)
logging.info("LOGGING_LEVEL_ROOT: %s", LOGGING_LEVEL_ROOT)


def correct_url(prefix, url):
    if not url.startswith("http"):
        return prefix + url
    return url


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = env.str("BASE_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_URL = env.str("BASE_URL")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Turn this off because of existing database we work with
SILENCED_SYSTEM_CHECKS = ["fields.W342"]


# Application definition

INSTALLED_APPS = [
    "apps.signals",
    "django.contrib.admin",
    "django.contrib.auth",
    "scouts_auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "drf_yasg2",
    "corsheaders",
    "inuits",
    "groupadmin",
    "apps.members",
    "apps.equipment",
    "apps.locations",
    "apps.insurances",
    "apps.info",
]

MIGRATION_MODULES = {
    "apps.base": "migrations",
    "apps.equipment": "migrations",
    "apps.info": "migrations",
    "apps.insurances": "migrations",
    "apps.locations": "migrations",
    "apps.members": "migrations",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "verzekeringen_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "verzekeringen_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
django_pw_validation = "django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Brussels"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Rest framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "scouts_auth.oidc.InuitsOIDCAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "verzekeringen_api.pagination.PageNumberPagination",
    "EXCEPTION_HANDLER": "inuits.exceptions.drf_exception_handler",
}


# CORS
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")

# OIDC

AUTH_USER_MODEL = "groupadmin.ScoutsUser"
AUTHORIZATION_ROLES_CONFIG_PACKAGE = "initial_data"
AUTHORIZATION_ROLES_CONFIG_YAML = "roles.yaml"
AUTHENTICATION_BACKENDS = {
    "groupadmin.services.ScoutsOIDCAuthenticationBackend",
}
OIDC_OP_ISSUER = env.str("OIDC_OP_ISSUER")
OIDC_OP_AUTHORIZATION_ENDPOINT = correct_url(OIDC_OP_ISSUER, env.str("OIDC_OP_AUTHORIZATION_ENDPOINT"))
OIDC_OP_TOKEN_ENDPOINT = OIDC_OP_ISSUER + env.str("OIDC_OP_TOKEN_ENDPOINT")
OIDC_OP_USER_ENDPOINT = correct_url(OIDC_OP_ISSUER, env.str("OIDC_OP_USER_ENDPOINT"))
OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET")
OIDC_RP_SIGN_ALGO = env.str("OIDC_RP_SIGN_ALGO", default="RS256")
OIDC_DRF_AUTH_BACKEND = "groupadmin.services.ScoutsOIDCAuthenticationBackend"
OIDC_OP_JWKS_ENDPOINT = correct_url(OIDC_OP_ISSUER, env.str("OIDC_OP_JWKS_ENDPOINT"))


# SCOUTS
GROUP_ADMIN_BASE_URL = env.str("GROUP_ADMIN_BASE_URL")
KNOWN_ADMIN_GROUPS = env.list("KNOWN_ADMIN_GROUPS")
KNOWN_TEST_GROUPS = env.list("KNOWN_TEST_GROUPS")
KNOWN_ROLES = env.list("KNOWN_ROLES")
SECTION_LEADER_IDENTIFIER = env.str("SECTION_LEADER_IDENTIFIER")
GROUP_ADMIN_ALLOWED_CALLS_ENDPOINT = GROUP_ADMIN_BASE_URL + "/"
GROUP_ADMIN_PROFILE_ENDPOINT = GROUP_ADMIN_BASE_URL + "/lid/profiel"
GROUP_ADMIN_MEMBER_SEARCH_ENDPOINT = GROUP_ADMIN_BASE_URL + "/zoeken"
GROUP_ADMIN_MEMBER_DETAIL_ENDPOINT = GROUP_ADMIN_BASE_URL + "/lid"
GROUP_ADMIN_MEMBER_LIST_ENDPOINT = GROUP_ADMIN_BASE_URL + "/ledenlijst"
GROUP_ADMIN_GROUP_ENDPOINT = GROUP_ADMIN_BASE_URL + "/groep"
GROUP_ADMIN_FUNCTIONS_ENDPOINT = GROUP_ADMIN_BASE_URL + "/functie"
BELGIAN_CITY_SEARCH_ENDPOINT = GROUP_ADMIN_BASE_URL + "/gis/gemeente"
COMPANY_NON_MEMBER_DEFAULT_FIRST_NAME = "FIRMA:"


# Storages/S3
DEFAULT_FILE_STORAGE = env.str("DEFAULT_FILE_STORAGE")
FILE_UPLOAD_ALLOWED_EXTENSIONS = env.list("FILE_UPLOAD_ALLOWED_EXTENSIONS")

USE_S3_STORAGE = env.bool("USE_S3_STORAGE", False) == True
STATIC_URL = "static/"
STATIC_ROOT = env.str("STATIC_ROOT")
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
if USE_S3_STORAGE:
    AWS_ACCESS_KEY_ID = env.str("S3_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = env.str("S3_ACCESS_SECRET")
    AWS_STORAGE_BUCKET_NAME = env.str("S3_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = env.str("S3_ENDPOINT_URL")
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_SIGNATURE_VERSION = "s3v4"
else:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/
    STATIC_URL = "static/"
    STATIC_ROOT = env.str("STATIC_ROOT")
    MEDIA_URL = "media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# EMAIL RESOURCES
RESOURCES_PATH = env.str("RESOURCES_PATH")
RESOURCES_MAIL_TEMPLATE_PATH = RESOURCES_PATH + env.str("RESOURCES_MAIL_TEMPLATE_PATH")
RESOURCES_CLAIMS_INSURER_TEMPLATE_PATH = RESOURCES_MAIL_TEMPLATE_PATH + env.str(
    "RESOURCES_CLAIMS_INSURER_TEMPLATE_PATH"
)
RESOURCES_CLAIMS_VICTIM_TEMPLATE_PATH = RESOURCES_MAIL_TEMPLATE_PATH + env.str("RESOURCES_CLAIMS_VICTIM_TEMPLATE_PATH")
RESOURCES_CLAIMS_STAKEHOLDER_TEMPLATE_PATH = RESOURCES_MAIL_TEMPLATE_PATH + env.str(
    "RESOURCES_CLAIMS_STAKEHOLDER_TEMPLATE_PATH"
)
INSURANCE_FILES_BASE_PATH = env.str("INSURANCE_FILES_BASE_PATH")
INSURANCE_FILE_NAME_PREFIX = env.str("INSURANCE_FILE_NAME_PREFIX")
INSURANCE_CLAIM_FILES_BASE_PATH = env.str("INSURANCE_CLAIM_FILES_BASE_PATH")
INSURANCE_CLAIM_FILE_NAME_PREFIX = env.str("INSURANCE_CLAIM_FILE_NAME_PREFIX")
INSURANCE_CLAIM_FILE_NAME_SUFFIX = env.str("INSURANCE_CLAIM_FILE_NAME_SUFFIX")
STORE_INSURANCE_CLAIM_REPORT_WHILE_DEBUGGING = env.bool("STORE_INSURANCE_CLAIM_REPORT_WHILE_DEBUGGING")

# EMAIL
# We are going to use anymail which maps multiple providers like sendinblue with default django mailing code
# For more info see https://anymail.readthedocs.io/en/stable/esps/sendinblue/
def setup_mail():
    global EMAIL_BACKEND
    global ANYMAIL
    global EMAIL_INSURANCE_FROM
    global EMAIL_INSURANCE_TO
    global EMAIL_INSURANCE_CC
    global EMAIL_INSURANCE_BCC
    global EMAIL_TEMPLATE
    global EMAIL_INSURER_ADDRESS

    if USE_SEND_IN_BLUE:
        EMAIL_BACKEND = env.str("SEND_IN_BLUE_BACKEND")
        ANYMAIL["SENDINBLUE_API_KEY"] = env.str("SEND_IN_BLUE_API_KEY")
        ANYMAIL["SENDINBLUE_TEMPLATE_ID"] = env.str("SEND_IN_BLUE_TEMPLATE_ID")
        EMAIL_TEMPLATE = ANYMAIL["SENDINBLUE_TEMPLATE_ID"]
    else:
        EMAIL_TEMPLATE = None

    FROM_LIST = env.str("EMAIL_INSURANCE_FROM", None)
    if FROM_LIST:
        EMAIL_INSURANCE_FROM = FROM_LIST.split(",")
    EMAIL_INSURER_ADDRESS = env.str("EMAIL_INSURER_ADDRESS")
    CC_LIST = env.str("EMAIL_INSURANCE_CC", None)
    if CC_LIST:
        EMAIL_INSURANCE_CC = CC_LIST.split(",")
    BCC_LIST = env.str("EMAIL_INSURANCE_BCC", None)
    if BCC_LIST:
        EMAIL_INSURANCE_BCC = BCC_LIST.split(",")


# DJANGO MAIL SETTINGS
EMAIL_BACKEND = env.str("EMAIL_BACKEND")
EMAIL_URL = env.str("EMAIL_URL")
EMAIL_SENDER = env.str("EMAIL_SENDER")
EMAIL_RECIPIENTS = env.str("EMAIL_RECIPIENTS")
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_PORT = env.str("EMAIL_PORT")
# SEND_IN_BLUE EMAIL SETTINGS
USE_SEND_IN_BLUE = env.bool("USE_SEND_IN_BLUE", False)
# SCOUTS VERZEKERINGEN EMAIL SETTINGS
EMAIL_INSURANCE_FROM = None
EMAIL_INSURANCE_REPLY_TO = EMAIL_INSURANCE_FROM
EMAIL_INSURER_ADDRESS = None
EMAIL_INSURANCE_CC = None
EMAIL_INSURANCE_BCC = None
EMAIL_INSURER_ADDRESS_DEBUG = env.str("EMAIL_INSURER_ADDRESS_DEBUG")
EMAIL_VICTIM_ADDRESS_DEBUG = env.str("EMAIL_VICTIM_ADDRESS_DEBUG")
EMAIL_DECLARANT_ADDRESS_DEBUG = env.str("EMAIL_DECLARANT_ADDRESS_DEBUG")
EMAIL_TEMPLATE = None
PDF_TEMPLATE_PATH = RESOURCES_PATH + "blank_insurance_claim.pdf"
TMP_FOLDER = RESOURCES_PATH + "temp"
ANYMAIL = {}

setup_mail()
