from django.contrib.auth.models import User # 引入内置user模型
from django.db import models

# Create your models here.

#配置：友链，侧边栏

class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )
    title = models.CharField(max_length=50,verbose_name='标题')
    href = models.URLField(verbose_name='链接') # 默认长度为200
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    weight = models.PositiveIntegerField(default=1,choices=zip(range(1,6),range(1,6)),verbose_name='权重',help_text='权重高展示顺序靠前')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    
    # 每个model中都定义一个Meta类属性，作用是配置Model属性
    # 配置展示名称为文章，排序规则根据id降序排序
    class Meta:
        verbose_name = verbose_name_plural = '友链'

    def __str__(self):
        return self.name

class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW,'展示'),
        (STATUS_HIDE,'隐藏'),
    )
    SIDE_TYPE = (
        (1,'HTML'),
        (2,'最新文章'),
        (3,'最热文章'),
        (4,'最近评论'),
    )
    title = models.CharField(max_length=50,verbose_name='标题')
    display_type = models.PositiveIntegerField(default=1,choices=SIDE_TYPE,verbose_name='展示类型')
    content = models.CharField(max_length=500,blank=True,verbose_name='内容',help_text='如果设置的不是HTML类型，可为空')
    status = models.PositiveIntegerField(default=STATUS_SHOW,choices=STATUS_ITEMS,verbose_name='状态')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'
    
    # 侧边栏展示title
    def __str__(self):
        return self.title


