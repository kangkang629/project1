from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Record
from myapp.serializers import RecordSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        notices = Record.objects.all().order_by('-create_time')
        serializer = RecordSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)