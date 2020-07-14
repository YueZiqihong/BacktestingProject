from django.db import models 

class TradeCalendar(models.Model):
    trade_date = models.DateField(blank=True, null=True)

    class Meta:
        app_label = "analysisTool"


class Market(models.Model):
    ts_code = models.TextField(blank=True, null=True)
    trade_day = models.ForeignKey('TradeCalendar',on_delete=models.CASCADE)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    vol = models.FloatField(blank=True, null=True)
    pct_chg = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = "analysisTool"


class Position(models.Model):
    book = models.TextField()
    ts_code = models.TextField()
    trade_day = models.ForeignKey('TradeCalendar',on_delete=models.CASCADE)
    position = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    wavg_cost = models.FloatField(blank=True, null=True)
    return_field = models.FloatField(db_column='return', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    pct_return = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = "analysisTool"


class OrderBook(models.Model):
    order_id = models.AutoField(primary_key=True)
    book = models.TextField()
    trade_day = models.ForeignKey('TradeCalendar',on_delete=models.CASCADE)
    ts_code = models.TextField()
    order_type = models.TextField()
    limit_price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    amount_type = models.TextField()
    validity_term = models.IntegerField(blank=True, null=True)
    order_status = models.TextField()

    class Meta:
        app_label = "analysisTool"
