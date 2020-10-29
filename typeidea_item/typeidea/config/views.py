from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# 编写友链页URL对应视图函数

def links(request):
    return HttpResponse('links')
