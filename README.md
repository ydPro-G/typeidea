# typeidea

# 第一部分：初入江湖

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
4. **访问时的路径是根据url来的，但是返回的页面是views.py中的函数控制！！！！！！****



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


### middleware完整接口：Django的middleware在项目启动时会被初始化接受请求后根据settings中的MIDDLEWARE配置顺序挨个调用，传递request做参数
1. process_request:请求来到middleware中时进入的第一个方法，可以在这里做校验，有两个返回值HttpResponse or None，返回HttpResponse就返回了，返回None执行其他方法

2. process_view:在process_request之后执行，统计view相关信息，返回值跟process_request一样，如果返回None，那么Django帮你执行view函数

3. process_template_response:执行完上面的方法，并且Django帮我们执行完view，拿到最终的response后，如果使用了模板的response就会来到这个方法，可以对response做操作，对header的修改/增加

4. process_response:所有流程处理完来到这个方法，逻辑和process_template_response一样，只是process_template_response针对带有模板的response的处理

5. process_exception:发生异常进入这个方法，可以返回一个带有异常信息的HttpResponse，或者直接返回None不处理

### 单个*的args是一个元组，两个*的kwargs是一个字典，，参数的数量都是任意



















# 第二部分：正式开发
1. post_list逻辑：使用Model从数据库批量拿取数据，然后展示标题和摘要
2. post_detail逻辑：使用Model从数据库批量拿取数据，然后展示
3. 编写模板数据：根据view传递的数据,使用模板语法展示数据
4. 注意外键内容的获取，每一次每一条记录请求都需要对应数据库的来获取外键，导致一次文章列表页查询产生N次相关查询
5. 博客首页，博文详情页都简单展示了



### 配置页面通用数据
**新增页面逻辑：model->view->url->html**
1. 完善模板信息：根据html5标准组织页面
    + 增加不同页面的信息展示：post_list
2. 重构post_list视图
    + 将通过tag_id拿到文章列表和tag对象抽出去作为独立函数
    + 将通过category_id拿到文章分类和文章对象抽出去作为独立函数
    + 先修改model层post模型定义:使用 select_related() 和 prefetch_related() 可以很好的减少数据库请求的次数，从而提高性能
3. 分类信息：model->view——>html
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

7. **定义PostDetailView**，代替post_detail函数，修改模板代码，**修改url**，从url指定要匹配的参数来作为过滤post数据的参数（Post.objects.filter(pk=pk)）,拿到指定文章的实例(pk == primary key(主键))

8. 对于单个数据的请求，django已经帮我们封装好了数据获取的逻辑


#### [DetailView提供的属性和接口： 获取一条数据](https://blog.csdn.net/weixin_42134789/article/details/80327619)
1. model：指定当前View要使用的Model
2. queryset：跟model一样，二选一，设定基础的数据集，model设定没有过滤功能，通过 `queryset = Post.objects.filter(status=Post.Status_normal)`进行过滤
4. get_queryset：返回一个量身定制的对象列表,定义了该方法那么DetailView返回的一个具体对象只会从queryset里查找。
5. get_object接口：根据URl参数，从queryset上获取对应的实例
6. get_context_data：可以用于给模板传递模型以外的内容或参数
3. template_name属性：模板名称

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
3. 修改settings中的配置目录：**THEME指定主题文件的整体目录**
    + 在在DIRS中新增了Django模板查找路径，找不到模板情况下去各个APP查找，因为我们上面设置了'APP_DIRS'：True,如果要新建主题，只需要修改THEME=‘default’即可.新建主题bootstrap==THEME=‘bootstrap’
4. 修改模板：新增**bootstrap**主题
5. 编写bootstrap/base.html
6. 编写bootstarp/list.html
7. 编写bootstarp/detail.html

#### 模板页面extends和block的用法：导航页面是一个主模版，非导航页面通过extends引入主模版，通过block往里面添加不同的内容

1. extends 引入父模板路径[{% extends "./base.html" %}]
2. block 
    + [在导航页面需要被替换的地方使用{% block name %} {% endblock %}  52行](typeidea_item\typeidea\typeidea\themes\bootstrap\templates\blog\base.html)
    + 在非导航页面编辑具体逻辑


### 配置线上静态资源
1. 内联css与外部css
2. Django中的静态资源
    + 怎么在Django中处理静态资源？
    + 线下：通过INSTALLED_APPS中自带的'django.contrib.staticfiles'这个APP
    + 线上：通过STATIC_ROOT和Nginx来部署静态资源

3. 配置settings文件：
    + STATIC_ROOT：配置部署后的静态资源路径。Django提供collectionstatic命令收集所有静态资源到STATIC_ROOT配置的目录中
    + STATIC_URL：用来配置页面上的静态资源的起始路径
    + STATICFILES_DIRS：指定静态资源所在的目录

4. 在base.html 顶部加载 {% load static %},修改link中的路径
    + 使用css {% static 'css/base.css' %} 
    + 使用static标签时为了避免把static硬编码到页面中
    + static不是内置标签，需要在顶部加载{% load static %}

**总结**：
前端概念，Bootstrap提供功能，套用Bootstrap框架实现静态页面，主题配置，熟悉THEME的逻辑。






## 完成整个博客系统
1. 需要完善的页面：
    + 搜索结果页
    + 作者列表页
    + 侧边栏的热门文章
    + 文章访问链接统计
    + 友情链接页面
    + 评论模块


### . 增加搜索和作者过滤：根据关键词搜索文章；展示指定作者的文章列表
1. 增加搜索页面
    + [views.py增加搜索功能：根据title和desc搜索 继承IndexView，编写SearchView，控制数据源由get_queryset方法实现](typeidea_item\typeidea\blog\views.py)
    + 配置urls.py
    + 修改模板字段

3. 增加作者页面
    + 增加view
    + 增加新的url
    + 修改模板中对应的链接

### 增加友链页面

1. 编写config/views.py
2. 编写urls.py
3. 编写config/links.html


### 增加评论模块：单独页面提交
1. 评论提交方式：JavaScript异步提交，当页提交，单独页面提交

2. 评论模块通用化改造：修改comment中的target为CharField，存放被评论内容的网址

3. 通用外键
    + 通过GenericForeigenKey(通用外键)关联多个表
    + 通过增加一个字段content_type来储存对应的模型类型
    + content_type存放的字符串由ContentType来实现
    + 为了实现通用外键，需要多维护一个字段和一张表

