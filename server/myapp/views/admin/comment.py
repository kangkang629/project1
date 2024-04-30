from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Comment
from myapp.serializers import CommentSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        notices = Comment.objects.all().order_by('-comment_time')
        serializer = CommentSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def delete(request):
    if request.method == 'POST':
        pk = request.GET.get('ids', -1)
        pk = pk.split(',')
        for i in pk:
            Comment.objects.get(pk=i).delete()
        return APIResponse(code=0, msg='删除成功')