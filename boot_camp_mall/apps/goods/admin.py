from django.contrib import admin
from boot_camp_mall.components.BaseAdmin import BaseAdmin
from goods import models
from celery_tasks.async_html.tasks import generate_static_sku_detail_html
from goods.models import Goods


class SKUAdmin(BaseAdmin):

    list_display = ['id', 'category','substring_name', 'substring_caption','goods','price','cost_price','market_price','stock','sales','comments','is_launched','is_hot']

    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_sku_detail_html(obj.id)

class SKUSpecificationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_sku_detail_html.delay(obj.sku.id)

    def delete_model(self, request, obj):
        sku_id = obj.sku.id
        obj.delete()
        generate_static_sku_detail_html.delay(sku_id)

class SKUImageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        generate_static_sku_detail_html.delay(obj.sku.id)

        # 设置SKU默认图片
        sku = obj.sku
        if not sku.default_image_url:
            sku.default_image_url = obj.image.url
            sku.save()

    def delete_model(self, request, obj):
        sku_id = obj.sku.id
        obj.delete()
        generate_static_sku_detail_html.delay(sku_id)
@admin.register(Goods)
class GoodsAdmin(BaseAdmin):

        list_display = ['id','brand','name','sales','comments','filtration_create_time']

        search_fields = ['name']

admin.site.register(models.GoodsCategory)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Brand)
admin.site.register(models.GoodsSpecification)
admin.site.register(models.SpecificationOption,SKUSpecificationAdmin)
admin.site.register(models.SKU,SKUAdmin)
admin.site.register(models.SKUSpecification)
admin.site.register(models.SKUImage,SKUImageAdmin)