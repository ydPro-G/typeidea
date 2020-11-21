"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


from .custom_site import custom_site
from config.views import links
from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView,
)


# 三个View post_list post_detail links
urlpatterns = [
    # url(<正则>,<view function>,<默认传递参数，无论什么请求过来都会传递这个参数到view function中>,<url的名称>)
    url(r'^$', IndexView.as_view(), name='index'),
    # view从url中<>内取值然后作为参数传递给后面的view函数，逗号后面是view中的函数名称，这样url和view可以对应起来
    # 通过这一逻辑我们可以处理不同的url匹配到同一参数的逻辑 /category/1 or post/2.html  后面的字段是对应的view函数， <>内的字段作为参数传递给函数处理
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    
    # 指定要匹配的参数pk作为过滤Post数据的参数，从而产生Post.objects.filter(pk=pk)拿到指定文章的实例 
    #   as_view() 只是个查询方法，根据?p<>里的字段查询 https://www.jianshu.com/p/17860becea09
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view() , name='post-detail'),
    url(r'^links/$', links, name='links'),
    url(r'^super_admin/', admin.site.urls, name='super-admin'),
    url(r'^admin/', custom_site.urls, name='admin'), 
]
