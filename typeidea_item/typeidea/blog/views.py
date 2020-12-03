from datetime import date
from django.db.models import Q,F
from django.shortcuts import render
from django.http import HttpResponse 
from django.views.generic import DetailView,ListView
from django.shortcuts import get_object_or_404
from django.core.cache import cache # 缓存功能

from comment.forms import CommentForm
from comment.models import Comment
from .models import Post,Tag,Category
from config.models import SideBar
from .models import Post, Category,Tag

# Create your views here.
# 编写url对应的视图函数
# 编写列表页url对应视图函数----编写文章页url对应视图函数




# function view 现在被 class-based view 替代

# tag和post是多对多关系，所以先获取tag对象，查询tag_id，不存在为空，存储在保存id并且筛选所有状态正常的展示出来
# 没有就为空，如果tag_id为空，查询所有文章状态正常的展示，如果category_id不为空，展示所有分类正常状态文章
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None

#     # 有标签文章返回标签文章，有分类文章返回分类文章，都没有返回最新文章
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
    
#     context = {
#         'category': category,
#         'tag': tag,
        
#         'post_list': post_list,
#         'sidebars': SideBar.get_all(),
#     }
#     # 将get_navs中返回的字典添加到内容字典中
#     context.update(Category.get_navs())        
#     # 请求，模板名称，字典数据-传递到模板中
#     return render(request, 'blog/list.html', context=context)




# 文章页view: 展示文章id
# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
    
#     context = {
#         'post': post,
#     }
#     # update:把里面的字典的键/值对更新到字典中
#     context.update(Category.get_navs())
#     return render(request,'blog/detail.html', context=context)





# 通用数据：分类导航，侧边栏和底部导航，这些是基础数据，写成一个类。通过组合方式复用
class CommonViewMixin:
    # 使用**kwargs定义参数时，kwargs将会接收一个positional argument后所有关键词参数的字典。
    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        # update:把里面的字典的键/值对更新到字典中
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context

# 首页函数:决定首页展示什么
class IndexView(CommonViewMixin, ListView):
    # 展示侧边，分类
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)\
        .select_related('owner')\
        .select_related('category')
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

# 分类函数
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        # 指定要匹配的参数pk作为过滤Post数据的参数，从而产生Post.objects.filter(pk=pk)拿到指定文章的实例 
        # pk= id
        # get_object_or_404 是快捷方式，用来获取一个对象实例，获取到就返回实例对象，不存在抛出404错误
        category = get_object_or_404(Category, pk = category_id)
        context.update({
            'category': category,
        })
        return context
        
    # 重写queryset,根据分类过滤
    def get_queryset(self):
        """ 重写queryset，根据分类过滤 """
        queryset = super().get_queryset() # 调用父类方法，获取父类所有
        category_id = self.kwargs.get('category_id') # kwargs=关键字参数 根据分类关键字筛选
        return queryset.filter(category_id=category_id)
    
# 标签视图
class TagView(IndexView):
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) # 获取上下文所有关键字
        tag_id = self.kwargs.get('tag_id') # 获取tag_id
        tag = get_object_or_404(Tag, pk=tag_id) # id=tag_id
        context.update({ # 筛选显示tag
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据标签过滤"""
        queryset = super().get_queryset()
        # self.kwargs中的数据其实是从URL定义中拿到的
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

# 文章详情页，也展示评论
class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id' # url字段为post_id

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited() # 访问句柄
        return response

    # 统计pv，uv.判断有没有缓存，有+1，elif避免执行两次更新操作
    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        # cache获取
        if not cache.get(pv_key):
            increase_pv = True
            # cache设置，缓存时间为1分钟，超过一分钟就是删除缓存
            cache.set(pv_key, 1, 1*60)# 1分钟 有效
        
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60) # 24小时有效

        if increase_pv and increase_uv:
            # F；直接执行SQL语句，增加。优化ORM操作数据库
            # F表达式并不会马上从数据库中获取数据，而是在生成SQL语句的时候，动态的获取传给F表达式的值。
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1,
            uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)



    # 将评论传递到模板层,被comment/templatetags.comment_block.py代替
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # update:把里面的字典的键/值对更新到字典中
    #     context.update({
    #         'comment_form': CommentForm,
    #         'comment_list': Comment.get_by_target(self.request.path),
    #     })
    #     return context



# 搜索view
class SearchView(IndexView):
    def get_context_data(self):
        # get_context_data()可以用于给模板传递模型以外的内容或参数
        context = super().get_context_data()
        # update 更新数据keyword（搜索关键字字典）字典
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        # get_queryset()返回一个量身定制的对象列表,可以只获取自己想要的数据
        queryset = super().get_queryset() # 调用父类方法
        keyword = self.request.GET.get('keyword') # keyword搜索的关键字
        # 如果没有搜索返回所有，有搜索返回title或者desc
        if not keyword:
            return queryset
            # 返回自己想要的数据
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=
        keyword))


# 作者页面view
class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)



