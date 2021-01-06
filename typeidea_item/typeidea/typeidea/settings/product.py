from .base import * # NOQA

# 正式配置文件

DEBUG = False

ALLOWED_HOSTS = ['youhost.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '<正式数据库ip>',
        'PORT': 3306,
        'CONN_MAX_AGE': 5 * 60,
        # 存放表情
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}