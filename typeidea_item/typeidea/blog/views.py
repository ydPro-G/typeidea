from django.shortcuts import render
from django.http import HttpResponse 
from django.views.generic import DetailView,ListView
from django.shortcuts import get_object_or_404

from .models import Post,Tag,Category
from config.models import SideBar
from .models import Post, Category,Tag
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



# 通用数据：分类导航，侧边栏和底部导航，这些是基础数据，写成一个类。通过组合方式复用
class CommonViewMixin:
    # 使用**kwargs定义参数时，kwargs将会接收一个positional argument后所有关键词参数的字典。
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context

# 列表页类函数，一页5个
class IndexView(ListView):
    queryset = Post.latest_posts() #最新帖子
    paginate_by = 5  # 一页5个
    context_object_name = 'post_list' # 如果不设置此项，在模板中需要使用object_list变量
    template_name = 'blog/list.html'

# 分类函数
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        # pk
        category = get_object_or_404(Category, pk = category_id)
        context.update({
            'category': category
        })
