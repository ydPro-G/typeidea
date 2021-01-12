
启动服务器：python manage.py runserver

定义URL，编写视图，编写模板


python -m venv name  #创建虚拟环境
S/a:启动虚拟环境
python manage.py makemigrations:创建数据库迁移文件
python manage.py migrate 创建表
python manage.py createsuperuser:根据提示，创建管理员

username:gg
password:gg123456789


1.在model层中添加get_navs函数，获取分类信息
2.在view中获取这个函数返回的字典数据，并添加到context中
3.在模板获取views新添加的数据，并添加html代码展示分类数据