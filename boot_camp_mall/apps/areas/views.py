from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas.models import Area
from areas.serializers import AreasSerializers, SubAreaSerializers
# Create your views here.

#视图集实现方法
class AreasViewSet(CacheResponseMixin,ReadOnlyModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return AreasSerializers
        else:
            return SubAreaSerializers
    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()
#类视图实现方法
# GET /areas/(?P<pk>\d+)/
class SubAreasView(RetrieveAPIView):
    #指定当前视图所使用的查询集
    queryset = Area.objects.all()
    #指定当前视图所使用的序列化器类
    serializer_class = SubAreaSerializers
    pass
#GET /areas
class AreasView(ListAPIView):
    #指定当前视图所使用的查询集
    queryset = Area.objects.filter(parent=None)
    #指定当前视图所使用的序列化器类
    serializer_class = AreasSerializers