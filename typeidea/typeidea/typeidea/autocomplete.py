from dal import autocomplete # 自动补全插件

from blog.models import Category, Tag

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    # get_queryset处理数据源
    def get_queryset(self):
        # is_authenticated() 判断用户是否登录，未登录用户返回空的queryset
        if not self.request.user.is_authenticated():
            return Category.objects.none()

        # 获取用户创建的分类或标签
        qs = Category.objects.filter(owner=self.request.user)

        # 判断是否存在self.q q == url参数传过来的值
        if self.q:
            # 使用name_istartswith进行查询
            qs = qs.filter(name__istartswith=self.q)
        return qs

class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()
        
        qs = Tag.objects.filter(owner=self.request.user)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs