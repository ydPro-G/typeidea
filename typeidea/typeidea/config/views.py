from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from config.models import Link
from blog.views import CommonViewMixin
# Create your views here.
# 编写友链页URL对应视图函数

class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL) # 状态正常友链
    template_name = 'config/links.html'
    context_object_name = 'link_list'

