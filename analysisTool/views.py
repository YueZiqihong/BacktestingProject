from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import *
import datetime
from django.db.models import Sum
from django.db.models import F

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


# Create your views here.
@require_http_methods(["GET"])
def getPortfolioData(request):
    response = {}
    try:
        books = request.GET.getlist("books")
        response["test"] = books
        # books = ["jx","yz"]
        startDate = datetime.datetime.strptime(request.GET.get("startDate"), '%Y-%m-%d').date()
        endDate = datetime.datetime.strptime(request.GET.get("endDate"), '%Y-%m-%d').date()
        response["s"] = startDate
        response["e"] = endDate

        response["dates"] = json.dumps(list(TradeCalendar.objects.filter(
        trade_date__range=(startDate,endDate))
        .values_list("trade_date",flat=True)
        .order_by("trade_date")
        ), cls=DateEncoder)

        data = {}
        for book in books:
            positions = (Position.objects.filter(
            trade_day_id__trade_date__range=(startDate,endDate),
            book = book
            )
            .annotate(Date=F("trade_day_id__trade_date"))
            .values("Date")
            .order_by("trade_day_id")
            .annotate(Value=Sum("value")))
            data[book] = json.dumps(list(positions), cls=DateEncoder)
        response["performance"] = data
        # 这种写法返回的数据在前端会被字符串括起来，需要eval
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def getMarketData(request):
    response = {}
    try:
        ticker = request.GET.get("ticker")
        startDate = datetime.datetime.strptime(request.GET.get("startDate"), '%Y-%m-%d').date()
        endDate = datetime.datetime.strptime(request.GET.get("endDate"), '%Y-%m-%d').date()

        marketData = (Market.objects.filter(
        trade_day_id__trade_date__range=(startDate,endDate),
        ts_code = ticker,
        )
        .annotate(
        Date = F("trade_day_id__trade_date"),
        Volume = F("vol"),
        )
        .values("Date","open","close","high","low","Volume")
        .order_by("trade_day_id"))

        response['marketData'] = json.dumps(list(marketData), cls=DateEncoder)
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def getTransactionData(request):
    response = {}
    try:
        book = request.GET.get("book")
        startDate = datetime.datetime.strptime(request.GET.get("startDate"), '%Y-%m-%d').date()
        endDate = datetime.datetime.strptime(request.GET.get("endDate"), '%Y-%m-%d').date()
        ticker = request.GET.get("ticker")

        positions = (Position.objects.filter(
        trade_day_id__trade_date__range=(startDate,endDate),
        book = book,
        ts_code = ticker,
        )
        # .values("trade_day_id__trade_date","book","position","value","return_field","pct_return")
        .annotate(
        Date=F('trade_day_id__trade_date'),
        Position=F('position'),
        PercentageReturn=F('pct_return')
        )
        .values('Date',"Position","PercentageReturn")
        .order_by("trade_day_id"))

        response["transactionData"] = json.dumps(list(positions), cls=DateEncoder)
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
