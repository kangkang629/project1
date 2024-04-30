from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Notice
from myapp.serializers import NoticeSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        notices = Notice.objects.all().order_by('-create_time')
        serializer = NoticeSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def create(request):
    title = request.data.get('title', None)
    content = request.data.get('content', None)
    if not title:
        return APIResponse(code=1, msg='标题不能为空')
    if not content:
        return APIResponse(code=1, msg='内容不能为空')

    data = {
        'title': title,
        'content': content
    }
    serializer = NoticeSerializer(data=data)
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
            user = Notice.objects.get(pk=pk)
        except Notice.DoesNotExist:
            return APIResponse(code=1, msg='对象不存在')

        title = request.data.get('title', None)
        content = request.data.get('content', None)

        if title is None:
            return APIResponse(code=1, msg='标题不能为空')

        if content is None:
            return APIResponse(code=1, msg='内容不能为空')

        data = request.data.copy()
        serializer = NoticeSerializer(user, data=data)
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
            Notice.objects.get(pk=i).delete()
        return APIResponse(code=0, msg='删除成功')