from rest_framework import serializers # 前后端分离框架

from .models import Post

# 序列化的类,前端需要反序列化
# 文章列表接口需要的Serializer
class PostSerializer(serializers.ModelSerializer):
    # SlugRelatedField:定义外键数据是否可写（read_only参数）
    # slug_field指定用来展示的参数
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    tag = serializers.SlugRelatedField(
        # many=True  多对多
        # many=True, # 设置后表示有多个标签，但是设置后会报错--'Tag' object is not iterable
        read_only=True,
        slug_field='name'
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Post
        # 在页面展示的字段
        fields = ['id', 'title', 'category', 'tag', 'owner', 'created_time']

    

# 定义详情接口需要的serializer类
class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content_html', 'created_time']


