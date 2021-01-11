# 线下数据库配置文件

from .base import * # NOQA

DEBUG = True # 开发环境为True，上线后关闭

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # # 数据库引擎
        'NAME': 'typeidea_db',  # 你要存储数据的库名
        'USER': 'user_root', # 数据库用户名
        'PASSWORD': '123456', # 密码
        'HOST': 'localhost', # 默认主机
        'POST': 3306, # 使用端口
        # 'CONN_MAX_AGE': 5 * 60,
        # 'OPTIONS': {'charset': 'utf8mb4'}
    },
}

INSTALLED_APPS += [
    'debug_toolbar',
    'silk',
    # 'pympler',
    # 'debug_toolbar_line_profiler',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']


# 富文本编辑配置
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'full',
#         'height': 300,
#         'width': 800,
#         'tabSpaces': 4,
#         'extraPlugins': 'codesnippet', # 配置代码插件
#     },
# }




# 火焰图配置文件
# DEBUG_TOOLBAR_PANELS = [
#     'djdt_flamegraph.FlamegraphPanel',
# ]


# pympler配置文件
# DEBUG_TOOLBAR_CONFIG = {
#     'JQUERY_URL': 'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
# }

# pympler配置文件
# DEBUG_TOOLBAR_PANELS = [
#     'pympler.panels.MemoryPanel',
# ]

# line_profiler配置文件
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar_line_profiler.panel.ProfilingPanel',
# ]