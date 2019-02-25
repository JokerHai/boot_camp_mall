import random
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from boot_camp_mall.common import constants
from boot_camp_mall.common.ActionResult import ActionResult
from boot_camp_mall.libs.captcha.captcha import captcha

#url(r'^image_codes/?P(<image_code_id>[\w-]+)/$',view.ImageCodeView.as_view())
from verifications.serializes import ImageCodeCheckSerializers, CheckSMSCodeSerializers


class ImageCodeView(APIView):
    def get(self,request,image_code_id):
        """
            获取图片验证码
        """
        #生成验证码图片
        name, text, image_data = captcha.generate_captcha()

        redis_conn = get_redis_connection("verify_codes")

        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        return HttpResponse(image_data, content_type="image/jpg")
#r'^sms_codes/(?P<mobile>1[3-9]\d{9})/?image_code_id=xxx&text=xxx$'
class SMSCodeView(GenericAPIView):
    serializer_class = ImageCodeCheckSerializers
    def get(self, request, mobile):
        #效验参数
        serializer = self.get_serializer(data = request.query_params)
        serializer.is_valid(raise_exception = True)
        """
            获取短信验证码
        """
        redis_conn = get_redis_connection('verify_codes')

        # 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)

        # 创建redis管道对象
        pl = redis_conn.pipeline()

        print("短信验证码:%s" % sms_code)

        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, constants.SEND_SMS_TEMP_ID)
        # 一次执行redis管道的所有命令
        pl.execute()

        expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        # 发出发送短信任务消息
        from celery_tasks.async_sms.tasks import send_sms_code
        send_sms_code.delay(mobile, sms_code, expires)

        return ActionResult.success()
#r'^check_codes/(?P<mobile>1[3-9]\d{9}/?sms_code=xxx)$'
class CheckSmsCodeView(GenericAPIView):
    serializer_class = CheckSMSCodeSerializers
    def get(self,request,mobile):
        #效验参数
        serializer = self.get_serializer(data = request.query_params)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data)

