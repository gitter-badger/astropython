"""
Django settings for astropython project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

"""

from config import *
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY='cc*u4n__@&=^3x=hoyu-ndg(l^1^_4o72)bs4jt#5a#ewqhq7d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

ALLOWED_HOSTS = ['*']

# Application definition

#Do not change the order of installed apps

INSTALLED_APPS = (
    'grappelli', # Cleaner admin panel,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit', # Easy tagging functionality
    'secretballot',
    'crispy_forms',
    'compressor',
    'watson',
    'django.contrib.sites',
    'moderation', # Adding moderations
    'main',
    'social.apps.django_app.default',#Social  Authentication
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'secretballot.middleware.SecretBallotIpUseragentMiddleware',
    'watson.middleware.SearchContextMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    )


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'astropython.urls'

WSGI_APPLICATION = 'astropython.wsgi.application'

TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )


#Add social auth options here
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.google.GoogleOAuth2',
    'social.backends.github.GithubOAuth2',
    'social.backends.yahoo.YahooOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
)

#Database configuration(Need to change this !)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'amanjhunjhunwala$Astropython',
        'USER': 'amanjhunjhunwala',
        'PASSWORD': 'astropython',
        'HOST': 'mysql.server',
    }
}

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = False

SITE_ID =1

# Static and Media files configuration (CSS, JavaScript, Images)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "media")

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "static_root")

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), "static", "static_files"),
)

TEMPLATES[0]['DIRS'] = [
    os.path.join(BASE_DIR, 'templates'),
]

#States of a post
STATE_CHOICES = (
	('raw', 'raw'),
	('submitted', 'submitted'),
 )

INPUT_CHOICES = (
	('WYSIWYG', 'WYSIWYG'),
	('Markdown', 'Markdown'),
 )

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'astropython-*****'
EMAIL_HOST_PASSWORD = '****astropython'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SOCIAL_AUTH_PIPELINE =(
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)