from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Order
from myapp.serializers import OrderSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        notices = Order.objects.all().order_by('-order_time')
        serializer = OrderSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def delete(request):
    if request.method == 'POST':
        pk = request.GET.get('ids', -1)
        pk = pk.split(',')
        for i in pk:
            Order.objects.get(pk=i).delete()
        return APIResponse(code=0, msg='删除成功')


@api_view(['POST'])
def cancel_order(request):
    if request.method == 'POST':
        pk = request.GET.get('id', -1)
        obj = Order.objects.get(pk=pk)
        obj.status = 0
        obj.save()
    return APIResponse(code=0, msg='取消成功')