# typeidea

## 项目记录
### 5.奠定项目基石：Model---对数据库中字段的抽象
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



### 配置admin页面
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


### 自定义模块
1. 自定义Form（表单）
    + Form的作用：Form是对用户输入以及Model中要展示数据的抽象

2. 在同一页面编辑关联数据：在分类页面直接编辑文章
    + 编写blog/admin.py---PostInline类

3. 定制site：一个系统对外提供多个admin后台
    + 用户模块的管理与文章分类等数据的管理分开；修改后台的默认展示
    + 自定义site：将后台分为两个：super_admin(管理后台)    admin(用户后台)

### admin权限逻辑及SSO登录
1. 集成SSO(单点登录)
2. 判断某个用户是否由添加文章的权限：权限管理是在另外的系统上，只提供一个接口---有权限，响应状态为200，没权限则为403

 
