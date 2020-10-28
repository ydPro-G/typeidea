from django.contrib import admin

from .models import Comment
from typeidea.base_admin import BaseOwnerAdmin

# Register your models here.
# comment admin配置

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
