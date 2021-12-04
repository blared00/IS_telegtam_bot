from pathlib import Path

from decouple import config


TOKEN = config('TOKEN')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
    },
}


BASE_DIR = Path(__file__).resolve().parent.parent
