# from rest_framework import generics
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# from .models import Post
# from .serializers import PostSerializer



# # api_view():将View转换为API View的装饰器
# # 可提供参数api_view(['GET', 'POST'])来限定请求类型
# @api_view()
# # 文章列表函数视图(function view)
# def post_list(request):
#     posts = Post.objects.filter(status=Post.STATUS_NORMAL)
#     post_serializers = PostSerializer(posts, many=True)
#     return Response(post_serializers.data)

# # 文章列表类函数(class-based view)
# # ListCreateAPIView，只需要提供queryset，配置好用来序列化的类serializer = PostSerializer 就可以实现数据列表页
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
#     serializer_class = PostSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Post, Category, Tag
from .serializers import (
    PostSerializer,PostDetailSerializer,
    CategorySerializer, CategoryDetailSerializer, Tagserializer, TagDetailSerializer
)

# 文章列表class-based view
class PostViewSet(viewsets.ModelViewSet):
    """提供文章接口"""
    # 指定序列化的类，这个类数据集是正常的文章
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    # permission_classes = [IsAdminUser]  # 用来做数据写入时(POST,PUT,DELETE操作)的权限校验

    # 文章详情view
    # 单个*的args是一个元组，两个*的kwargs是一个字典，，参数的数量都是任意
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    # 通过PostViewSet上的URL的query获取category参数
    def filter_queryset(self,queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
        
        # 获取tag
        tag_id = self.request.query_params.get('tag')
        if tag_id:
            queryset = queryset.filter(tag_id=tag_id)

        return queryset
    

# 分类视图
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    # 指定序列化的类，# CategorySerializer返回简单数据  CategoryDetailSerializer返回分类下的文章数据
    serializer_class = CategoryDetailSerializer
    # 指定数据集是状态正常分类
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    # 获取分类的详细信息view
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)


# 标签视图
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    # Tagserializer返回简单数据 TagDetailSerializer返回标签下的文章数据
    serializer_class = TagDetailSerializer
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)

    # # 在retrieve方法中重新设置serializer_class的值，达到不同接口使用不同serializer的目的
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TagDetailSerializer
        return super().retrieve(request, *args, **kwargs)



    

 
