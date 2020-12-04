from dal import autocomplete
from django import forms

from .models import Category, Tag, Post

# 自定义Form，修改status的输入框为文本框(Textarea)

class PostAdminForm(forms.ModelForm):
    # widget 文本框 ，简介：摘要 required
    desc = forms.CharField(widget=forms.Textarea,label='摘要',required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类',
    )

    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )

    # 为避免javascript资源冲突，定义meta and fields，将自动补全字段放在前面
    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'content', 'status')