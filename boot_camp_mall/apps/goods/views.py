from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from goods.models import SKU
from goods.serializers import SKUSerializer
from rest_framework.filters import OrderingFilter, SearchFilter


# GET /categories/(?P<category_id>\d+)/skus/
class SKUListView(ListAPIView):

    serializer_class = SKUSerializer

    # 搜索过滤器和排序过滤器
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    #搜索的是is_hot字段的内容
    filter_fields = ('is_hot',)
    #排序功能根据以下的四个字段排序
    ordering_fields = ('create_time', 'price', 'sales')
    #搜索查询
    search_fields = ('name',)
    #默认排序的字段
    ordering = ('-create_time',) #指定默认排序

    def get_queryset(self):
        return SKU.objects.filter(category_id=self.kwargs['category_id'],is_launched=True)