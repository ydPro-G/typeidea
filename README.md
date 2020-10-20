# typeidea

## 项目记录
### 5.奠定项目基石：Model
1. 创建虚拟环境，项目与配置

2. 拆分settings适应不同的运行环境
    + __init__.py：引导模块
    + base.py：基础模块，之后需要创建不同的配置文件都是基于base.py(重复的抽象成基类，有特性的抽出来做子类也就是单独的配置文件。)
    + develop.py:子类，线下数据库配置文件

3. 编写Model层代码
    + 创建APP：每个APP都是自组织，紧耦合，内部所有逻辑都相关联的。
    + 在models.py中创建博客内容相关的模型

 
