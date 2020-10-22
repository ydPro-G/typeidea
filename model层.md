# 详细讲解Model层

## ORM基本概念
1. ORM(对象关系映射)：将定义的对象(类)映射到对应数据库的表上
2. Django的Model就是ORM的具体实现
3. model中定义的属性对应一个表的字段；类中的属性对应MySQL中的字段；属性的类型对应MySQL字段的类型；属性定义时传递的参数定义了字段的其他属性
4. 对于有choices的字段，在admin后台，Django会提供一个下拉列表让用户选择，而不是填写。
  

##  常用类型字段
### 数值型
1. AutoField int(11):自增主键
2. BooleanField tinyint(1):布尔类型字段，一般用于记录状态标记
3. DecimalField decimal:开发对数据精度要求较高的业务时考虑使用，支付，金融
4. IntegerField int(11):同AutoField一样，唯一差别就是不自增
5. PositiveIntegerField:同IntergerField，只包含正整数
6. SmallIntegerField smallint 小整数时一般会用到
### 字符型：对应MySQL有两种类型：longtext,varchar
1. CharField varchar:基础的varchar类型
2. URLField:继承CharField,但是实现了对URL的特殊处理
3. UUIDField char(32)：除了在PostgreSQL中使用uuid类型外，其他数据库都是用char(32，用来存放生成的唯一id)
4. FileFiled:继承charfield，多了对文件的特殊处理，当定义一个字段为FileField时，在admin页面生成一个可上传文件的按钮
5. TextField longtext:存放大量文本内容
### 日期类型：date，datetime,time
1. DateField
2. DateTimeField
3. TimeField
### 关系类型：关联两个表
1. ForeignKey(外键) 
2. OneToOneField(一对一)
3. ManyToManyField(多对多) 创建一个中间表，进行多对多关联



### 参数：参数就是python中的类，这些参数是类在实例化时传递的
1. null：数据库层面该值是否允许为空
2. blank：业务层面该值是否允许为空
3. choices：在admin页面可以看到看到对应的可选项展示
4. db_column:指定model中某个字段对应数据库中的那个字段
5. db_index: 索引配置，业务上经常作为查询条件的字段配置
6. default：默认值配置
7. editable：是否可编辑，默认为True
8. error_messages: 自定义字段值校验失败是的异常提示，字典格式
9. help_text：字段提示语
10. primary_key：主键，一个model只允许设置一个字段为primary_key
11. unique:唯一约束，唯一值
12. unique_for_date：针对date(日期)的联合约束
13. unique_for_month:针对月份的联合约束
14. unique_for_year:针对年份的联合约束
15. verbose_name:字段的展示文案
16. validators：自定义校验逻辑


## Model层：QuerySet使用
### 理解model层如何提供数据：
1. Django通过给Model增加一个objects属性来提供数据操作接口
2. 当我们用到这个数据时，它会去DB中获取数据，如果不用这个数据，那么只会返回一个QuerySet对象，等你真正用它时才会执行查询
3. posts = Post.object.all() # 返回一个QuerySet对象并赋值给Posts
4. available_posts = posts.filter(status=1) # 继续返回一个QuerySet对象并赋值给available_posts
5. print(available_posts) # 此时会根据上面的两个条件执行数据查询操作，对应的SQL为：SELETE * FROM BLOG_POST WHERE STARTUS =1;
### QuerySet概念
1. QuerySet本质上时一个懒加载对象，只有真正用到时才会执行查询

### 常用QuerySet接口-支持链式调用的接口
支持链式调用的接口即返回QuerySet的接口
1. all接口：查询所有数据
2. filter接口：根据条件过滤数据，常用的条件基本上是字段等于，不等于，大于，小于
3. exclude接口：同filter，只是相反的逻辑
4. reverse： 把QuerySet中的结果倒序排列
5. distinct接口：用来进行去重查询
6. none接口，返回空的QuerySet
---------------------------------------
### 不支持链式调用的接口
不支持链式调用的接口即返回值不是QuerySet的接口
1. get接口：post.objects.get(id=1):查询id为1的文章，存在返回post实例，不存在抛出DoesNotExist异常
2. create接口：创建一个model对象
3. get_or_create：根据条件查询，如果没查询到就创建
4. update_or_create: 同get_or_create,知识用来做更新操作
5. count接口：用来返回QuerySet有多少条记录
6. latest:返回最新的一条记录
7. earliest：返回最早的一条记录
8. first：从当前QuerySet记录获取第一条
9. last: 同上，最后一条
10. exists：返回True或False，只需要判断QuerySet是否有数据用这个接口合适，因为会减少一次DB查询请求
11. bulk_create：同create，批量创建记录
12. in_bulk：批量查询，返回字典类型
13. update：根据条件批量更新记录——Post.objects.filter(owner_name='dd'.update(title='测试更新'))
14. delete: 同update，根据条件批量删除记录
15. values：明确知道只需要返回莫格字段的值
16. values_list：同values，但直接返回的是包含tuple的QuerySet
### 进阶接口
1. defer：把不需要展示的字段做延迟加载
2. only：同defer接口相反：只获取title内容，其他值在获取时会产生额外的查询
3. select_related：解决外键N+1问题的方案
4. prefetch_related：针对多对多关系的数据，通过这个接口避免N+1查询


## 常用字段查询：
1. contains：包含
2. icontains：同contains,只是忽略大小写
3. exact：精确匹配
4. iexact：忽略大小写精确匹配
5. in：指定某个集合
6. gt：大于某个值
7. gte：大于等于
8. lt：小于
9. lte：小于等于
10. startswith：以某个字符串开头，与contains类似
11. istartswith：同startswith，忽略大小写
12. endswith：以某个字符串结尾
13. iendswith：以某个字符串结尾，忽略大小写
14. range：范围查询，多用于时间范围

### 进阶查询
1. F
2. count:聚合查询
3. Sum:合计


