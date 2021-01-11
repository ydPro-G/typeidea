from setuptools import setup, find_packages

setup(
    name='typeidea',
    version='0.1',
    description='Blog System base on Django',
    author='ydpro',
    author_email='nicai@163.com',
    url='https://www.ydpro_Blog.com',
    license='MIT',
    packages=find_packages('typeidea'),
    package_dir={'': 'typeidea'},
    # package_data={'': [    # 方法一：打包数据文件
    #     'themes/*/*/*/*',  # 需要按目录层级匹配  
    # ]}，
    include_package_data=True # 方法二： 配合MANIFEST.in文件
    # 依赖版本
    install_requires=[
        'django~=1.11',
    ],
    # 依赖包，下载时一起下载
    extras_require={
        'ipython': ['ipython==6.2.1']
    },
    # 指明要放到bin目录下的可执行文件
    scripts=[
        'typeidea/manage.py',
    ],
    entry_points={
        'console_scripts': [
            'typeidea_manage = manage:main',
        ]
    },
    classifiers=[  # Optional
        # 软件成熟度
        # 3 - alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # 指明项目受众
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',


        # 选择项目许可证(License)
        'License :: OSI Approved :: MIT License',

        # 指定项目需要使用的Python版本
        'Programming Language :: Python :: 3.8',
    ]
)