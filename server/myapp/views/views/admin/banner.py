from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import Banner
from myapp.serializers import BannerSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        notices = Banner.objects.all().order_by('-create_time')
        serializer = BannerSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)