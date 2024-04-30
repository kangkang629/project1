from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Thing
from myapp.serializers import ThingSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', "")
        notices = Thing.objects.filter(title__contains=keyword).order_by('-create_time')
        serializer = ThingSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def create(request):
    title = request.data.get('title', None)
    classification = request.data.get('classification', None)
    price = request.data.get('price', None)
    repertory = request.data.get('repertory', None)
    status = request.data.get('status', None)
    tag = request.data.get('tag', None)
    cover = request.data.get('cover', None)
    description = request.data.get('description', None)
    if tag is not None:
        tag = list(tag)
    if not title:
        return APIResponse(code=1, msg='名称不能为空')
    if not classification:
        return APIResponse(code=1, msg='分类不能为空')
    if not price:
        return APIResponse(code=1, msg='价格不能为空')
    if not repertory:
        return APIResponse(code=1, msg='库存不能为空')
    if not status:
        return APIResponse(code=1, msg='状态不能为空')

    data = {
        'title': title,
        'classification': classification,
        'price': price,
        'repertory': repertory,
        'status': status,
        'tag': tag,
        'cover': cover,
        'description': description
    }
    serializer = ThingSerializer(data=data)
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
            user = Thing.objects.get(pk=pk)
        except Thing.DoesNotExist:
            return APIResponse(code=1, msg='对象不存在')

        title = request.data.get('title', None)
        classification = request.data.get('classification', None)
        price = request.data.get('price', None)
        repertory = request.data.get('repertory', None)
        status = request.data.get('status', None)
        tag = request.data.get('tag', None)
        cover = request.data.get('cover', None)
        description = request.data.get('description', None)
        if tag is not None:
            tag = list(tag)
        if not title:
            return APIResponse(code=1, msg='名称不能为空')
        if not classification:
            return APIResponse(code=1, msg='分类不能为空')
        if not price:
            return APIResponse(code=1, msg='价格不能为空')
        if not repertory:
            return APIResponse(code=1, msg='库存不能为空')
        if not status:
            return APIResponse(code=1, msg='状态不能为空')

        data = request.data.copy()
        serializer = ThingSerializer(user, data=data)
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
            Thing.objects.get(pk=i).delete()
        return APIResponse(code=0, msg='删除成功')