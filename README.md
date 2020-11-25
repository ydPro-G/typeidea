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



### 编写正式view代码：把数据从数据库中取出来并放到模板中展示
1. post_list逻辑：使用Model从数据库批量拿取数据，然后展示标题和摘要
2. post_detail逻辑：使用Model从数据库批量拿取数据，然后展示
3. 编写模板数据：根据view传递的数据,使用模板语法展示数据
4. 注意外键内容的获取，每一次每一条记录请求都需要对应数据库的来获取外键，导致一次文章列表页查询产生N次相关查询
5. 博客首页，博文详情页都简单展示了



### 配置页面通用数据
1. 完善模板信息：根据html5标准组织页面
    + 增加不同页面的信息展示：post_list
2. 重构post_list视图
    + 将通过tag_id拿到文章列表和tag对象抽出去作为独立函数
    + 将通过category_id拿到文章分类和文章对象抽出去作为独立函数
    + 先修改model层post模型定义:使用 select_related() 和 prefetch_related() 可以很好的减少数据库请求的次数，从而提高性能
3. 分类信息：model->view->html
    + **[在model层中添加函数get_navs---获取所有状态正常的数据，一个变量存is_nav为true的数据，一个存置顶false的数据，返回这两个数据]**(typeidea_item\typeidea\blog\models.py)
    + **在views.py中获取这个函数返回的两个字典数据，添加到context中**
    + **在模板中获取views中的这两个数据，并添加新的html代码，来展示这两个数据**
    + 这个函数会产生两次数据库查询操作，可以使用if来判断让其只产生一次查询，但并非绝对
4. 侧边栏配置：model->view->html
    + 1. [在model层新增类函数get_all获取侧边栏信息](typeidea_item\typeidea\config\models.py)
    + 2. 在view中将model中返回的数据添加到context中
    + 3. 在模板中添加相应字段,展示数据


### 封装侧边栏逻辑
#### 目标:1.把复杂逻辑封装，在模板中只用sidebar.content 2.调整Post模型，添加获取最热文章逻辑

1. 调整模型
    + 增加Post字段：pv,uv, 在model模型增加字段别忘了迁移(py manage.py makemigrations   py manage.py migrate)
    + [增加方法展示最新，最热文章hot_posts](typeidea_item\typeidea\blog\models.py)
    + 使用only只展示title和id字段
2. 封装好SideBar
    + 把数据的获取封装到Model层，在model层渲染数据，return渲染好的数据
    + 定义单独的模板bolck渲染SideBar数据
    + 编写两个模板代码


### 整理模板代码：抽象出基础模板，通过基类方法实现；去掉模板不合适的硬编码(对扩展开放，对修改关闭)
1. 抽象基础模板:通用的抽象出来做成类
    + 两个类
    + [block title:页面标题](typeidea_item\typeidea\typeidea\templates\blog\list.html)
    + [block main：页面主内容](typeidea_item\typeidea\typeidea\templates\blog\detail.html)

2. 解耦硬编码：在逻辑运算中使用更加语义化变量来取代毫无意义的数字或url
    + 定义URL时加上name参数，reverse通过name反向解析成URL
    + 修改urls.py参数


## 将函数视图升级为class-based view
**使用class-based view 重构 function view**

### 1.函数与类
1. 什么时候使用函数？什么时候封装出一个类呢？
只要代码逻辑被重复使用，有需要共享的数据，就可以考虑封装出一个类。

### 2.理解class-based-view
**view是一个接受请求并且返回响应的可调用对象**

1. view：基础的view，实现了基于HTTP方法的分发逻辑，get请求调用响应的get方法，但是他自己没有实现具体的get方法

2. `TemplateView`：继承自View，直接用来返回指定的模板，实现了get方法，可以传递变量到模板中来进行数据展示

3. DetailView：继承自View，实现了get方法，并且可以绑定某一模板，获取一条数据

4. ListView：继承自View，实现了get方法，绑定模板获取多条数据

5. 好处：解耦了HTTP GET/POST/OTHER 请求，如果需要增加处理post请求的逻辑，可以不用修改原来的函数，只需要新增函数 def post（self,request）即可，不用动之前的逻辑

6. **使用了class-based view，那么url的定义通过as_view**
通过as_viwe函数来接受请求以及返回响应。

7. **定义PostDetailView**，代替post_detail函数，修改模板代码，**修改url**，从url指定要匹配的参数来作为过滤post数据的参数（Post.objects.filter(pk=pk)）,拿到指定文章的实例

8. 对于单个数据的请求，django已经帮我们封装好了数据获取的逻辑


