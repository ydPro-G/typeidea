from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# 博客内容相关的模型

# 分类
class Category(models.Model):
    STATUS_NORMAL = 1 # 状态正常1
    STATUS_DELETE = 0 # 状态删除0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )

    name = models.CharField(max_length=50,verbose_name='名称')
    # choices一个元组 一般是下拉框，方便页面获取字典值
    # 默认正常，下拉列表显示状态栏
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    is_nav = models.BooleanField(default=False,verbose_name='是否为导航')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    # 每个model中都定义一个Meta类属性，作用是配置Model属性
    # 配置展示名称为分类
    class Meta:
        verbose_name = verbose_name_plural = '分类'
     
    # 动作返回self.name
    def __str__(self):
        return self.name

    

# 标签
class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )

    name = models.CharField(max_length=10,verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    # 外键
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

# 文章
class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
        (STATUS_DRAFT,'草稿'),
    )
    
    title = models.CharField(max_length=255,verbose_name='标题')
    desc = models.CharField(max_length=1024,blank=True,verbose_name='摘要')
    content = models.TextField(verbose_name='正文',help_text='正文必须为MarkDown格式')
    # 正整数类型，在HTML中表现为NumberInput或者TextInput标签
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    # foreignKey 外键
    category = models.ForeignKey(Category,verbose_name='分类')
    tag = models.ForeignKey(Tag,verbose_name='标签')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    
    # 每个model中都定义一个Meta类属性，作用是配置Model属性
    # 配置展示名称为文章，排序规则根据id降序排序
    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id'] # 根据id降序排列

