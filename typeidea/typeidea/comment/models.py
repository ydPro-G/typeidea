from django.db import models

from blog.models import Post

# Create your models here.
# 评论模型
class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )
    target = models.CharField(max_length=100, verbose_name='评论目标')
    content = models.CharField(max_length=2000,verbose_name='内容')
    nickname = models.CharField(max_length=50,verbose_name='昵称')
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    # 每个model中都定义一个Meta类属性，作用是配置Model属性
    class Meta:
        verbose_name = verbose_name_plural = '评论'
    
    def __str__(self):
        return self.target
    
    # 在model层定义的接口，cls指这个类本身，返回状态正常的target
    @classmethod
    def get_by_target(cls,target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)


