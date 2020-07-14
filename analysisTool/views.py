from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import *
import datetime
from django.db.models import Sum
from django.db.models import F
from . import requestHandler


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        else:
            return json.JSONEncoder.default(self, obj)


@require_http_methods(["GET"])
def getPortfolioData(request):
    response = {}
    try:
        books = request.GET.getlist("books")
        response["books"] = books
        startDate = datetime.datetime.strptime(request.GET.get("startDate"), '%Y-%m-%d').date()
        endDate = datetime.datetime.strptime(request.GET.get("endDate"), '%Y-%m-%d').date()

        response["dates"] = json.dumps(list(TradeCalendar.objects.filter(
        trade_date__range=(startDate,endDate))
        .values_list("trade_date",flat=True)
        .order_by("id")
        ), cls=MyEncoder)

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
            data[book] = json.dumps(list(positions), cls=MyEncoder)
        response["performance"] = data

        data = {}
        for book in books:
            positions = (Position.objects.filter(
            trade_day_id__trade_date__range=(startDate,endDate),
            book = book
            )
            .annotate(Date=F("trade_day_id__trade_date"))
            .values_list("Date")
            .order_by("trade_day_id")
            .annotate(Value=Sum("value")))
            data[book] = json.dumps(list(positions), cls=MyEncoder)
        response["performanceTuple"] = data

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

        response['marketData'] = json.dumps(list(marketData), cls=MyEncoder)
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

        .annotate(
        Date=F('trade_day_id__trade_date'),
        Position=F('position'),
        PercentageReturn=F('pct_return')
        )
        .values('Date',"Position","PercentageReturn")
        .order_by("trade_day_id"))

        response["transactionData"] = json.dumps(list(positions), cls=MyEncoder)
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def setTransactions(request):
    response = {}
    try:
        file = request.FILES.get('file')
        tradeID = requestHandler.getDateIDs()
        skipFirstLine = True
        for line in file:
            if skipFirstLine:
                skipFirstLine = False
                Position.objects.all().delete()
                statements = []
                continue
            infomation = str(line.split()[0], encoding = "utf-8").split(",")
            value = infomation[4] if infomation[4]!="" else 0
            return_field = infomation[6] if infomation[6]!="" else 0
            pct_return = infomation[7] if infomation[7]!="" else 0
            statements.append(Position(
            book=infomation[0],
            ts_code=infomation[1],
            trade_day_id=tradeID[infomation[2]],
            position=infomation[3],
            value=value,
            wavg_cost=infomation[5],
            return_field=return_field,
            pct_return=pct_return,
            ))
        Position.objects.bulk_create(statements)

        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def getBookList(request):
    response = {}
    try:

        books = (Position.objects.all().values_list("book",flat=True).distinct()
        .order_by("book"))

        response["books"] = json.dumps(list(books), cls=MyEncoder)
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def getCurrentStockPrice(request):
    response = {}
    try:

        date = datetime.date(2020,6,1)

        priceData = (Market.objects.filter(
        trade_day_id__trade_date=(date),
        )
        .annotate(
        ticker = F("ts_code"),
        date = F("trade_day_id__trade_date"),
        volume = F("vol"),
        )
        .order_by("ticker")
        .values("ticker","date","open","close","high","low","volume"))


        response['price'] = json.dumps(list(priceData), cls=MyEncoder)
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["POST"])
def startBacktesting(request):
    response = {}
    try:
        params = {}
        params['startDate'] = datetime.datetime.strptime(request.POST.get("startDate"), '%Y-%m-%d').date().strftime('%Y%m%d')
        params['endDate'] = datetime.datetime.strptime(request.POST.get("endDate"), '%Y-%m-%d').date().strftime('%Y%m%d')
        params['stockPool'] = request.POST.getlist("stockPool")
        params['strategy'] = request.POST.get("strategy")

        response['params'] = requestHandler.simulate(params)
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
