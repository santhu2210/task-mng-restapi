import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'task_mng_dev',
        'USER': 'devuser',
        'PASSWORD': 'Welcome123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

USE_TOKEN = False

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'log_dir')

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)
