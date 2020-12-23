from rest_framework import serializers # 前后端分离框架

from .models import Post, Category

# 序列化的类,前端需要反序列化


# 文章列表接口
# ModelSerializer:1.自动生成字段2.默认实现create和update
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
        # 指明序列化器类对应的模型类
        model = Post
        # 指明一句模型类的哪些字段生成序列化器类的字段
        fields = ['id', 'title', 'category', 'tag', 'owner', 'created_time']

# 文章详情接口
class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content_html', 'created_time']





# 分类接口
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time',
        )
    


