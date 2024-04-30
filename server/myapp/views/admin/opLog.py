from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import OpLog
from myapp.serializers import OpLogSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        notices = OpLog.objects.all().order_by('-re_time')
        serializer = OpLogSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)