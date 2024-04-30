# Create your views here.
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Cart, Thing, User
from myapp.serializers import CartSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        userId = request.GET.get('userId', -1)

        if userId != -1:
            carts = Cart.objects.filter(user=userId, status=1).order_by('-id')
            serializer = CartSerializer(carts, many=True)
            for i in serializer.data:
                thing_id = i["thing"]
                thing_obj = Thing.objects.filter(id=thing_id).values('title', 'cover')
                i["title"] = thing_obj[0]["title"]
                i["cover"] = thing_obj[0]["cover"]
            return APIResponse(code=0, msg='查询成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='userId不能为空')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def create(request):
    thing_id = request.GET.get('thingId', None)
    price = request.GET.get('price', None)
    user_id = request.GET.get('userId', None)

    if thing_id is None or price is None or user_id is None:
        return APIResponse(code=1, msg='不能为空')
    if Cart.objects.filter(status=1, thing_id=thing_id, user_id=user_id):
        return APIResponse(code=1, msg='购物车里已经有此商品了')
    Cart.objects.create(number=1, price=price, status=1, thing_id=thing_id, user_id=user_id)
    return APIResponse(code=0, msg='创建成功')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def update(request):

    try:
        pk = request.GET.get('id', -1)
        addresses = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    user = request.data['user']
    default = request.data['default']

    if default:
        # 其他置为false
        Cart.objects.filter(user=user).update(default=False)

    serializer = CartSerializer(addresses, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        utils.log_error(request, '参数错误')

    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def delete(request):
    try:
        ids = request.GET.get('cart_id')
        Cart.objects.filter(id=ids).delete()
    except Cart.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    return APIResponse(code=0, msg='删除成功')