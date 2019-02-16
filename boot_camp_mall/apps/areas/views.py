from rest_framework.generics import ListAPIView, RetrieveAPIView
from areas.models import Area
from areas.serializers import AreasSerializers, SubAreaSerializers


# Create your views here.

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
    queryset = Area.objects.filter(parent= None)
    #指定当前视图所使用的序列化器类
    serializer_class = AreasSerializers