#### DetailView提供的属性和接口： 获取一条数据
1. model属性：指定当前View要使用的Model
2. queryset属性：跟model一样，二选一，设定基础的数据集，model设定没有过滤功能，通过 `queryset = Post.objects.filter(status=Post.Status_normal)`进行过滤
3. template_name属性：模板名称
4. get_queryset接口：获取数据，如果设置queryset，直接返回queryset
5. get_object接口：根据URl参数，从queryset上获取对应的实例
6. get_context_data接口：获取渲染到模板中的所有上下文

#### ListView：获取多条数据，数据量过大可以选择分页
1. 编写ListView--列表页



### 3.改造代码：将已存在的function view的代码重构为class-based view
function view和class-based view的差别，说白了就是函数和类的区别

1. 改造post_list和post_detail
    + post_list处理多个url逻辑，改造为class-based view后，可以通过继承的方式来复用代码
    + [将通用数据写成基类，分类导航，侧边栏，底部导航栏等](typeidea_item\typeidea\blog\views.py)

    + queryset中数据根据当前选择的分类或者标签进行过滤
    + 渲染到模板的数据加上当前选择的分类的数据
    + 重写get_context_data,将get_context_data传入模板
    + 重写get_queryset方法，获取指定的Model或queryset数据

2. [编写首页，分类，标签页view](typeidea_item\typeidea\blog\views.py)

3. [编写文章详情页view](typeidea_item\typeidea\blog\views.py)

4. 编写URl代码

5. 在list.html增加分页逻辑



### Django的view如何处理请求
**总结**：
分别编写了function view 和 class-based view(blog/views.py).
定义url，将请求转发到对应的view上.
知道如何在view中获取数据，操作Model层拿到数据，渲染模板然后返回.

1. function view & class-based view 两种方式处理请求的差别：
    + request经过所有的middleware的process_request方法做校验——>然后解析URL——>根据配置的URL和View的映射——>把request对象传递到View

    + 👆View有两类，function view or class-based view

    + function view：简单函数——>流程就是函数的执行流程，只是第一个参数是request对象

2. class-based viwe 处理流程
    + as_view逻辑：返回一个闭包——>闭包会在Django解析完请求后调用
        + 闭包的逻辑：
            + 给class（定义的view类）赋值--request，args，和kwargs
            + 根据HTTP方法分发请求
    
    + 请求到达后的完整逻辑
        1. 调用dispatch分发
        2. 接着调用GET方法
            1. 在GET请求中，首先调用get_queryset方法，拿到数据源
            2. 接着调用get_context_data方法，拿到了需要渲染到模板中的数据
                + 1)在get_context_data中，首先调用get_paginate_by拿到每页数据
                + 2)接着调用get_context_object_name拿到要渲染到模板中的这个quertset名称
                + 3)然后调用paginate_queryset进行分页处理
                + 4)最后拿到的数据转为dict并返回
            3. 调用render_to_response渲染数据到页面
                + 1)在render——to_response中调用get_template_names拿到模板名
                + 2)然后把request，context，template_name等传递到模板中



## 美化界面：前端样式框架Bootstrap


### 框架提供的功能
1. 页面脚手架：样式重置，浏览器兼容，栅格系统和简单布局
2. 基础的css样式：代码高亮，排版，表单，表格和小的样式效果
3. 组件：tab，pill,导航，弹窗，顶部栏等
4. JavaScript插件：一些动态功能，下拉菜单，进度条等

### 容器和栅格系统
1. 容器：<div>
2. 栅格：页面划分


### 简单的页面布局
1. container:提供容器，所有其他元素需在此容器中
2. navbar:导航栏组件，配置导航信息
3. jumbotron：大块内容展示重要信息
4. row和col-?:排列行和列
5. card: 卡片组件以卡片方式组织内容的展示

### 基于Bootstrap美化页面
1. 增加themes目录 在settings同级目录中增加themes/default目录
2. 把templates移动到这个目录下
3. 修改settings中的配置目录
    + 在在DIRS中新增了Django模板查找路径，找不到模板情况下去各个APP查找，因为我们上面设置了'APP_DIRS'：True,如果要新建主题，只需要修改THEME=‘default’即可.新建主题bootstrap==THEME=‘bootstrap’
4. 修改模板：新增**bootstrap**主题
5. 编写bootstrap/base.html
6. 编写bootstarp/list.html
7. 编写bootstarp/detail.html

#### 模板页面extends和block的用法：在导航页面只使用block，具体block里的逻辑在非导航页面编写，非导航页面使用extends 来引入父模板路径
1. extends 引入父模板路径[{% extends "./base.html" %}]
2. block 
    + [在导航页面需要被替换的地方使用{% block name %} {% endblock %}  52行](typeidea_item\typeidea\typeidea\themes\bootstrap\templates\blog\base.html)
    + 在非导航页面编辑具体逻辑



