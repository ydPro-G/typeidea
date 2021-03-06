from django.contrib.auth.models import User
from django.db import models
import mistune
from django.utils.functional import cached_property
from django.core.cache import cache

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
    
    # 获取所有状态正常的数据，一个变量存is_nav为true的数据，一个存置顶false的数据，返回这两个数据
    # 产生两次数据库请求，可以使用if语句判断，节省I/O操作，但并非绝对
    @classmethod
    def get_navs(cls):
        # 因QuertSet懒特性，第一个filter函数在被调用是不产生数据库访问，因为返回对象未被使用
        categorites = cls.objects.filter(status=cls.STATUS_NORMAL)
        # 产生一次数据库查询， I/O操作，因为被使用
        nav_categories = categorites.filter(is_nav=True)
        # 产生第二次数据库查询， I/O操作 ， 因为被使用
        normal_categories = categorites.filter(is_nav=False)
        return {
            # 两个都被使用，分别产生自己的查询语句， 对系统来说就是两次I/O操作
            'navs': nav_categories,
            'categories': normal_categories,
        }
'''
    使用if来让其只查询数据库一次，只产生一次I/O操作
    @classmethod
    def get_navs(cls):
        catefories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in catefories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
    
        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }
'''
    

# 标签
class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )
    # PositiveIntegerField 自增主键，只包含正整数 默认值为1


    name = models.CharField(max_length=10,verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    # 外键
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name

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
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    
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
    # 存储markdown处理后的内容，允许有空白，但是不允许编辑
    content_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)
    # is_top = models.BooleanField(default=True,verbose_name="置顶")
    # topped_expired_time = models.DateTimeField(verbose_name="置顶失效时间")


    # 模型的元数据，指的是“除了字段外的所有内容”，例如排序方式、数据库表名、人类可读的单数或者复数名等等。
    # 配置展示名称为文章，排序规则根据id降序排序
    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id'] # 根据id降序排列
    
    # 在model层定义的接口，返回有标签的状态正常的文章
    @staticmethod
    def get_by_tag(tag_id):
        try:
            # 获取tag信息
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag=None
            post_list = []
        else:
            # 获取post_list信息
            # 对于一对一字段（OneToOneField）和外键字段（ForeignKey），可以使用select_related 来对QuerySet进行优化。
            # 标签下所有状态正常的文章,使用select_related查询，减少数据库请求次数
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')

        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            # 获取category信息
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category=None
            post_list = []
        else:
            # 获取post_list信息
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner','category')
                # 返回信息
        return post_list, category
    
    # 接口，返回最新帖子，cls指的是这个类本身   with_related:控制返回数据是否加上外键数据
    @classmethod
    def latest_posts(cls, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        if with_related:
            queryset = queryset.select_related('owner', 'category')
        return queryset
    
    # 第一种业务
    @classmethod
    def get_topped_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL, is_top=True)



    # 返回最热帖子,按照访问量排序
    # 增加cache，10分钟缓存
    @classmethod
    def hot_posts(cls):
        result = cache.get('hot_posts')
        if not result:
            # 使用only接口只展示title和id
            result = cls.objects.filter(status=cls.STATUS_NORMAL).only('title', 'id').order_by('-pv')
            cache.set('hot_posts', result, 10 * 60)
        return result
        
        # return cls.objects.all(status=STATUS_NORMAL).only('title', 'id').order_by('-pv')
        # return cls.objects.filter(status=STATUS_NORMAL).order_by('-pv')
    



    # 把返回的数据绑到实例上,values_list使用不了暂时隐藏
    # @cached_property 
    # def tags(self):
    #     return ','.join(self.tag.values_list('name', flat=True))
    
    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save(*args, **kwargs)



# 置顶表model
# class ToppedPosts(models.Model):
#     title = models.CharField(max_length=255, verbose_name="置顶")
#     post_id = models.PositiveIntegerField(verbose_name="关联文章ID")