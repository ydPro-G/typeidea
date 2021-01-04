# 线下数据库配置文件

from .base import * # NOQA

DEBUG = True # 开发环境为True，上线后关闭

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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