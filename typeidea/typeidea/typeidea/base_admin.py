# 抽象一个基类-----1.重写save方法(设置对象的owner)------2.重写get_queryset方法(让列表页在展示文章或分类是只能展示当前用户的数据)
from django.contrib import admin

# 继承admin.ModelAdmin,修改父类中的save_model和get_queryset方法
class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. save_model 用来自动补充文章，分类，标签，侧边栏，友链这些Model的owner字段
    2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner', )

    # 自定义列表页数据，让当前登录用户只能在列表页看到自己创建的文章，返回当前用户的查询集
    def get_queryset(self, request):
        # super 调用父类的方法  super(type[, object-or-type]) type --类  object-or-type -- 类，一般是self
        qs = super(BaseOwnerAdmin,self).get_queryset(request)
        # 返回过滤器中的作者信息时当前登录用户信息
        return qs.filter(owner=request.user)

    # 默认保存登录作者信息
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)



  #  def get_queryset(self, request):
    #     """
    #     返回管理站点可编辑的所有模型实例查询集，由变更列表视图使用
    #     Return a QuerySet of all model instances that can be edited by the
    #     admin site. This is used by changelist_view.
    #     """
    #     qs = self.model._default_manager.get_queryset()
    #     T: this should be handled by some parameter to the ChangeList.
    #     ordering = self.get_ordering(request)
    #     if ordering:
    #         qs = qs.order_by(*ordering)
    #     return qs