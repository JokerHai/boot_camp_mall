from django.conf import settings
from django.core.mail import send_mail
from django.test import TestCase

# Create your tests here.

class UsersTests(TestCase):

    def test_users_email_code(self):
        msg = '<a href="http://www.itcast.cn/subject/pythonzly/index.shtml" target="_blank">点击激活</a>'
        send_mail('注册激活', '', settings.EMAIL_FROM, ['smallslacker@163.com'], html_message=msg)