4. 实现评论模块
    + 修改model中target字段类型从外键修改为CharField
    + 使用python manage.py makemigrations命令记录model.py的改动
    + 使用python manage.py migrate 使数据库状态与修改完的model状态同步

    + 创建cpmment/forms.py（[Meta](https://www.jianshu.com/p/dd7f4a11a7bb)）
    + 不论是传统需要Form来提交数据，还是通过Ajax的方式提交数据到后端，Form都很好用，可以比较优雅的处理和校验来自外部的数据
    + 在model层提供接口 @classmethod，返回所有有效的评论
    + 在blog/views.py-PostDetailView中添加一个新函数，把commentform和评论的数据传递到模板
    + 在detail.html 中添加评论模块

    + 在comment/view.py中新增一个view
    + 添加模板comment/result.html(评论结果页)
    + 添加url

5. 抽象评论模块组件：将评论修改为即插即用的组件
    + 在commentAPP下新增templatetags目录，新增__init__.py和comment_block.py
    + 编写comment_block.py 定义标签
    + 编写 typeidea/theme/.../comment/block.html,将评论模块抽象为组件
    + 在detail.html加载{% load comment_block %}
    + 调用模块{% comment_block request.path %}

    + 总结：编写py文件，将相关模块html代码抽出来，其他模板用加载就行


### 配置Markdown编写文章的支持
1. MarkDown 第三方库：mistune
    + 使用方法：import mistune ; html = mistune.markdown(your_text_string)

2. 评论内容支持Markdown
    + 评论到展示的流程：填写评论，提交表单->comment/forms.py--CommentForm处理表单->验证通过->保存数据到instance->instance.save方法把数据保存到数据库->用户刷新页面->通过comment_block模板自定义标签获取并展示数据

    + 在写数据的时候进行转换，修改clean_conntent方法，在return content之间增加content = mistune.markdown(content)

    + 写完这句语法后HTML代码直接展示到页面，这时需要手动关闭Django模板自动转码功能---关闭自动转码:comment/block.html代码{{ comment.content }}位置上下增加autoescape off 

3. 文章正文使用Markdown
    + 在Model/Post中新增字段content_html,储存Markdown处理后的内容，修改完model后迁移数据库
    + Post重写save方法
    + 在模板中使用content_html代替content

4. 配置代码高亮
    + 代码高亮需要使用htghlight.js
    + 修改blog/base.html,在</head>上新增一个新的block块，让子模版来填充数据
    + 在blog/detail.html{% block main %}上面新增代码

5. 一般来说script代码应该放到最后，这是为了防止浏览器加载JavaScript时页面停止渲染，用户等待时间过长。




### 增加访问统计：文章访问量的统计
1. 如何统计？
    + 基于当次访问后端实时处理
    + 基于当次访问后端延迟处理---Celery(分布式任务队列)
        + 异步：当前需要执行某种操作，但是我自己不执行，让别人帮忙执行
    + 前端通过JavaScript埋点或者img标签来统计
    + 基于Nginx日志分析来统计

2. **怎么知道用户已经访问过某篇文章？：Web系统针对不同用户提供不同服务**
    + 1.根据用户IP和浏览器类型等一些信息生成MD5标记：用户会重合，ip重合
    + 2. 系统生成唯一的用户id，将其放置到用户cookie中：用户换浏览器产生新用户
    + 3. 用户登录


3. 文章访问统计分析：基于当次访问后端实时处理
    + 连续刷页面不累计算PV
    + UV根据日期来处理
    + 根据系统生成的用户id来标记用户

4. 实现面对的问题：
    + 如何生成唯一id：使用python内置uuid库生成
    + 在哪一步给用户配置id：越早越好，放在middleware中来做
    + 使用什么缓存：使用Django提供的韩村节后

5. **实现文章访问统计：记录uid，赋值，记录**
    + blogAPP新建middleware，新建__init__.py和user_id.py
    + user_id.py:接受请求，生成uid，把uid赋值给request对象，返回response设置cookie，设置为httponly(only服务端)
    + 在setting/base.py中配置MIDDLEWARE的第一行，这样后面的request都带uid属性
    + 完善view层逻辑，在PostDetailView新增一个方法专门处理PV和UV统计，可以直接使用Django cache接口
    + 在实际项目中避免用户在请求数据过程中进行写数据
    + 根据统计进行排序，使用hot_posts方法



### 配置RSS和sitemap：提供一个RSS和sitemap输出接口
RSS：简易信息聚合
sitemap：提供给搜索引擎

1. 实现RSS输出
    + 使用Django的RSS模块，实现RSS输出
    + 在blog目录下新增rss.py

2. 实现sitemap
    + 输出文章列表
    + 在blog目录下新增sitemap.py
    + 编写对应模板的themes/bootstrap/templates/sitemap.xml
    + url.item.tags 做下支持，Post模型tag多对多关联，增加一个属性,blog/models.py

3. 配置RSS和sitemap的urls.py






# 第三部分：使用第三方插件增强管理后台
use xadmin，django-autocomplete-light and django-ckeditor 增强管理后台

### xadmin不写了，已停止更新。




### 使用django-autocomplete-light优化性能
django对于外键或者多对多字段的处理比较粗暴，一股脑的加载到页面，生成一个select标签，如果数据多了一次加载到页面上耗时太多。所以需要优化。

1. django-autocomplete-light 介绍
    + 轻量级自动补全插件
    + 本质上属于懒加载，外键关联数据并不会随着页面加载而加载，等到输入搜索时再加载
    + 原理：封装好一个接口，查询要处理的数据，提供前端组件，用户输入时实现接口查询，拿到数据，展示到页面


2. 引入插件:pip install ....

3. 配置settings.py/installed apps，增加'dal' 'dal_select2'

4. 配置后端查询逻辑
    + typeidea/typeidea目录新建模块autocomplete.py
    + autocomplete.py用来配置所有需要自动补全的接口，自动补全的view层
    + 编写autocomplete.py
    + 配置url
    + 配置展示逻辑：使用autocomplete-light提供的Form层组件接入后端接口（编写blog/adminforms.py ）




### 使用django-ckeditor开发富文本编辑器:引入编辑器插件


1. 安装django-ckeditor

2. 配置settings.py/APP

3. 配置blog/adminforms.py---content

4. 配置settings/base.py，新增配置CKEDITOR_CONFIGS


### 配置图片
1. 在installed_app中增加app-ckeditor_uploader(记得配置CKEDITOR_UPLOAD_PATH)
2. 修改blog/adminforms.py
3. 配置上传路径settings/base.py
4. 修改url



### 自定义存储以及水印
默认存储方式是文件存储，可以根据需求定制

1. 定制方式：继承django.core.files.storage.Storage,然后实现几个接口，可以存储到本地文件系统or网络

2. 在urls.py同级目录下新增文件storage.py,继承FileStorage，重写save方法，处理图片







## 使用django-rest-framework
把所有被请求的实体当作资源，通过http自带方法(GET,HEAD,POST,PUT,DELETE)来进行对应的增删改查等操作。

GET:获取资源；POST：新增数据；PUT：更新数据；DELETE删除数据。

默认接受数据格式：JSON，也可以通过HTTP请求header中的content-type来设置默认格式

RestFramework是一个能快速为我们提供API接口，方便我们编程的框架。API是后端编程人员写的，为了让前端拿数据的一个接口，通常就是以url的形式存在。


1. 每个项目总有第一个人做基础构架，这个时候就不是仅仅实现一个API就OK了，需要考虑更多的事情，包括:
    + 统一的异常处理
    + API权限
    + 统一的参数校验
    + 缓存如何可以做的更简单统一
    + 认证
    + 统一的查询过滤
    + 代码分层
    RestFramework能很好的帮我们做这些事情。

2. REST
    + REST是一种标准，restful是一种规范，根据产品需求需要定出一份方便前后端的规范，与协议（如HTTP协议）不同，不是所有的标准要求都需要遵循。
    + REST与技术无关，代表的是一种软件架构风格，REST是Representational State Transfer的简称，中文翻译为“表征状态转移”
    + REST从资源的角度类审视整个网络，它将分布在网络中某个节点的资源通过URL进行标识，客户端应用通过URL来获取资源的表征，获得这些表征致使这些应用转变状态
    + 所有的数据，不过是通过网络获取的还是操作（增删改查）的数据，都是资源，将一切数据视为资源是REST区别与其他架构风格的最本质属性
    + API的使用主要是为了解决多人开发，特别是前后端分离的情况,
    + 大部分情况前端会用ajax发送请求，后端人员则发送JSON字符串给前端，前端再反序列化后进行使用。这个时候我们需要API.

3. [RESTful 规范](https://www.jianshu.com/p/714b20de337a)
    + **域名**：1.写在路径上，API很简单 2.将API部署在专用域名上（存在跨域问题， 跨域时会引发发送多次请求）
    + **版本**：1.写在路径上，API很简单 2.将版本号部署在专用域名上（存在跨域问题， 跨域时会引发发送多次请求）
    + **路径**：视网络上任何东西都是资源，所以路径均使用名词表示
    + **请求方式**:
        + GET ：从服务器取出资源（一项或多项）
        + POST ：在服务器新建一个资源
        + PUT ：在服务器更新资源（客户端提供改变后的完整资源——全部修改）
        + PATCH ：在服务器更新资源（客户端提供改变的属性——部分修改
        + DELETE ：从服务器删除资源
    + **过滤**： 通过在URL上传参的方式，有GET请求获取相应的数据
    + [**状态码**：我们可以通过状态码来判断请求的状态，以处理相应的请求。在状态码是4开头时，应该捕捉相应错误并返回错误信息 ](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)
    + **返回结果**:针对不同操作，服务器向用户返回的结果应该符合以下规范。






### 1.接口需求及django-rest-framework介绍
1. 需求：开发一套接口，提供分类，标签 数据
    + 配置一套RESTful接口，输出所有文章，其功能跟Web系统提供的类似。具体包含（最新文章列表，分类列表，根据分类获取文章，标签列表，根据标签获取文章）

2. 快速上手
    + 安装：pip install django-rest-framework==3.8.2
    + 设置settings.py中的APP
    + 在blogApp下新增serializers.py文件
    + 新建view层逻辑，在blog下新建apis.py
    + 在urls.py中增加代码
    + 访问http://127.0.0.1:800/api/post/?format=json

3. api_view
    + 是django-rest-framework创建的帮我们把View转换为API View的装饰器
    + 提供可选参数api_view(['GET', 'POST'])限定请求的类型

4. ListCreateAPIView(class-based view):指定queryset，配置好用来序列化的类，就可以实现一个数据列表页。

5. 每一个资源都需要CRUD操作，如果一个个去添加，很麻烦，django-rest-framework提供了更上层的抽象ViewSet，把这些逻辑都封装起来，让我们在一个类中就能完成所有方法的维护。
    + 重新编写apis.py中的代码
    + 在urls.py中增加代码
    + **这样改造完后就有了多个接口，根据只读的需求，有了list和detail接口**
        + http://127.0.0.1:8000/api/post/
        + http://127.0.0.1:8000/api/post/<post_id>/

6. 如果需要reverse操作，可以通过reverse('api:post-list')获取到**文章列表的接口**，通过reverser('api:post-detail', args=[1])获取对应**文章详情的接口**。
    
    + 在运行状态下，可以在ViewSet的某个方法中，通过reverse_action方法获取对应的url。

    + 如果使用了namespace配置，就需要在router中调整。去掉`namespace="api"`,通过base_name来区分不同的URL名称。

    + 在运行状态下的命令：通过self.reverse_action('list')获取对应的列表接口；self.reverse_action('detail', args=[<id>])来获取对应文章的详细接口地址。


#### 2.配置API docs
使用django-rest-framework提供的dosc工具生成接口文档

1. 配置urls.py
2. 安装python包-coreapi
3. http://127.0.0.1:8000/api/docs/ 打开链接，现在展示的是**自动生成的接口文档**


### 实现post接口
####  区分list和detail
1. 调整接口返回数据的格式，文章列表页与文章详情页所需字段不同。需要做的就是为不同接口定义不同的serializer。

2. 定义序列化的类，编写serializers.py
    + (modelSerializer的作用)[https://www.cnblogs.com/oklizz/p/11278510.html]
    + SlugRelatedField:定义外键数据是否可写（read_only参数）
    + slug_field：指定用来展示的参数
    + many=True  多对多（标签与文章）

3. 定义详情接口需要的类，继承PostSerializer在fields中增加content_html

4. 重写获取详情数据的接口，指定serializer_class,所有数据通过这个配置进行序列化。
5. 修改apis.py中的接口代码，在retrieve方法中重新设置serializer_class的值，达到不同接口使用不同serializer的目的

#### 实现分页：在setting中设置新的rest_framework的分页类型，每页多少条
1. 数据量大的情况下要分页返回数据
2. 配置分页,其一是在settings中增加配置（REST_FRAMEWORK）
    + **分页选项**： 1.rest_framework.pagination.PageNumberPagination--当前几页，每页多少条
    + **分页选项**： 2.rest_framework.pagination.LimitOffsetPagination--基于偏移量和Limit的分页，当前位置几条，还需要几条。
    + **分页选项**： 3.rest_framework.pagination.CursorPagination--防止用户填写任意的页码和每页数据量来获取数据




### 实现Category接口---编写接口-->编写视图-->编写url
1. 在serializers.py中增加代码---编写接口

2. 在apis.py中新增代码---编写视图

3. 在urls.py中新增代码 ---编写url


### 获取分类下的文章列表
思路：在postViewSet中通过获取url上query中的category参数，重写类似get_queryset方法实现过滤。这个方法在django-rest-framework中叫做filter_queryset。

1. 先修改apis.py中PostSerializer，通过filter_queryset方法拿到category参数
2. 在serializers.py中定义详情页需要的serializer
3. 再修改apis.py中的CategoryViewSet,添加retrieve
4. 这时访问分类的详情接口，就可以看到对应的文章列表



### HyperlinkedModelSerializer的使用(超链接模型序列化程序)
使用HyperlinkedModelSerializer，直接返回接口链接，而不需要客户端再拼接URL。
1. 用户请求流程：请求文章列表接口/api/post/————>用户点击文章列表，**客户端通过用户点击的id，拼接处URL--/api/post/<post_id>**。
2. 我们可以返回接口地址而不是id，让客户端不需要拼接，直接从数据中拿到接口地址。

3. 实现：通过HyperlinkedModelSerializer
    + 将继承serializers.ModelSerializer改为serializers.Hyper-linkedModelSerializer，然后在Meta的fields配置中新增一个url字段即可

    + 为了避免url的name冲突，对所有接口都设定了base_name，因此需要做额外的工作展示URL。
        + 第一种方法：使用HyperlinkedIdentityField定义要使用的view_name,这种方法可以不继承HyperlinkedModelSerializer,直接用原来的就可以
        + 第二种方法：通过在Meta中定义extra_kwargs属性



### 其他数据接口的实现：标签接口&根据标签获取文章
1. 在serializers.py中新增标签接口
2. 在apis.py中新增展示匹配
3. 在urls.py中新增代码

4. 获取标签下的文章列表
    + 在PostViewSet中编写函数fulter_queryset获取URL上Query中的tag参数
    + 修改serializers.py中的代码
    + 在apis.py中修改TagViewSet，添加retrieve,在retrieve方法中重新设置serializer_class的值，达到不同接口使用不同serializer的目的



### 总结
无论是通过接口输出内容还是通过页面渲染内容，都是输出的一种
无论是通过提交表单(form)的方式还是通过Ajax(serializer)的方式提交数据都是输入的一种，唯一的差别是格式不同。
一图总结：
![avatar](img\form&serializer.jpg)

<hr/>


# 第四部分：上线前的准备及线上问题排查

## 调试和优化

### 常用的调试和调优手段
#### 调试手段：print, logging, pdb
1. **print**:打印程序某个位置的变量，校验是否符合预期。JSON或者dict格式的数据，可以使用pprint模块中的pprint函数打印。

2. **logging**：print只能用于开发阶段，在线上手机数据可以使用logging模块，logging用法和print一样，唯一的差别是logging可以选择输出到文件还是输出到控制台。

3. **pdb**：pdb可以跟踪程序的执行流程，pdb提供了REPL(交互式执行环境)，可以在代码中引入importpdb;pdb.set_trace()让程序来到这一行后进入pdb交互模式，进而可以像Python shell中执行命令那样，获取到上下文中所有变量的值或者更改变量的值。-----类似的工具bpdb和ipdb，交互更友好。
    + pdb运行：python -m pdb python.py
    +pdb设置断点：在需要设置的位置下引入断点：import pdb;pdb.set_trace(),程序执行到这里就会停止下来，进入交互模式。
    + pdb指令：
        + n:next，执行当前语句，只想下一行语句
        + s:step in，跳入某个执行函数中
        + c:continue,恢复执行状态
        + l: list列出当前要执行语句的上下代码
        + ll: long list，展示当前函数的所有代码
        + r:return：直接执行到返回结果的部分
        + q：quit 退出


#### 调优手段
1. 纯手工timer：在要执行代码前增加start = time.time()，最后增加print(time.time() - start),就可以获得代码的执行时间。
    + 代码示例：
    ```python
    import time
    import requests

    start = time.time()
    reqeusts.get('https://www.baidu.com')
    print('cost {}s'.format(time.time() - start))
    ```
    + 这样做比较笨拙，可以进一步优化，构建一个装饰器来完成函数执行时间的获取和输出
    代码：
    ```python
    import time
    import requests

    def time_it(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            print(func.__name__, 'cost', time.time() -start)
            return result
        return wrapper
    @time_it
    def fetch_page():
        requests.get('http://www.baidu.com')
    
    fetch_page()
    ```

2. profile/cProfile
    + 性能检测工具，探测函数的执行时间和执行次数，方便查询函数执行细节，是否是网络接口调用次数过多导致的执行缓慢，还是冗余的数据处理操作导致执行了太多无效代码。
    + 代码示例：定义函数loop，使用profile测量该函数的执行细节,可以显示这个函数的**ncalls：执行次数，tottime：总执行时间(排除子函数执行时间)，percall：平均每次执行时间（tottime/ncalls），cumtime：累计执行时间（包括子函数执行时间），percall：平均每次执行时间,filename:lineno(function):具体执行内容说明**
    ```python
    import cProfile
    import pstats
    from io import StringIO

    pr = cProfile.Profile()

    def loop(count):
        result = []
        for i in range(count):
            result.append(i)


    pr.enable()
    loop(100000)
    pr.disable()
    s = StringIO()
    # sortby = 'cumulative'
    sortby = 'tottime'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    ```

#### 总结：调试和优化是必须的，还要对组件做优化

<hr/>

### django-debug-toolbar优化系统，在线看到各种数据
django-debug-toolbar是Django中一个第三方插件，用来做性能排查。

#### 快速配置
1. 安装：pip install django-debug-toolbar==1.9.1
2. 再settings/develop.py中新增代码
    + 在develop.py中增加的原因是该工具只有在DEBUG为True时才生效，上线后不能用。
3. 配置urls.py,新增代码

#### 解读数据
1. versions: 展示项目用到的库与版本
2. 时间：展示服务端耗时；浏览器端请求响应耗时(使用timing.js库)
3. **SQL：表示请求时执行了那些SQL语句，也就是查询数据库部分。**
    + **21 queries including 13 duplicates,21个数据库请求，13个是重复的。**
    + **SQL下面有类似Duplicated 4 times提示的都是被重复执行的。大部分重复请求都是模板中产生的。**
    + **如何解决重复请求？使用select_related方法**
    + **举例：侧边栏现在也会查询category和User,但是不需要展示，如何不让这两个字段展示？   1.修改Model中的Post的latest_posts方法**
    ```python
        def latest_posts(cls, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        if with_related:
            queryset = queryset.select_related('owner', 'category')
        return queryset
    新增参数with_related,控制返回数据是否包含category和user
    修改完成后还需要修改SideBar模型，此时只需要把content_html方法中的
    'post' : Post.latest_posts() 修改为
    'post' : Post.latest_posts(with_related=False)
    让侧边栏的数据里不包含category和user即可
    ```
    + **查看time，最长的是优化重点。在最右侧有两个动作，一个是Sel，查看具体返回的对象是什么；一个是Expl,用来查看具体执行情况的命令，根据这两个来优化。**

4. Settings:项目中的setting配置
5. Headers：请求header数据
6. Request：请求的一些数据
7. Static files:当前页面用的静态文件，以及那些静态文件可用。
8. Templates：用到的模板以及渲染这些模板时传递的上下文变量
9. Cache：看到缓存的命中情况以及其他统计
10. Signals：查看当前相中的signal以及配置了那些Receiver
11. Logging：当前请求中项目通过logging模块记录了那些日志

<hr/>

### 配置第三方panel

#### 1.djdt_flamegraph----火焰图
1. 安装pip install djdt_flamegraph == 0.2.12
2. 配置settings/develop.py
3. 为便于观察，修改SideBar模型中的get_all函数，增加sleep代码,等待3秒
4. 使用 ./manage.py runserver --noreload --nothreading命令，启动项目
5. **火焰图纵向是调用栈，横向是执行时间，平顶越宽，耗时越大，具体到函数了。**

#### 2.pympler----内存占用分析
1. 安装 pip install pympler==0.5
2. 配置settings/develop.py
3. **上半部分展示内存和虚拟内存使用情况，下半部分展示Django的Model实例具体占用了多少内存**
    + **Resident set size : 表示当前进程实际的内存占用**
    + **Virtual size： 表示系统分配给当前进程的所有虚拟内存**


#### 3. line_profiler----行级性能分析插件
1. 安装 (pip install django-debug-toolbar-line-porfiler==0.6.1)[https://www.jianshu.com/p/9604abfc2b1d]
2. 配置settings/develop.py
3. 简介作用：
    + Line：行号
    + **Hits：这一行代码被执行的次数--调用次数**
    + Time：当前行执行时间除以定时器单元
    + Per Hit：每次执行消耗时间
    + **%Time：执行时间占总时间的比值--耗时占比**
    + Line Contents：对应代码


#### 总结：django-debug-toolbar适合自己分析自己项目的性能


### 使用silk
让测试用户访问最后你来看分析结果，silk非常适合，它需要手机并存储所有访问数据，因此需要增加新的表来存储。

#### 快速配置silk
1. 安装 pip install django-silk==3.0.0 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
2. 配置settings/develop.py
3. 配置url
4. 创建表，因为需要silk存储数据--python manage.py migrate
5. **多访问几个页面，然后打开http://127.0.0.1:8000/silk，展示刚才随机点开的页面请求耗时，数据库请求树以及有多少次数据库请求。**
6. 点进去可以看到，detail，sql，profiling
    + detail：浏览器network看到的内容
    +**SQL：列出具体SQL执行情况，点进去可以看到这个SQL由那行代码发起**


#### 配置profiling
1. 修改blog/views.py,在ommonViewMixin里添加装饰函数@silk_profile(name='get_context_data')。
2. 打开http://127.0.0.1:8000/silk，查看profiling
3. profiling记录了装饰函数在执行时的耗时以及是否产生查询的情况


#### 总结
xilk：适合测试时用

### 本章总结
介绍了python中常用的调试和调优方法，了解了两个比较好的插件：django-debug-toolbar和silk
无论什么语言与框架，调优思路大体一致：减少外部I/O，减少冗余的调用，优化耗时的逻辑。
<hr/>


## 配置MySQL和redis缓存
配置redis，如果只是作为缓存来用，在做完所有的优化之后再来配置缓存，不然会绕过已有的性能问题。


### 配置MySQL
1. 分层模式：MVC模式
    + Model层--模型层
    + View(django的Template)----展示层
    + Controller(django的view)----逻辑控制层

2. **没有固定模式，只有更适合业务的模式**

3. 分层的目的
    + **解耦：完全耦合的东西在中间加一层，从而保证互相变化后只需要对外接口不变，就不会有任何影响。**

4. 修改settings/develop.py中的DATABASES配置

5. 配置数据库的两种方法
    + 1. 下载mysql，配置好文件，启动服务，创建数据库CREATE DATABASE mysql_db;，指定数据集，校对规则。
    + 2. 下载phpstudy+navicatpremium 15，phpstudy启动集成的配置，navicatpremium 15连接数据库



#### 使用CONN_MAX_AGE优化数据库连接
1. CONN_MAX_AGE作用：**配置Django和数据库的持久化连接，用来解决并发量过大时来不及关闭连接导致的错误。**理念类似于数据库连接池的概念，但是从实现上来看它并不是。

2. **为什么要优化连接？**上线后访问量大点，**数据库层抛出 too many connections错误**，其原因就是：默认情况下，**每个请求都会创建一个新连接，请求结束会关闭该连接，当并发量过大时来不及关闭连接，就会导致连接数不断增多，抛出错误。**

3. 如何配置：**默认值是0**，配置时需要**参考数据库的wait_timeout配置**，建议不要大于wait_timeout的值。**可选项还有None，None意味着不限制连接时长**。

4. 建议：采用多线程方式部署项目不要配置CONN_MAX_AGE。因为每一个请求都使用一个新线程处理，那么每个持久化的连接都达不到复用的目的。使用gevent作为worker来运行项目，也不建议配置CONN_MAX_AGE，因为gevent会给python的thread动态打patch，导致数据库连接无法复用。


#### 配置正式Settings
1. 创建正式配置文件settings/product.py




#### 总结：找本MYSQL书看

<hr/>

### 缓存的演变
了解基本概念。

#### 什么是缓存？
1. 缓存(cache)：其作用是缓和较慢存储的高频次请求。**加速慢存储的访问效率。**
2. 缓存实现：
    + **被动缓存：如果这个SQL被执行过，那么短时间内就没必要执行，直接复用上次的结果**实现详情查看--->other_cache\learn_cache.py
    + **主动缓存：1.系统启动时，自动把所有接口刷一遍，这样用户访问时缓存就已经存在；2.在数据写入时同步更新或写入缓存**



#### 缓存装饰器
1. 每个函数都要写一遍缓存获取逻辑，太麻烦，将其改编为装饰器模式，通过装饰对应函数给其增加缓存逻辑,详情查看--->other_cache\cache_decorator.py
2. (装饰器：装饰器本质上是一个 Python 函数或类，它可以让其他函数或类在不需要做任何代码修改的前提下增加额外功能，装饰器的返回值也是一个函数/类对象。它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景，装饰器是解决这类问题的绝佳设计。有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码到装饰器中并继续重用。概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。)[https://www.liaoxuefeng.com/wiki/1016959663602400/1017451662295584]
3. functools.wraps的作用时为了保留原函数的签名，因为被装饰的函数实际上对外暴露的是装饰器函数。repr作用是把传递给它的对象都转为字符串。


#### 增强缓存装饰器
1. 缓存装饰器会遇到2个问题，1.缓存数据始终不更新，这是个问题；2. CACHE的容量
2. 解决问题：1.标记被缓存的数据；2.设置CACHE的容量上限---可以通过限制size和时间来限制淘汰那些不经常使用的数据，实现一个自己的dict，设定好淘汰算法,代码参考--->other_cache\my_lrucache.py
    + 实现自己的一个dict，用dict内置的方法--magic method
    + 设定好淘汰算法，当容量超过设定的值时，删掉不需要的内容，使用LRU算法，大体逻辑就是淘汰掉最长时间没使用的哪个。
3. 总结my_lrucache.py逻辑
    + 实现dict：通过**实现内置方法(__getitem__和__setitem__)实现了一个dict对象**
    + 缓存淘汰算法的使用：实现的是**LRU算法，这个缓存dict是非线程安全**的
    + OrderedDict的使用：保证顺序，每次遍历都能从最早放进去的数据开始。

4. 实现了自己的dict后，继续修改learn_cache.py
    + 对于变化频繁函数，有效期设置短一点，变化不频繁的函数有效期长一点

5. 在python3中，LRUCache已经是标准库的一部分，通过引入functools.lru_cache使用

6. 总结：在cache_decorator.py中使用了装饰器，但是需要解决两个问题，缓存数据的更新与缓存数据的容量，所以写了my_lrucache.py,在这里面可以通过限制size和时间来限制淘汰那些不经常使用的数据，自己实现一个自己的dict，然后我们修改learn_cache.py里的代码，这里可以继承自己写的字典，设定max_size和expiration。


#### 是否需要引入reddis
1. 没有性能问题，或者没有那么大的流量，没必要多增加一套系统
2. 如果需要增加，最好充分掌握它的用法和实现逻辑


#### 继续演变缓存逻辑
如果需要支持多线程应该怎么办？多台服务器呢？可以通过socket编写一个缓存服务器，对外提供服务，无论是多线程还是多进程还是多台服务器，都可以处理了，如果独立的缓存服务受限与服务器内存可以实现分布式缓存吗？
软件，系统框架都是一些简单需求不断累加的来的




### Django中的缓存配置
Django缓存配置分为2种，一种是内置的缓存模块，一种是第三方缓存。

#### 内置缓存模块：四种缓存
1. 实例 urls.py中的sitemap.xml接口进行缓存，20分钟内访问不需要再次生成sitemap

2. local-memory caching：内存缓存，线程安全，进程独立，每个进程一份缓存，默认配置。代码如下👇
```python
CACHES = {
    'default': {
        # 后端
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 路径，位置
        'LOCATION': 'unique-snowflake',
    }
}
```
      
3. filesystem caching: 文件系统缓存,把数据缓存到文件系统中，其他没差别。代码👇
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
```


4. database caching：数据库缓存，需要创建缓存用的表，这些表用来存储缓存数据。代码👇
```python
python manage.py createcachetable
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
```


5. memcached: django推荐的缓存系统，也是分布式（分布式逻辑在客户端）,django内置支持，集成度较好。
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '172.19.26.240:11211',
            '172.19.26.242:11211',
        ]
    }
}
```

#### 配置Redis缓存

1. 下载稳定包：https://redis.io/download

2. 配置Django中的Redis缓存
    + 安装对应包:pip install django-redis==4.9.0-----pip install hiredis==0.2.0，hiredis提升Redis解析性能

3. 在settings/product.py中增加代码


#### 应用场景和缓存的粒度
需要知道什么时候，什么情况下，在哪里使用缓存。不同场景不同缓存，配置不同粒度。

1. django提供的粒度缓存方案
    + 整站缓存：直接在settings的MIDDLEWARE中第一行增加'django.middleware.cache.UpdateCacheMiddleware'
    + 整个页面的缓存:sitemap缓存
    + 局部数据缓存:既包含函数中某部分逻辑的缓存，也包含 模板中一部分数据的缓存。

2. 局部数据缓存
    + 函数缓存，增加装饰器，修改Post.hot_posts，进行较长时间缓存
    + 模板缓存:只需要把缓存的内容用cache标签包起来👇50s
    ```python
    {% load cache %}
    {% cache 50 sidebar %}
        ..sidebar..
    {% endcache %}
    ```

#### 总结
django缓存配置和使用都非常简单，并且提供了多种缓存系统的适配。


### 本章总结
配置了MySQL和缓存
别忘了修改成markdown




## 上线前的准备
如何部署上线，让代码为用户提供服务。

### 代码如何为用户提供服务
img\部署结构图.jpg


#### 整体结构
1. 先到打包服务器执行打包命令(逻辑：从git仓库拉取最新代码，并执行打包)

2. 到部署服务器执行部署命令，部署服务器远程连接生产服务器，执行安装命令，安装对应版本。


#### 项目部署方案
传代码到服务器--->安装项目依赖包---->启动项目
1. 代码到服务器步骤
    + 打包和上传软件到一个软件源，在生产服务器执行安装命令

2. 软件分发方式
    + rsync/scp工具：同步两个服务器之间文件的工具，较方便的将本地文件同步到服务器上，个人项目可以使用这个工具。
    + git仓库分发代码：可以在服务器上通过拉去git仓库的代码来更新代码
    + PyPI：标准的Python项目分发方式：需要自己搭建PyPI服务器，将开发好的代码打包并上传到PyPI服务器。

3. 系统架构
1. img\系统架构图.jpg

2. 流程：
    + 项目对外发布时，申请对外域名，最外层服务器根据域名转发用户请求到应用系统上，最终通过读取数据库的数据拿到结果，返回给用户。

3. 注意：避免单点存在，每个节点的服务器都要部署多台；1.提供系统的并发承载；2.避免某台机器宕掉对整体服务产生影响。



### 标准化打包和自动化部署
使用官方的PyPI打包

#### 配置项目的setup.py
1. setup.py作用：打包和安装

2. 这个文件只是执行了Python提供的setup函数，需要了解这个函数中每项参数的作用

3. 编写：放在typeidea根目录下

4. 参数介绍：**了解控制把文件打到包里的参数**

    + packages:指明要打入的包，find_packages函数帮助我们发现指定目录下的所有Python包

    + package_dir：指明上面的packages的包都在哪个目录下，如果再setup.py统计目录，可以不写。

    + package_data:指明除了.py文件外，还需要打包那些文件到最终的安装包里。对应的值需要是字典格式，key表示要查找的目录，value是list结构，表示要查找的具体文件。如果key为空表示查找所有包。需要打包javascript文件，位置在typeidea/themes/bootstrap/static/js/post_editor.js,**开头typeidea是包名，所以从themes开始，匹配每一级目录。**

    + include_package_data同package_data类似，也是用来指定要打包那些额外文件到安装包里，不同的是，这项配置依赖MANIFEST.in文件---文件路径(MANIFEST.in)

    + **package_data和include_package_data功能差不多，一般用第二种方式配置，因为配置简单。**

    + install_requires: 指明依赖版本。安装当前项目时，先去安装依赖包，也是这项配置。

    + extras_require: 额外的依赖，安装包的同时也会安装这个配置里面的包

    + scripts：指明要放到bin目录下的可执行文件

    + entry_points：程序执行点，比较常用的配置是console_scripts，用来生成一个可执行文件到bin目录下。

    + classifiers：说明当前项目情况，版本，阶段，面向人群等信息。

5. 配置好setup.py后，运行python setup.py sdist或者python setup.py bdist_wheel。----**注意：如果打包出现gbk错误，请把MANIFEST.in中的中文删掉，以及.py文件不能用中文名**



#### sdist与bdist_wheel的差别：bdist_wheel更好
1. **sdist：源码分发，打包之后的包时以.tar.gz结尾,打的包是源码包。**当用pip安装源码包时，还需要经过build阶段，也就是执行python setup.py install
2. **bdist_wheel：打出来的包是wheel格式，以whl结尾，这种格式的包里面包含文件和元数据，安装时只需要移动到对应位置即可。**

3. 有wheel包存在优先安装wheel

4. 通过参数控制最终输出的包是针对python哪个版本的。比如python setup.py bd-st_wheel --universal：表示所有版本，并且没有c扩展；python setup.py bdist_wheel --python-atg py36:指定版本为python3.6。也可以通过文件方式配置，创建文件setup.cfg,设定[bdist_wheel] python-tag = py36 #universal=0，仅限当前python版本2或3 #universal=1 # 2和3通用


#### 配置内部PyPI服务器:需要在linux系统使用
1. 安装：pip install pypiserver

2. 启动：pypi-server -p 18080 -P /opt/mypypi/.htaccess /typeidea/dist
    + -p:指定端口号
    + -P：指定认证文件 最后一个参数是上传包存放目录


#### 自动化部署
自动化：把人类需要做的操作让代码来执行

1. 新版本上线需要的流程
    + 1.打包上传到PyPI服务器：python setup.pybdist_wheel upload -r internale
    + 2. 登录生产服务器 ssh root@product_server_ip
    + 3. 检查或创建虚拟环境：less my-venv/.bin/activate或python3.6 -m venv my-venv
    + 4. 激活虚拟环境：source my-venv/.bin/activate
    + 5. 安装对应包：pip install typeidea==0.1 -i http://private-pypi-server.com/simple/--trusted-host private-pypi-server.com
    + 6. 上传supervisord.conf
    + 7. 启动supervisord

2. 服务上线后，可能随时会遇到突发流量，需要增加服务器，一次增加很多台。此时，怎么快速把所有服务器都安装好？这就是自动化的意义。

3. 合适自动化部署的库：paramiko和Fabric
    + paramiko：比较底层的库，是SSHv2协议的Python实现，提供一个SSHClient使用，可以完成SSH的所有操作。
    + Fabic：是基于paramiko的库，封装了很多工具
    + 对比来说：paramiko像是socket，而Fabric相当于requests这样多封装的库

4. Ansible:Fabric像是一个工具箱，用来在远端执行命令，而Ansible提供了一套简单的流程，按照流程来就可以。

#### 编写fabfile配置
1. Fabric提供了哪些功能：**通过对SSH的包装对rsync的包装，处理跟远端服务器的交互**
    + 配置主机信息以及提供全局的env对象，在代码执行期间的任意函数中通过它获取配置信息
    + 对本地shell命令和远端shell命令的封装,可以通过简单的local(whoami)或者run('whoami)的方式在本地或者远端执行命令
    + 基于上面两项功能提供了更多的工具及
    + 上下文管理工具context_manager

2. 在项目根目录下增加fabric.py文件，同时新增一个conf文件夹在文件夹中新增supervisord.conf文件

3. 编写fabfile.py

4. 打包时只需要执行命令fab build

5. 如果通过专门服务器打包，需要把local替换为run，并且也需要把_Version中操作文件的部分改成Fabric提供的fabric.contrib.files.sed来进行版本号的替换，另外还需要增加分支切换的逻辑，因为打包时要指明分支。

6. 理解打包逻辑后，编写部署方法fabfile.py

7. 执行打包命令fab build

8. 项目部署完成后，收集静态文件到STATIC_ROOT下

9. 开发完成后，理论上拿到服务器并配置号SSH key认证登录后，只需要执行fab deploy:<对应版本>,<对应profile>，就可以把项目安装上去


### 总结

要做到自己搭建PyPI服务器，能完成通过fab的打包，上传以及部署安装


### 在生产环境运行项目
配置项目运行相关内容。
#### 为什么需要使用Gunicorn？
1. 使用WSGI方式部署项目而不是通过runserver部署项目

### Gunicorn简介
1. Django实现了WSGI协议，通过该协议，可以使其运行在其他WSGI容器中。Gunicorn就是这么一个容器。

2. Gunicorn是纯Python开发的一款WSGI容器，它使用pre-fork多进程模式，能够广泛兼容不同Web框架，实现简单，资源占用少，相当快。

3. 特性：
    + 原生支持WSGI，Django和Paster
    + 自动的工作进程管理
    + 简单的Python配置
    + 多种工作进程配置方式
    + 提供多种钩子(hook)，便于开发自己的扩展

4. 提供多种worker模型
    + 同步方式：sync--默认配置,与runserver类似，但是它不会启动新的线程来处理接受的请求
    + 异步方式：gaiohttp,gthread,gevent,eventlet,tornado
    + 异步分为：异步worker，tornado，worker，AsyncIO(异步IO)，worker


#### 使用Gunicorn

1. 通过gunicorn typeidea.wsgi:application -w 8 -k gtnread -b 127.0.0.1:8000 --max-requests=10000 启动
    + -w：启动进程数，n+1
    + -k:使用哪个worker模型运行项目
    + -b：绑定到哪个端口上
    + --max-requests:可选配置，当进程处理请求达到指定数量后重启，避免内存泄漏


#### Supervisor介绍：进程控制软件 
1. 提供功能：
    + supervisord：启动supervisor组件
    + supervisorctl：通过类似shell的交互方式来管理已经启动的进程
    + Web服务器
    + XML-RPC接口：提供跟Web服务器一样的功能，只是对上面接口做了xmlrpc的封装

2. 配置文件：
    + [unix_http_server]:UNIXsocket配置，是supervisor用来管理进程的接口（supervisord启动后，supervisorctl需要通过这个socket来跟它通信）
    + [inet_http_server]:这时Web服务器配置
    + [rpcinterface:supervisor]：用来配置RPC接口，这是必须的配置
    + [supervisorctl]：命令配置
    + [program<程序名>]：程序配置

3. 安装：pip install supervisor -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

4. 编写dev_supervisord.conf

5. 通过supervisord -c conf/dev_supervisord.conf运行程序

6. 有异常通过过tail -f stdout.log以及tail -f supervisord.log查看是否有异常日志

7. 需要注意：[program_name:typeidea]下的command和directory需要重新配置

#### 自动化部署和supervisord

1. _reload_supervisoird函数作用：根据变量渲染supervisord.conf，然后将其上传到对应的部署目录，通过run函数，关闭原有的supervisord进程，然后启动新的进程。这样做的目的是加载新的supervisord.conf


####  setup.py和requirements.txt
1. 新增的依赖项添加到setup.py中，并且一定要写版本号

2. 修改requirements.txt
    + 第一行指明需要从内部PyPI源安装
    + 第二行是依赖项
    + 第三行是指从当前目录安装，其实就是通过setup.py安装当前的项目


#### 配置正式settings
1. 配置正式环境，也就是配置settings/product.py
    + SECRET_KEY:加密，不要对外泄漏。
    + DEBUG：生产环境要设置成False
    + ALLOWED_HOSTS: 允许访问的域名，它在DEBUG为False时才会生效，用于配置外部访问
    + E-mail相关配置：服务器配置了SMTP服务的话，就不需要额外配置，否则需要配置E-mail服务。
    + STATIC_ROOT：通过./manage.py collectstatic命令将所有静态资源收集到这项配置中
    + CONN_MAX_AGE：对于线上应用，建议配置长连接，但是需要避免使用多线程或者gevent
    + LOGGING:日志时必不可少的部分，通过它来记录和排查线上问题
    + ADMINS和MANAGERS：配置系统管理员邮箱，这时list格式，用来接收系统异常，前提是配置了邮件服务。
    + 配置自定义异常页面

2. 编写product.py


#### 静态文件处理
1. 常规Nginx配置

2. 通过Django提供的静态文件服务来处理静态请求


#### 总结
1. 本地：通过runserver
2. 测试服务器通过 fab -R myserver deploy:0.1,develop部署
3. 正式：fab -R mysql deploy:0.1, product部署




### 配置Nginx：如何通过Nginx来做负载均衡

#### 1.Nginx介绍
1. Nginx是俄罗斯人编写的轻量级HTTP服务器，是一个高性能的HTTP和反向代理服务器，同时也是一个IMAP/POP3/SMTP代理服务器。Nginx最早由俄罗斯人lgor Sysoev开发。很长时间内，它被用作高负载的俄罗斯网站上。

#### 2.为什么使用Nginx
 1. 从理论上来讲，其实不需要Nginx这样一个代理服务器的，哪个为什么需要额外增加呢？


 2. 了解下Web部署模型
     + 1. **最简单的Web部署模型--runserver**：**client直接连接socket**，但是不能用于生产环境。
     + 2. **通过Gunicorn--Gunicorn WSGI**：可以**通过多进程方式来部署项目，但是依然受限于单机资源限制**，不能很方便的通过增加服务器提高负载能力
     + 3.**较常见的系统结构--Nginx+Gunicorn**：好处是可以**有多台服务器来部署Nginx，也可以有多台服务器来部署Gunicorn应用，在这样架构中，Nginx处于网管角色，有效分发恶意请求，处理静态资源，扩展方便**。
     + 4.**比较成熟的架构模型--Nginx+Gunicorn**：**避免单点存在，因此架构中的任何一个组件都需要在不同的服务器/机房”冗余“一份**，一方面可以**抗住高并发流量，另一方面不会因为服务器或者机房故障导致系统不可用。**


3. 从'runserver'到'Gunicorn WSGI'，再到'Nginx+Gunicorn'，其实是在**不断增加软件中的'层'，让每一层只通过一定的标准来通信**，比如**Gunicorn和Django通过WSGI**，**Nginx和Gunicorn通过HTTP接口**，这样**每一层的变化都不会对另一层造成影响**。**在Gunicorn中，可以选择任意的worker模型**，**在Nginx，也可以调整任意参数**，而不会对后端造成影响。


#### 3. 配置Nginx
1. 安装 yum insteadall nginx

2. 安装后的默认配置/etc/nginx/nginx.conf

3. 在/etc/nginx/apps/typeidea.conf最后一行包含网站的配置文件

4. 通过fab deploy:<版本>,product部署项目，启动Nginx后就能看到页面了，激活虚拟环境，并且配置正式的profile:export TYPEIDEA_PROFILE=product，然后执行./bin/manage.py collectstatic

#### 总结
Nginx是现在Web开发中不可缺少的组件。



### 常用的监控方式
1. 对与正式项目来说一定要增加监控：
    + 知道系统目前状态
    + 第一时间发现异常
    + 预测系统变坏的可能
2. 两类监控：
    + 实时监控
    + 统计分析

#### 实时监控
1. 比较使用的方法就是配置Nginx的check status模块

2. 实时监控应对的几种不同的异常：
    + Nagios，Zabbix，Cacti端口存活检测：运维常用监控系统，**定时扫描端口是否存活，如果存在异常，会发送警告**
    + 通过E-mail发送异常信息，如果系统运行时发生异常，发送邮件警告。
    + Sentry：和E-mail逻辑差不多，但是会收集到一个独立平台。


#### 统计分析
1. 通过日志来分析潜在风险

2. 上线后会得到的日志
    + Nginx的访问日志和异常日志
    + 系统运行产生的正常日志
    + Redis的慢日志
    +Mysql的慢日志

3. ELK：是用的比较多的模式，所有日志都会被统计到ELK中，针对Nginx日志，可以用ELK分析每天各种状态码占比以及后端服务的响应时间。

4. 无论任何日志分析系统都包含
    + 访问量统计
    + 错误状态码(50x,40x)占比；
    + Nginx请求时间统计
    + 后端响应时间统计

5. 如果Nginx的请求时间高于后端的响应时间，意味着Nginx所在服务器跟应用所在服务器时间存在网络问题



#### 业务监控(埋点统计)
1. 监控上线后业务流量，分析用户行为，知道下次需求迭代


#### 总结
监控很重要。




### 压力测试

#### 计算系统承载量
1. **最小承载量**：一个网站有10万活跃用户，每次访问4页面，一天40万次访问，每次访问一个页面调用三个接口就是，访问量就是40万*4=160万，一天有86400s，减去睡觉的8小时也就是一天有57600s，**每秒需要承载的访问量就是160万/86400=28QPS或TPS**，但是**这种情况只能是系统的最小承载量**。假设用4进程4线程处理业务也就是4*4=16，28/16=1.75,每秒处理两个请求。
    + **QPS：每秒能承受的请求数**
    + **TPS：每秒能处理的请求量**


2. **最大承载量**：是系统高峰期几分钟或者十几分钟的访问量来做计算，并在算出来的值上面冗余一定的承载空间。比如网站在访问高峰期5分钟活跃用户量为1000，那么应该是1000*4*4=16000访问量，16000/（5*60）=53QPS或TPS,1S处理53个请求，如果是单线程单进程模式，1000/53=18ms处理一次请求。


3. 反推：系统QPS是100，最小承载访问量为100*60*60*24=864万，最大承载量100*60*5=3万


#### 压力测试
1. 系统上线后，一定要进行压测，得出系统理论上的处理情况以及每个进程或者单台机器的承载量。


#### 压测工具介绍
1. ab：Apache压力测试工具
    + 用法:10000次请求100并发
        + ab -n 10000 -c 100 http://127.0.0.1:8000/

2. siege:基于C开发的一款开源压测工具
    + 用法：100并发持续30s
        + siege -c 100 -t 30s http://127.0.0.1:8000/

3. **wrk:更现代的压测工具，支持Lua脚本**
    + 10个连接，4个线程，持续30s
        + wrk -c 100 -d 30s -t 4 http://127.0.0.1:8000/
    + 启动方式:export TYPEIDEA_PROFILE=product && gunicorn -w 8 typeidea.wsgi:application -k gthread

4. 还有其他压测工具，基于Golang开发的hey和boom，大同小异--**需要做的就是配置不同参数---总请求数或持续时间，并发数来观察系统的放映，需要关心的是Requests/sec或者Transfer/sec，以及成功率失败率。**对于复杂的交易系统来说，wrk是合适工具，可以编写Lua脚本。



#### 完全模拟真实流量
1. TCP Copy：线上用了100台，需要优化到50台，每台承载量翻一倍，怎么放大流量？使用TCP Copy，复制和放大流量。

2. 关注线上监控：
    + 小时/分钟级别的错误量
    + 分钟/5分钟级别的后端服务平均响应时间，以及响应时间大于100ms以及200ms的占比
    + 系统负载

3. TCP Copy可以用用来做灰度发布


#### 缓存加速访问
1. 在压测时需要排除缓存对测试结果的影响，得到不加缓存的测试结果后，可以配置不同级别的缓存，分别进行压力测试。对系统承载情况有更加全面的认识，方便上线后调整缓存方案

2. 测试sitemap.xml
    + wrk -c 100 -d 30s -t 4 http://127.0.0.1:8000/sitemap.xml

#### 总结
上线前压测，尤其是可预期流量系统的压测。还要做好监控方案，合理部署结构降低影响。


































*args表示任何多个无名参数，它是一个tuple；**kwargs表示关键字参数，它是一个dict。
*args(tuple)代表继承来的参数不可更改，需要继承后再更改


当你把一对小括号放在后面，这个函数就会执行；然而如果你不放括号在它后面，那它可以被到处传递，并且可以赋值给别的变量而不去执行它。


函数对象有一个__name__属性，可以拿到函数的名字，__name__就是个验证用的变量，来看下执行的模块是外来户，还是本地人，是本地的都运行；不是本地人的，就运行能够引入的那一部分




    
