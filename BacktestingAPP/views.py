from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import datetime

from .models import *
from BacktestingAPP import marketControl
from django.db import connection

# Create your views here.


@require_http_methods(["GET"])
def test2(request):
    response = {}
    try:
        start = time.time()
        market = marketControl.VirtualMarket()

        # set params
        #===TBF===

        # init back,forward,(# should clear trade_calendar2, back, forward first.)
        marketControl.initializeContainer(request, market)
        # init broker book
        response["inittime"] = time.time() - start
        response["runningtime"] = market.execute()
        # end init broker book

        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

@require_http_methods(["GET"])
def test(request):
    response = {}
    try:

        # response['test'] = requestHandler.generate(request)



        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def zymInterface(request):
    response = {}
    try:
        startDate = datetime.datetime.strptime(request.GET.get("startDate"), '%Y-%m-%d').date()
        endDate = datetime.datetime.strptime(request.GET.get("endDate"), '%Y-%m-%d').date()
        strategy = "" # 可以先自己写
        stockPool = [] # 之后我处理，应该是一个列表，每一项是一个ticker
        # 利用上面几个参数 做坏事


        # 这样那样 （注意事项：如果要引入其他的包，需要在此页写import


        # 返回值：示例见下
        # 标注一下即可，最后我需要处理数据类型才能正常连接

        response['testdata'] = "ying"
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
