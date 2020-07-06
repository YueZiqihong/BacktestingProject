from .models import TradeCalendar
import datetime

tradeID = {}
def setDates():
    tradeDays = TradeCalendar.objects.all()
    for tradeDay in tradeDays:
        tradeID[tradeDay.trade_date.strftime("%Y-%m-%d")] = tradeDay.id
