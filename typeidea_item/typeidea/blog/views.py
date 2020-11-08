from django.shortcuts import render
from django.http import HttpResponse 

from .models import Post,Tag,Category
from config.models import SideBar
# Create your views here.
# 编写url对应的视图函数
# 编写列表页url对应视图函数----编写文章页url对应视图函数




# 列表页view：标题和摘要展示
# tag和post是多对多关系，所以先获取tag对象，查询tag_id，不存在为空，存储在保存id并且筛选所有状态正常的展示出来
# 没有就为空，如果tag_id为空，查询所有文章状态正常的展示，如果category_id不为空，展示所有分类正常状态文章
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    # 有标签文章返回标签文章，有分类文章返回分类文章，都没有返回最新文章
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    
    context = {
        'category': category,
        'tag': tag,
        
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    # 将get_navs中返回的字典添加到内容字典中
    context.update(Category.get_navs())        
    # 请求，模板名称，字典数据-传递到模板中
    return render(request, 'blog/list.html', context=context)




# 文章页view: 展示文章id
def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    
    context = {
        'post': post,
    }
    # update:把里面的字典的键/值对更新到字典中
    context.update(Category.get_navs())
    return render(request,'blog/detail.html', context=context)

