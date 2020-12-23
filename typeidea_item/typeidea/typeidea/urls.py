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
from django.contrib.sitemaps import views as sitemap_views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from rest_framework.documentation import include_docs_urls


from .custom_site import custom_site
from config.views import LinkListView
from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView, AuthorView,
)
from comment.views import CommentView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.apis import PostViewSet, CategoryViewSet
# from .autocomplete import CategoryAutocomplete, TagAutocomplete


router = DefaultRouter()
# 文章
router.register(r'post',PostViewSet,base_name='api-post')
# 分类
router.register(r'category', CategoryViewSet, base_name='api-category')


urlpatterns = [
    # url(<正则>,<view function>,<默认传递参数，无论什么请求过来都会传递这个参数到view function中>,<url的名称>)
    url(r'^$', IndexView.as_view(), name='index'),
    # view从url中<>内取值然后作为参数传递给后面的view函数，逗号后面是view中的函数名称，这样url和view可以对应起来
    # 通过这一逻辑我们可以处理不同的url匹配到同一参数的逻辑 /category/1 or post/2.html  后面的字段是对应的view函数， <>内的字段作为参数传递给函数处理
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    
    #   as_view() 只是个查询方法，根据?p<>里的字段查询 https://www.jianshu.com/p/17860becea09
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view() , name='post-detail'),
    url(r'^super_admin/', admin.site.urls, name='super-admin'),
    url(r'^admin/', custom_site.urls, name='admin'), 
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^link/$', LinkListView.as_view(), name='links'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    # RSS and sitemap
    url(r'^rss|feed', LatestPostFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    # 整个接口 router
    url(r'^api/', include(router.urls, namespace="api")),
    # 接口文档url
    url(r'^api/docs/', include_docs_urls(title='typeidea apis')),
    










    # 接受文件接口
    # url(r'^ckeditor/', include('ckeditor_uploader.urls')),
     
    # url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(),name='category-autocomplete'),
    # url(r'^tag-autocomplete/$', TagAutocomplete.as_view(),name='tag-autocomplete'),

]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 配置图片资源访问
