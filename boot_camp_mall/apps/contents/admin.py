from django.contrib import admin
from contents.models import Content, ContentCategory
from boot_camp_mall.common import constants
# Register your models here.

@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_per_page = constants.ADMIN_LIST_PER_PAGE

    list_display = ['id','name','key']
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):

    list_per_page = constants.ADMIN_LIST_PER_PAGE


    list_display = ['id','category','title','text','sequence','status']

    list_filter = ['category','status']

    search_fields = ['title']