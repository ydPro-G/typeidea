from rest_framework import serializers, pagination # 前后端分离框架

from .models import Post, Category, Tag

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

    # url = serializers.HyperlinkedIdentityField(view_name='api-post-detail')

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
    
# 分类详情页接口
class CategoryDetailSerializer(CategorySerializer):
    # serializerMethodField把posts字段获取的内容映射到paginated_posts方法上
    posts = serializers.SerializerMethodField('paginated_posts')

    # 实现对某个分类下文章列表的获取和分页，并最终返回分页信息
    def paginated_posts(self, obj):
        # posts对应的数据需要通过paginated_posts获取
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        # 分页,指定分页方式：当前几页，每页多少条
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': 
        self.context['request']})
        return {
            # 数字
            'count': posts.count(),
            # 详细信息
            'results': serializer.data,
            # 上一个分类
            'previous': paginator.get_previous_link(),
            # 下一个分类
            'next': paginator.get_next_link(),
        }
    
    # 
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'created_time', 'posts'
        )



# 标签接口
class Tagserializer(serializers.ModelSerializer):
      class Meta:
        model = Tag
        fields = (
            'id', 'name', 'created_time'
        )
    
# 继承标签接口，同时让标签接口也返回这个标签下所有文章资源
class TagDetailSerializer(Tagserializer):
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        # 分页,指定分页方式：当前几页，每页多少条
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True,context={'request':
        self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'created_time', 'posts'
        )