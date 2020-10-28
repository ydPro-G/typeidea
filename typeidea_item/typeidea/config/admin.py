from django.contrib import admin

from .models import Link, SideBar
from typeidea.base_admin import BaseOwnerAdmin

# Register your models here.
# 友链，侧栏admin配置文件

@admin.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    """ 因为给每个model定义了一个owner，但是admin里没有owner的配置选项，所以设置一个save_model
     保存数据之前，把owner这个字段设定为当前的登录用户，未登录的request.user拿到的匿名用户对象
     obj：当前要保存的对象 form页面提交过来的表单之后的对象 change:标志本次保存的数据是新增还是更新
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)
    """
    
    
@admin.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')