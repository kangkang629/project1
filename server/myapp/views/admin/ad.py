from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Ad
from myapp.serializers import AdSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        notices = Ad.objects.all().order_by('-create_time')
        serializer = AdSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def create(request):
    image = request.data.get('image', None)
    link = request.data.get('link', None)
    if not image:
        return APIResponse(code=1, msg='图片不能为空')
    if not link:
        return APIResponse(code=1, msg='链接不能为空')

    data = {
        'image': image,
        'link': link
    }
    serializer = AdSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
def update(request):
    if request.method == 'POST':
        try:
            pk = request.GET.get('id', -1)
            user = Ad.objects.get(pk=pk)
        except Ad.DoesNotExist:
            return APIResponse(code=1, msg='对象不存在')

        link = request.data.get('link', None)
        if not link:
            return APIResponse(code=1, msg='链接不能为空')

        data = request.data.copy()
        serializer = AdSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='更新成功', data=serializer.data)
        else:
            print(serializer.errors)

        return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
def delete(request):
    if request.method == 'POST':
        pk = request.GET.get('ids', -1)
        pk = pk.split(',')
        for i in pk:
            Ad.objects.get(pk=i).delete()
        return APIResponse(code=0, msg='删除成功')