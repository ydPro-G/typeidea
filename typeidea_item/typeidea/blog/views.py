from django.shortcuts import render
from django.http import HttpResponse 
# Create your views here.
# 编写url对应的视图函数
# 编写列表页url对应视图函数----编写文章页url对应视图函数

# 列表页view
def post_list(request, category_id=None, tag_id=None):
    # 请求，模板名称，字典数据-传递到模板中
    return render(request, 'blog/list.html', context={'name': 'post_list'})


# 文章页view
def post_detail(request, post_id=None):
    return render(request, 'blog/detail.html', context={'name': 'post_detail'})


