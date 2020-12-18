from rest_framework import serializers # 前后端分离框架

from .models import Post

# 序列化，和ModelForm一样写法,前端需要反序列化
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'category', 'desc', 'content_html', 'created_time']