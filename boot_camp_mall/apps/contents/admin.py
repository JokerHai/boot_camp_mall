from django.contrib import admin
from contents.models import Content, ContentCategory
# Register your models here.

class ContentAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ['id']

admin.site.register(Content)
admin.site.register(ContentCategory)


