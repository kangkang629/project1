from rest_framework.decorators import api_view, authentication_classes
from myapp import utils
from myapp.handler import APIResponse
from myapp.models import User
from myapp.utils import md5value
from myapp.auth.authentication import TokenAuthtication
from myapp.serializers import UserSerializer, LoginLogSerializer


def make_login_log(request):
    try:
        username = request.data['username']
        data = {
            "username": username,
            "ip": utils.get_ip(request),
            "ua": utils.get_ua(request)
        }
        serializer = LoginLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
    except Exception as e:
        print(e)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = utils.md5value(request.data['password'])

        users = User.objects.filter(username=username, password=password)
        if len(users) > 0:
            user = users[0]

            if user.role in ['2', '3']:
                return APIResponse(code=1, msg='该帐号为非后台管理员帐号')

            data = {
                'username': username,
                'password': password,
                'admin_token': md5value(username)  # 生成令牌
            }
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                make_login_log(request)
                return APIResponse(code=0, msg='登录成功', data=serializer.data)
            else:
                print(serializer.errors)

        return APIResponse(code=1, msg='用户名或密码错误')


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', None)
        notices = User.objects.filter(username__contains=keyword).order_by('-create_time')
        serializer = UserSerializer(notices, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def create(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    role = request.data.get('role', None)
    nicke_name = request.data.get('nicke_name', None)
    email = request.data.get('email', None)
    mobile = request.data.get('mobile', None)
    status = request.data.get('status', None)
    if not username or not password:
        return APIResponse(code=1, msg='用户名或密码不能为空')
    users = User.objects.filter(username=username)
    if len(users) > 0:
        return APIResponse(code=1, msg='该用户名已存在')

    data = {
        'username': username,
        'password': password,
        'role': role,  # 角色2
        'nicke_name': nicke_name,
        'email': email,
        'mobile': mobile,
        'status': status
    }
    data.update({'password': utils.md5value(request.data['password'])})
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='创建失败')


@api_view(['GET'])
def info(request):
    if request.method == 'GET':
        pk = request.GET.get('id', -1)
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def update(request):
    try:
        pk = request.GET.get('id', -1)
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    data = request.data.copy()
    if 'username' in data.keys():
        del data['username']
    if 'password' in data.keys():
        del data['password']
    if 'role' in data.keys():
        del data['role']
    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def updatePwd(request):
    try:
        pk = request.GET.get('id', -1)
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    password = request.data.get('password', None)
    newPassword1 = request.data.get('newPassword1', None)
    newPassword2 = request.data.get('newPassword2', None)

    if not password or not newPassword1 or not newPassword2:
        return APIResponse(code=1, msg='不能为空')

    if user.password != utils.md5value(password):
        return APIResponse(code=1, msg='原密码不正确')

    if newPassword1 != newPassword2:
        return APIResponse(code=1, msg='两次密码不一致')

    data = request.data.copy()
    data.update({'password': utils.md5value(newPassword1)})
    serializer = UserSerializer(user, data=data)
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
        User.objects.get(pk=pk).delete()
        return APIResponse(code=0, msg='删除成功')