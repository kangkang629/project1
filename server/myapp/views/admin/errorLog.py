from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import ErrorLog
from myapp.serializers import ErrorLogSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', "")
        notices = ErrorLog.objects.filter(content__icontains=keyword).order_by('-log_time')
        serializer = ErrorLogSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)