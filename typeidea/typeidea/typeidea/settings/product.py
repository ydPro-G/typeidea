from .base import * # NOQA

# 正式配置文件

DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CONN_MAX_AGE': 60,
        # 存放表情
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}


ADMINS = MANAGERS = (
    ('姓名', '<邮件地址>'),
)

EMALL_HOST = '<邮件smtp服务地址>'
EMALL_HOST_USER = '<邮箱登录名>'
EMALL_HOST_PASSWORD = '<邮箱登录密码>'
EMALL_SUBJECT_PREFIX = '<邮箱标题前缀>'
DEFAULT_FROM_EMALL = '<邮件展示发件人地址>'
SERVER_EMALL = '<邮件服务器>'
STATIC_ROOT = '/home/user/venvs/typeidea-env/static_files/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers':False,
    'formatters' : {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s:'
                      '%(funcName)s:%(lineno)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/logs/typeidea.log',
            'formatter': 'default',
            'maxBytes': 1024 * 1024, # 1M
            'backupCount': 5,
        },
    },

    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'TIMEOUT': 300,
        'OPTIONES': {
            # 'PASSWORD': '<对应密码>',
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
    }
}
