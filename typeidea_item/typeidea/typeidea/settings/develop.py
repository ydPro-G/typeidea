# 线下数据库配置文件

from .base import * # NOQA

DEBUG = True # 开发环境为True，上线后关闭

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}