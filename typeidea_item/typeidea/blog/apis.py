from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer



# api_view():将View转换为API View的装饰器
# 可提供参数api_view(['GET', 'POST'])来限定请求类型
@api_view()
# 文章列表函数视图(function view)
def post_list(request):
    posts = Post.objects.filter(status=Post.STATUS_NORMAL)
    post_serializers = PostSerializer(posts, many=True)
    return Response(post_serializers.data)

# 文章列表类函数(class-based view)
# ListCreateAPIView，只需要提供queryset，配置好用来序列化的类serializer = PostSerializer 就可以实现数据列表页
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer