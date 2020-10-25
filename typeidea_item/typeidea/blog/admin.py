from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag

# Register your models here.
# Category,Post,Tag对应的admin配置    


# 注册装饰器
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # admin页面列表展示
    list_display = ('name','status','is_nav','created_time','post_count')
    # 添加需要显示的设置字段
    fields = ('name','status','is_nav')

    # save_model判断保存owner信息，保存数据到数据库
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




@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 列表页面展示字段
    list_display = [
        'title', 'category', 'status',
        'created_time','operator'
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

    fields = (
        ('category', 'title'),
        'desc',
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

    def save_model(self, request, obj, form, change):
        obj.owner = request.user 
        return super(PostAdmin, self).save_model(request, obj, form, change)

