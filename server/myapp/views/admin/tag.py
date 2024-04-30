from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Tag
from myapp.serializers import TagSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        tags = Tag.objects.all().order_by('-create_time')
        serializer = TagSerializer(tags, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def create(request):
    title = request.data.get('title', None)
    if not title:
        return APIResponse(code=1, msg='title不能为空')

    data = {
        'title': title
    }
    serializer = TagSerializer(data=data)
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
            user = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return APIResponse(code=1, msg='对象不存在')

        title = request.data.get('title', None)

        if title is None:
            return APIResponse(code=1, msg='标题不能为空')

        data = request.data.copy()
        serializer = TagSerializer(user, data=data)
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
            Tag.objects.get(pk=i).delete()
        return APIResponse(code=0, msg='删除成功')