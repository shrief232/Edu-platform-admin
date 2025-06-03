import os
from datetime import timedelta
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = []

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'auth_plugin': 'mysql_native_password'
        }
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',  
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

STRIPE_TEST_API_KEY = 'your-stripe-api-key'


INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.sites', 
    'allauth',
    'allauth.account',  
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',  
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'rest_framework_simplejwt',
    'corsheaders',
    "modeltranslation", 
    "users",
    "courses",
    "quizzes",
    'payments',
    'channels',
    'notifications',
    'final',
    'profiles',
]




ASGI_APPLICATION = 'edu_platform.asgi.application' 

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],  
        },
    },
}


AUTH_USER_MODEL = 'users.CustomUser'



MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.locale.LocaleMiddleware",  
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'edu_platform.backends.EmailAuthBackend',
)

SITE_ID = 1

LANGUAGES = [
    ("en", "English"),
    ("ar", "العربية"),
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=260),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'AUTH_COOKIE': 'access_token',  
    'AUTH_COOKIE_DOMAIN': None,
    'AUTH_COOKIE_SECURE': False,    
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': 'Lax',
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt-auth'
JWT_AUTH_REFRESH_COOKIE = 'jwt-refresh-token'
JWT_AUTH_SECURE = True  
JWT_AUTH_SAMESITE = 'Strict' 

# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LANGUAGE_CODE = "en"
LOCALE_PATHS = [BASE_DIR / "locale"]

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",  
    "http://127.0.0.1:5174",  
]


STRIPE_TEST_API_KEY = config("STRIPE_TEST_API_KEY")

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config("GOOGLE_CLIENT_ID"),
            'secret': config("GOOGLE_CLIENT_SECRET"),
            'key': ''
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True  
CSRF_COOKIE_SECURE = True 
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174", 
    "http://127.0.0.1:5174", 
]
CORS_ALLOW_CREDENTIALS = True


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

ROOT_URLCONF = 'edu_platform.urls'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": "Extra Smart Admin",
    "site_header": "Extra Smart Academy",
    "welcome_sign": "Welcome to the Extra Smart Academy Admin",
    "copyright": "Smart Academy",
    "search_model": "users.CustomUser",
    "show_ui_builder": True,
    "site_logo": "extra-logo.png",  
    "login_logo": "extra-logo.png",
    "site_logo_classes": "img-fluid p-1",   
    "custom_css": "css/admin_custom.css", 
}
JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",  
    "dark_mode_theme": "darkly",  

    # حجم النصوص
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": True,
    "sidebar_nav_small_text": True,

    
    "sidebar_search_visible": True,
    "navbar_search_visible": True,
    "navbar_actions_visible": True,
    "navbar_actions_sticky": True,

    
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,

    
    "accent": "accent-warning",
    "sidebar": "sidebar-dark-warning",
    

   
    "navbar": "navbar-dark",
    "brand_color": "navbar-warning",
}
