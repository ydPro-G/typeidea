# typeidea

# 项目记录

## 后端开发 
### 1.奠定项目基石：Model---对数据库中字段的抽象
1. 创建虚拟环境，项目与配置,编写完model后还需要编写admin才能展示

2. 拆分settings适应不同的运行环境
    + __init__.py：引导模块
    + base.py：基础模块，之后需要创建不同的配置文件都是基于base.py(重复的抽象成基类，有特性的抽出来做子类也就是单独的配置文件。)
    + develop.py:子类，线下数据库配置文件

3. 编写Model层代码
    + 创建bolg-APP：每个APP都是自组织，紧耦合，内部所有逻辑都相关联的。
    + 在blog-APP中models.py中创建博客内容相关的模型：文章，标签，分类

    + 创建 config-APP
    + 编写config里model层代码：友链，链接

    + 创建comment-APP
    + 编写comment中的model层代码：评论

4. 配置INSTALLED_APPS:将bolg，config,comment放到settings配置中


5. 创建数据库（表）：
    + 创建数据库表：python manage.py makemigrations
    + 执行迁移操作：python manage.py migrate



### 2配置admin页面
####  通过继承admin.ModelAdmin,就能实现对这个Model的增删改查页面的配置
1. 创建blog的管理后台

2. [使用装饰器编写分类，标签，文章的admin配置](typeidea_item\typeidea\blog\admin.py)

3. [创建comment的配置文件](typeidea_item\typeidea\comment\admin.py)  

4. [创建config模型的admin配置文件](typeidea_item\typeidea\config\admin.py)

5. 根据需求定制blog的admin:1.数据批量展示和操作的列表页2.数据增加或修改的页面----问题(可以看到所有作者，右侧筛选器也可以看到所有分类)
    + 1.自定义列表筛选器（list_filter）——1.定义CategoryOwnerFilter:自定义过滤器只显示当前用户分类
    + 2.自定义列表页数据：重写get_quertset，让owner=request.user

6. 编辑页面的配置：按钮位置，填写字段，字段展示顺序，输入框样式
    + 按钮位置：save_on_top--控制是否在页面顶部展示按钮
    + 字段展示以及展示顺序：fields或fieldset配置
    + fields：限定要展示的字段，配置展示字段的顺序
    + fieldsets：控制页面布局
    + 字段不展示：exclude指定字段不展示   exclude = ('owner',) 作者字段不展示
    + classes:加css属性

7. 自定义静态资源引入
    + 自定义静态资源引入路径: class Media:css or js


### 3自定义模块
1. 自定义Form（表单）
    + Form的作用：Form是对用户输入以及Model中要展示数据的抽象

2. 在同一页面编辑关联数据：在分类页面直接编辑文章
    + 编写blog/admin.py---PostInline类

3. [定制site：一个系统对外提供多个admin后台](typeidea_item\typeidea\typeidea\custom_site.py)
    + 用户模块的管理与文章分类等数据的管理分开；修改后台的默认展示
    + 自定义site：将后台分为两个：super_admin(管理后台)    admin(用户后台)

### 4admin权限逻辑及SSO登录
1. 集成SSO(单点登录)
2. 判断某个用户是否由添加文章的权限：权限管理是在另外的系统上，只提供一个接口---有权限，响应状态为200，没权限则为403




### 5抽象author基类：将相同逻辑分散在不同模块的代码抽象为基类
1. [将逻辑相同的代码抽象成为基类](typeidea_item\typeidea\typeidea\base_admin.py)
2. 【BaseOwnerAdmin】继承admin文件admin.ModelAdmin类，并根据我们的需求改写其中的save_model,get_queryset方法
    + save_model:设置对象的owner
    + get_queryset: 让列表页在展示文章或分类是只展示当前用户数据
3. 将用到这两个方法APP中的类继承的父类更改为BaseOwnerAdmin




### 6.记录操作日志----LogEntry
1. 如果需要自定义变更记录，只需要传递对应的参数即可
2. LogEntry.objects.log_action方法参数：
    + user_id:当前用户id
    + content_type_id: 要保存内容的类型
    + object_id: 记录变更实例的id --比如PostAdmin它就是post.id
    + object_repr：实例的展示名称
    + action_flag:操作记录（更改or新增or删除）
    + change_message:记录的消息
3. 在admin页面配置数据，查看操作日志




## 前端页面开发
1. 目的：把后端创建的数据展示到前台
2. 技术：先使用function view来完成前台的编辑，最后演化到class-based view
3. 步骤：1-整理出需要多少url；2-分析页面上需要呈现的数据
4. 访问时的路径是根据url来的，但是返回的页面是views.py中的函数控制！！！！！！



### 分析URL和页面数据
1. 页面
    + 博客首页：https://www.gg.com/
    + 博文详情页: https://www.gg.com/post/<post_id>.html
    + 分类列表页: https://www.gg.com/category/<category_id>/
    + 标签列表页:https://www.gg.com/tag/<tag_id>/
    + 友链展示页:https://www.gg.com/links/
2. View
    + 列表页View：根据不同的查询条件分别展示博客首页，分类页，标签页
    + 文章页View：展示博文详情页
    + 友链页View：展示所有友情链接

### 编写URL代码：Url到View的数据映射
1. url(<传递给view function函数的参数>,<view function>,<默认传递参数，无论什么请求过来都会传递这个参数到view function中>,<url的名称>)
2. 在view编写相应的view function，处理<>内的参数
3. 使用render方法：结合一个给定的模板和一个给定的上下文字典, 并返回一个渲染后的HttpResponse对象
    + render(request,template_name, context=None, content_type=None,status=None, using=None)
    + request:封装了HTTP请求的request对象
    + template_name:模板名称，可以像前面的代码那样带上路径
    + context：字典数据，传递到模板上
    + content_type:页面编码类型，默认值是text/html
    + status：状态码，默认值是200
    + using：使用哪种模板引擎解析

### 编写模板：每个app各自创建模板or同一放到项目同名的APP中
1. [在主项目创建templates](typeidea_item\typeidea\typeidea\templates)
2. 在templates中创建app-blog and app-config
3. 在blog中创建两个模板
4. 去配置INSTALLED_APPS
5. 根据url设置然后看看view配置后的页面

