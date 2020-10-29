from django.shortcuts import render
from django.http import HttpResponse 

from .models import Post,Tag
# Create your views here.
# 编写url对应的视图函数
# 编写列表页url对应视图函数----编写文章页url对应视图函数




# 列表页view：标题和摘要展示
# tag和post是多对多关系，所以先获取tag对象，查询tag_id，不存在为空，存储在保存id并且筛选所有状态正常的展示出来
# 没有就为空，如果tag_id为空，查询所有文章状态正常的展示，如果category_id不为空，展示所有分类正常状态文章
def post_list(request, category_id=None, tag_id=None):
    if tag_id:
        try:
            # 查询所有标签id
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    # 当程序中的 try 块没有出现异常时，程序就会执行 else 块
    else:
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            post_list = post_list.filter(category_id=category_id)

    # 请求，模板名称，字典数据-传递到模板中
    return render(request, 'blog/list.html', context={'post_list': post_list})




# 文章页view: 展示文章id
def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request,'blog/detail.html', context={'post': post})

