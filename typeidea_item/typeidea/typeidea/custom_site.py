from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = 'Typeidea'
    site_title = 'Typeidea管理后台'
    index_title = '首页'

# 定义站点从admin变为cus_admin
custom_site = CustomSite(name='cus_admin')