# typeidea

## 项目记录
### 5.奠定项目基石：Model
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
1. 






 
