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
from blog.views import post_detail,post_list # 导入用来处理请求的view函数
from config.views import links

# 三个View post_list post_detail links
urlpatterns = [
    # url(<正则>,<view function>,<默认传递参数，无论什么请求过来都会传递这个参数到view function中>,<url的名称>)
    url(r'^$', post_list, name='index'),
    # view从url中<>内取值然后作为参数传递给后面的view函数，逗号后面是view中的函数名称，这样url和view可以对应起来
    # 通过这一逻辑我们可以处理不同的url匹配到同一参数的逻辑 /category/1 or post/2.html  后面的字段是对应的view函数， <>内的字段作为参数传递给函数处理
    url(r'^category/(?P<category_id>\d+)/$', post_list, name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', post_list, name='tag-list'),
    # post_id 1,2,3,4,5
    url(r'^post/(?P<post_id>\d+).html$', post_detail, name='post-detail'),
    url(r'^links/$', links, name='links'),
    url(r'^super_admin/', admin.site.urls, name='super-admin'),
    url(r'^admin/', custom_site.urls, name='admin'), 
]
