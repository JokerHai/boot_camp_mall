from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
# Create your models here.
from boot_camp_mall.common import constants
from boot_camp_mall.utils.model import BaseModel


class User(AbstractUser):

    """用户模型类"""

    mobile = models.CharField(max_length=11,unique=True,verbose_name='手机号')
    email_active = models.BooleanField(default=False,verbose_name='邮箱验证状态')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,on_delete=models.SET_NULL, verbose_name='默认地址')
    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_verify_email_url(self):
        """
            生成用户的邮箱验证连接地址
        """
        data = {
            'user_id':self.id,
            'email'  :self.email
        }
        serializer = TJWSSerializer(secret_key=settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)

        # 对用户的信息进行加密
        token = serializer.dumps(data).decode()

        #生成用户的邮箱验证连接地址
        verify_url = constants.EMAIL_VERIFY_URL+token

        return verify_url
    @staticmethod
    def check_verify_email_token(token):
        """
        检查验证邮件的token
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            email = data.get('email')
            user_id = data.get('user_id')
            try:
                user = User.objects.get(id=user_id, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user

class Address(BaseModel):
    """
    用户地址

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', related_name='province_address', on_delete=models.PROTECT, verbose_name='省')
    city = models.ForeignKey('areas.Area', related_name='city_address', on_delete=models.PROTECT, verbose_name='市')
    district = models.ForeignKey('areas.Area', related_name='district_address', on_delete=models.PROTECT, verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']