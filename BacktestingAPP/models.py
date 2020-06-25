from django.db import models
# Create your models here.

class Book(models.Model):
    book_name = models.CharField(max_length=64)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.book_name

# new stuff ,testMarket start=====

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Hushen300Component(models.Model):
    index_code = models.TextField(blank=True, null=True)
    con_code = models.TextField(blank=True, null=True)
    trade_date = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Hushen300component'


class LatestFactor(models.Model):
    ts_code = models.TextField(blank=True, null=True)
    trade_date = models.TextField(blank=True, null=True)
    adj_factor = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'latest_factor'


class Marketinfo(models.Model):
    ts_code = models.CharField(max_length=64)
    trade_date = models.DateField()
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    vol = models.FloatField(blank=True, null=True)
    pct_chg = models.FloatField(blank=True, null=True)
    adj_factor = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marketinfo'


class TradeCal(models.Model):
    exchange = models.CharField(max_length=64, blank=True, null=True)
    trade_date = models.DateField(blank=True, null=True)
    is_open = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trade_cal'


# ====testMarket End, 20200start=====

class BackwardMarket(models.Model):
    ts_code = models.TextField(blank=True, null=True)
    trade_date = models.DateField(db_index=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    vol = models.FloatField(blank=True, null=True)
    pct_chg = models.FloatField(blank=True, null=True)


class ForwardMarket(models.Model):
    ts_code = models.TextField(blank=True, null=True)
    trade_date = models.DateField(db_index=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    vol = models.FloatField(blank=True, null=True)
    pct_chg = models.FloatField(blank=True, null=True)



class Marketnow(models.Model):
    ts_code = models.TextField(blank=True, null=True)
    trade_date = models.DateField(db_index=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    vol = models.FloatField(blank=True, null=True)
    pct_chg = models.FloatField(blank=True, null=True)


class TradeCalendar(models.Model):
    trade_date = models.DateField(db_index=True)

# ==20200 end, atest start===


class CurrentPosition(models.Model):
    book = models.TextField(blank=True, null=True)
    ts_code = models.TextField(blank=True, null=True)
    position = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    wavg_cost = models.FloatField(blank=True, null=True)
    return_field = models.FloatField(db_column='return', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    pct_return = models.FloatField(blank=True, null=True)


class HistPosition(models.Model):
    book = models.TextField()
    ts_code = models.TextField()
    trade_date = models.DateField()
    position = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    wavg_cost = models.FloatField(blank=True, null=True)
    return_field = models.FloatField(db_column='return', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    pct_return = models.FloatField(blank=True, null=True)


class OrderBook(models.Model):
    order_id = models.AutoField(primary_key=True)
    book = models.TextField()
    trade_date = models.DateField()
    ts_code = models.TextField()
    order_type = models.TextField()
    limit_price = models.FloatField(blank=True, null=True)  # This field type is a guess.
    amount = models.FloatField(blank=True, null=True)  # This field type is a guess.
    amount_type = models.TextField()
    validity_term = models.IntegerField(blank=True, null=True)
    order_status = models.TextField()
