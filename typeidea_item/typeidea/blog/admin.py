from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag

# Register your models here.
# Category,Post,Tag对应的admin配置    


# 通过装饰器注册模型
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # admin页面列表展示
    list_display = ('name','status','is_nav','created_time','post_count')
    # 添加需要显示的设置字段
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




@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)

# 自定义过滤器，只显示当前用户分类
class CategoryOwnerFilter(admin.SimpleListFilter): # 继承admin模块SimplListFilter类来实现自定义过滤器
    """自定义筛选器只显示当前用户分类"""

    # 显示标题
    title = '分类过滤器'
    #查询时URL参数的名字 查询id为1，?owner_category=1
    parameter_name = 'owner_category'
    
    # 返回要展示的内容和查询用的id
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.owner).values_list('id'm 'name')
    
    # 根据URL Query的内容返回列表页的数据
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset







@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 列表页面展示字段
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]

    # 配置可作为链接的字段
    list_display_links = []

    # 配置列表筛选字段
    list_filter = ['category', ]
    # 配置搜索字段
    search_fields = ['title','category_name']

    # 是否展示在顶部
    actions_on_top = True
    # 是否展示在底部
    actions_on_bottom = True

    # 保存，编辑，编辑并新建按钮是否在顶部展示
    save_on_top = True

    # 添加页面显示的字段
    fields = (
        ('category', 'title'),# category title 一行
        'desc', # desc 一行
        'status',
        'content',
        'tag',
    )

    # 自定义方法
    def operator(self, obj):
        # 返回经过format_html函数处理
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change',args=(obj.id,)) # 根据名称解析处URL地址
        )
    operator.short_description = '操作' # 展示文案

    # 默认保存登录作者信息
    def save_model(self, request, obj, form, change):
        obj.owner = request.user 
        return super(PostAdmin, self).save_model(request, obj, form, change)
