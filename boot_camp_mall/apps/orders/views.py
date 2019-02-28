from decimal import Decimal
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from orders.serializers import OrderSettlementSerializer, SaveOrderSerializer


class OrderSettlementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        """
            获取
        """
        user = request.user

        # 从购物车中获取用户勾选要结算的商品信息
        redis_conn = get_redis_connection('cart')
        redis_cart = redis_conn.hgetall('cart_%s' % user.id)
        cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)

        cart = {}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(redis_cart[sku_id])

        # 查询商品信息
        skus = SKU.objects.filter(id__in=cart.keys())
        for sku in skus:
            sku.count = cart[sku.id]

        # 运费
        freight = Decimal('10.00')

        serializer = OrderSettlementSerializer({'freight': freight, 'skus': skus})
        return Response(serializer.data)


class SaveOrderView(CreateAPIView):
    """
    保存订单
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SaveOrderSerializer

    def post(self, request):
        """
        订单数据保存:
        1. 获取参数并进行校验(参数完整性，address是否存在，pay_method是否合法)
        2. 保存订单的数据
        3. 返回应答，订单创建成功
        """
        # 1. 获取参数并进行校验(参数完整性，address是否存在，pay_method是否合法)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 保存订单的数据(create)
        serializer.save()

        # 3. 返回应答，订单创建成功
        return Response(serializer.data, status=status.HTTP_201_CREATED)