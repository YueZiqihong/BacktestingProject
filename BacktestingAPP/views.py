from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
import time

from .models import *
from BacktestingAPP import marketControl
from django.db import connection

# Create your views here.
@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", books))
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
        a = request.GET.get('a')
        b = request.GET.get('b')

        response['testdata'] = a + "ying" + b
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


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
