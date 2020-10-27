from django import forms

# 自定义Form，修改status的输入框为文本框(Textarea)

class PostAdminForm(forms.ModelForm):
    # widget 文本框 ，简介：摘要 required
    desc = forms.CharField(widget=forms.Textarea,label='摘要',required=False)