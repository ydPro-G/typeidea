from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site # 引入typeidea文件的custom_site文件和类

# Register your models here.
# Category,Post,Tag对应的admin配置    

# 在分类页面增加一个编辑/新增文章的按钮
class PostInline(admin.TabularInline): # StackedInline 样式不同
    fields = ('title', 'desc')
    extra = 1 # 控制额外多几个
    model = Post


# 通过装饰器注册模型
@admin.register(Category, site = custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # 添加一行
    inlines = [PostInline, ]
    # admin页面列表展示
    list_display = ('name','status','is_nav','created_time','post_count')
    # 限定要展示的字段，配置展示字段的顺序
    fields = ('name','status','is_nav')

    # 保存数据之前，把owner这个字段设定为当前的登录用户，未登录的request.user拿到的匿名用户对象
    # obj：当前要保存的对象 form页面提交过来的表单之后的对象 change:标志本次保存的数据是新增还是更新
    def save_model(self, request, obj, form, change):
        # 给obj.owner赋值，自动设置owner，request.user就是当前已登录的用户
        # 如果是未登录的用户通过request.user拿到的是匿名用户对象
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request, obj, form, change)

    # 自定义函数：展示该分类下有多少文章
    def post_count(self, obj):
        return obj.post_set.count()

    # 展示文案
    post_count.short_description = '文章数量'




@admin.register(Tag, site = custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')



# 自定义过滤器，只显示当前用户分类
class CategoryOwnerFilter(admin.SimpleListFilter): # 继承admin模块SimplListFilter类来实现自定义过滤器
    """自定义筛选器只显示当前用户分类"""

    # 显示标题
    title = '分类过滤器'
    #查询时URL参数的名字 查询id为1，?owner_category=1
    parameter_name = 'owner_category'
    
    # 返回要展示的内容和查询用的id
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
    
    # 根据URL Query的内容返回列表页的数据,举例-最后Query是？owner_category=1,那么这里拿到的self.value()就是1，根据1来过滤QuerySet
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset







# 将site更换为我们自定义的site
@admin.register(Post, site = custom_site) 
class PostAdmin(BaseOwnerAdmin):
    #  自定义Form，修改status的输入框为文本框(Textarea)
    form = PostAdminForm
    # 列表页面展示字段
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]

    # 配置可作为链接的字段
    list_display_links = []

    # 配置列表筛选字段,设置侧边栏过滤器只能看到自己创建的分类
    list_filter = [CategoryOwnerFilter]
    # 配置搜索字段
    search_fields = ['title','category_name']

    # 是否展示在顶部
    actions_on_top = True
    # 是否展示在底部
    actions_on_bottom = True

    # 保存，编辑，编辑并新建按钮是否在顶部展示
    save_on_top = True

    """ 添加页面显示的字段
    fields = (
        ('category', 'title'),# category title 一行
        'desc', # desc 一行
        'status',
        'content',
        'tag',
    )
    """
    fieldsets = (
        ('基础配置',{
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('wide',),
            'fields': ('tag',),
        })
    )



    # 自定义方法
    def operator(self, obj):
        # 返回经过format_html函数处理
        return format_html(
            '<a href="{}">编辑</a>',
            # 用reverse方式获取后台地址时，将admin更换为cus_admin
            reverse('cus_admin:blog_post_change', args=(obj.id,)) # 根据名称解析处URL地址
        )
    operator.short_description = '操作' # 展示文案


    # 静态资源引入
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)

# 在admin页面查看操作日志
@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']



