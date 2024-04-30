from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import LoginLog
from myapp.serializers import LoginLogSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        notices = LoginLog.objects.all().order_by('-log_time')
        serializer = LoginLogSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)