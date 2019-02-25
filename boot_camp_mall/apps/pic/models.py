from django.db import models

# Create your models here.
class PicTest(models.Model):

    """图片商城测试类"""

    image = models.ImageField(verbose_name='图片')

    class Meta:
        db_table = 'tb_pics'
        verbose_name = 'FastDfs上传文件测试'
        verbose_name = verbose_name