from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.serializers import CartSerializer, CartSKUSerializer
from cart.utils import save_cart, get_cart


# url(r'cart/')
class CartView(APIView):
    def post(self, request):
        # 获取参数，并效验

        serializer = CartSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        flag = save_cart(request.user, serializer.validated_data)

        if flag:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self,request):

        sku_result = get_cart(request.user)

        serializer = CartSKUSerializer(sku_result, many=True)

        return Response(serializer.data)