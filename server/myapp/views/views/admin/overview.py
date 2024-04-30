from rest_framework.decorators import api_view
import datetime
from myapp.handler import APIResponse
from myapp.models import Order, Thing
from myapp.serializers import OrderSerializer
import random


@api_view(['GET'])
def count(request):
    if request.method == 'GET':
        thing_count = Thing.objects.all().count()
        cur_time = datetime.datetime.now()
        day_num = cur_time.isoweekday()

        monday = (cur_time - datetime.timedelta(days=day_num))
        thing_week_count = Thing.objects.filter(create_time__range=(datetime.datetime.now(), monday)).count()
        # order_not_pay_p_count = Order.objects.filter(status=1).distinct()
        # order_payed_p_count = Order.objects.filter(status=2).distinct()
        order_payed_count = Order.objects.filter(status=2).count()
        # order_cancel_p_count = Order.objects.filter(status=0).distinct()
        order_not_pay_count = Order.objects.filter(status=1).count()
        order_cancel_count = Order.objects.filter(status=0).count()
        current_date = datetime.date.today()
        previous_days = [current_date - datetime.timedelta(days=i) for i in range(1, 8)]
        visit_day = []
        for day in previous_days:
           visit_day.append({"day": day, "uv": random.randint(0, 100), "pv": random.randint(0, 100)})
        data = {
            'thing_count': thing_count,
            'order_not_pay_p_count': 1,
            'order_payed_p_count': 0,
            'order_cancel_p_count': 0,
            'thing_week_count': thing_week_count,
            'order_payed_count': order_payed_count,
            'order_not_pay_count': order_not_pay_count,
            'order_cancel_count': order_cancel_count,
            "order_rank_data": [
                {
                    "thing_id": 39,
                    "title": "笔记本电脑",
                    "count": 48
                },
                {
                    "thing_id": 25,
                    "title": "算法精粹：经典计算机科学问题的",
                    "count": 11
                },
                {
                    "thing_id": 38,
                    "title": "测试商品12",
                    "count": 9
                },
                {
                    "thing_id": 24,
                    "title": "C++多线程编程实战",
                    "count": 6
                },
                {
                    "thing_id": 35,
                    "title": "资优",
                    "count": 4
                },
                {
                    "thing_id": 20,
                    "title": "硅谷之火：个人计算机的诞生与衰落（第3版）（图灵图书）",
                    "count": 3
                },
                {
                    "thing_id": 36,
                    "title": "福柯传",
                    "count": 2
                },
                {
                    "thing_id": 37,
                    "title": "汽车配件223",
                    "count": 2
                },
                {
                    "thing_id": 29,
                    "title": "test_thing",
                    "count": 2
                },
                {
                    "thing_id": 17,
                    "title": "SQL入门经典（第5版）（异步图书） (计算机编程入门经典系列 31)",
                    "count": 2
                },
                {
                    "thing_id": 18,
                    "title": "TCP/IP入门经典（第5版）（异步图书） (计算机编程入门经典系列 33)",
                    "count": 2
                },
                {
                    "thing_id": 19,
                    "title": "像计算机科学家一样思考Python（第2版）（异步图书）",
                    "count": 1
                },
                {
                    "thing_id": 21,
                    "title": "SAP从入门到精通（异步图书） (计算机行业应用软件系列)",
                    "count": 1
                }
            ],
            "classification_rank_data": [
                {
                    "title": "人文社科",
                    "count": 9
                },
                {
                    "title": "漫画",
                    "count": 3
                },
                {
                    "title": "家具",
                    "count": 1
                },
                {
                    "title": "计算机",
                    "count": 1
                }
            ],
            "visit_data": visit_day
        }
        return APIResponse(code=0, msg='查询成功', data=data)