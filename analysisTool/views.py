from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import *
import datetime

# Create your views here.
@require_http_methods(["GET"])
def getPortfolioData(request):
    response = {}
    try:
        books = request.GET.get("book")
        startDate = datetime.datetime.strptime(request.GET.get("startDate"), '%Y-%m-%d').date()
        endDate = datetime.datetime.strptime(request.GET.get("endDate"), '%Y-%m-%d').date()
        response["s"] = startDate
        response["e"] = endDate

        response["dates"] = json.loads(serializers.serialize("json",
        TradeCalendar.objects.filter(trade_date__range=(startDate,endDate))
        ))

        # data = {}
        # for book in books:
        #     positions = Position.objects.filter()
        #     data[book] = json.loads(serializers.serialize("json", postions))
        #
        # response["data"] = data
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
