# -*- coding: utf-8 -*-
#自定义FastDFS上传类
# @Author  : joker
# @Date    : 2019-02-24
from django.conf import settings
from  django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from fdfs_client.client import Fdfs_client

@deconstructible
class FastDfsStorage(Storage):
    """
    FastDFS文件存储类
    """

    def __init__(self,client_conf = None,base_url=None):

        if client_conf is None:

            client_conf = settings.FASTDFS_CLIENT_CONF

        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_NGINX_URL

        self.base_url = base_url

    def _save(self,name,content):

        """
        上传图片
        :param name: 上传文件的名称
        :param content: 包含上传文件内容FILE对象，可以通过content.read()获取上传文件的内容
        """

        client = Fdfs_client(self.client_conf)

        result = client.upload_by_buffer(content.read())

        if result.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FastDFS失败')

        #获取文件id
        file_id = result.get('Remote file_id')

        return file_id

    def exists(self,name):
        """
        判断文件是否存在，FastDFS可以自行解决文件的重名问题
        所以此处返回False，告诉Django上传的都是新文件
        :param name: 文件名
        :return:
        """
        return False


    def url(self, name):
        """
        返回文件的完整URL路径
        :param name: 数据库中保存的文件名
        :return:完整的URL
        """
        return self.base_url+name