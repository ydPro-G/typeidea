from django import template

from comment.forms import CommentForm
from comment.models import Comment

# 自定义template 的tags和filters

# 要成为一个可用的 tag 库，模块必须包含一个名为 register 的模块级变量。
# 它是一个 template.Library 实例
register = template.Library()

#在 Library 对象上调用 inclusion_tag() 创建并注册该包含标签。
@register.inclusion_tag('comment/block.html')

def comment_block(target):
    return {
        # #  tagtemplate中不包含request对象，所以需要把tartget显示地传递进去
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target),
    }
