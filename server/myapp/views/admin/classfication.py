from django.db import connection
from rest_framework.decorators import api_view
from myapp.models import Classification
from myapp.handler import APIResponse
from myapp.utils import dict_fetchall
from myapp.serializers import ClassificationSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        notices = Classification.objects.all().order_by('-create_time')
        serializer = ClassificationSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def create(request):
    title = request.data.get('title', None)
    en_title = request.data.get('en_title', None)
    if not title:
        return APIResponse(code=1, msg='title不能为空')

    data = {
        'title': title,
        'en_title': en_title
    }
    serializer = ClassificationSerializer(data=data)
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
            user = Classification.objects.get(pk=pk)
        except Classification.DoesNotExist:
            return APIResponse(code=1, msg='对象不存在')

        title = request.data.get('title', None)
        en_title = request.data.get('en_title', None)

        if title is None:
            return APIResponse(code=1, msg='标题不能为空')

        data = request.data.copy()
        serializer = ClassificationSerializer(user, data=data)
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
            Classification.objects.get(pk=i).delete()
        return APIResponse(code=0, msg='删除成功')