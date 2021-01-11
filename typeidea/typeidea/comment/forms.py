# 文件： comment/forms.py
from django import forms
import mistune

from .models import Comment


# 处理表单，验证表单
class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        # Django 会把部件渲染成 HTML
        # 定制froms部件的实例对象，Input,EmailInput都是部件
        widget=forms.widgets.Input(
            # attrs里定制渲染到html的里面的属性
            attrs={'class': 'form-control', 'sytle': "width:60%;"}
        )
    )

    email = forms.CharField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'style': "width: 60%;"}
        )
    )

    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': "width:60%;"}
        )
    )

    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        # 获取到的content不足10字段
        if len(content) < 10:
            # 抛出异常，验证错误
            raise forms.ValidationError('内容太短了呢~')
        # 写入的时候使用markdown语法
        content = mistune.markdown(content)
        return content
    
    # 模型的元数据
    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']