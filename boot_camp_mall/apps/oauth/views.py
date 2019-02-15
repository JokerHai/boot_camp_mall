from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from boot_camp_mall.common.ActionResult import ActionResult
from boot_camp_mall.common.JwtToken import response_jwt_payload_token
from oauth.exceptions import QQAPIError
from oauth.models import OAuthQQUser
from oauth.serializers import QQAuthUserSerializer
from oauth.utils import OAuthQQ
# Create your views here.


#/oauth/qq/user/?code=<code>
class QQAuthUserView(GenericAPIView):
    #指定当前视图所使用的序列化器类
    serializer_class = QQAuthUserSerializer
    def post(self,request):
        #保存QQ登录绑定数据：
        #1.获取参数，并进行效验，(参数完整性，手机号格式，短信验证码是否正确，access_token是否有效)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        #2.保存QQ绑定的数据并生产jwt_token
        serializer.save()
        #3.返回应答，绑定成功
        return ActionResult.success(serializer.data,status.HTTP_201_CREATED)
    def get(self,request):
        #step1: 获取code并效验
        code = request.query_params.get('code')
        if code is None:
            return ActionResult.failure(status.HTTP_400_BAD_REQUEST,'缺少code参数')

        #step2: 根据code获取QQ 登录的openid
        oauth = OAuthQQ()
        try:
            #2.1通过code请求QQ服务器获取access_token
            access_token = oauth.get_access_token(code)
            #2.2通过access_token请求QQ服务器获取openid
            openid = oauth.get_openid(access_token)
        except QQAPIError:
            return ActionResult.failure(status.HTTP_503_SERVICE_UNAVAILABLE,'QQ登录异常')
        #step3: 根据openid判断是否绑定过本站点的用户
        try:
            qq_user_obj = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            #3.2如果未绑定，将openid加密并返回
            secret_openid = OAuthQQ.generate_save_user_token(openid)
            return ActionResult.success({'access_token':secret_openid})
        else:
            #返回jwt_token
            user = qq_user_obj.user
            token = response_jwt_payload_token(qq_user_obj.user)

            data = {
                'user_id':user.id,
                'username':user.username,
                'token':token
            }
            return ActionResult.success(data)
#GET /oauth/qq/authorization/?next=<登录之后访问页面地址>
class QQAuthURLView(APIView):
    def get(self, request):
        """
        获取QQ登录网址:
        1. 获取next
        2. 组织QQ登录网址和参数
        3. 返回QQ登录网址
        """
        # 1. 获取next
        next = request.query_params.get('next', '/')

        # 2. 组织QQ登录网址和参数
        oauth = OAuthQQ(state=next)
        login_url = oauth.get_login_url()
        # 3. 返回QQ登录网址
        return ActionResult.success({'login_url':login_url})