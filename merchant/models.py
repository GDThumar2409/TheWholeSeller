from django.db import models

# Create your models here.
class Tyres(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length = 255)
    size = models.CharField(max_length = 255)
    amount = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('type', 'size')

class TyreTypes(models.Model):
    type_name = models.CharField(max_length = 255,primary_key=True)

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 255)
    password = models.CharField(max_length=255,default='')
    ordercount = models.IntegerField()
    orderamount_received = models.FloatField()
    orderamount_remaining = models.FloatField()

    class Meta:
        unique_together = ('email', 'phone')

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length = 255)
    Client = models.ForeignKey(Client, on_delete=models.CASCADE,null=True)
    order_amount = models.FloatField()
    amount_paid = models.FloatField(default=0.0)
    order_date = models.DateField(default='2022-11-23')
    order_type = models.CharField(max_length = 255,default='')

class order_items(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    amount = models.FloatField()
    item = models.ForeignKey(Tyres,on_delete=models.CASCADE,null=True)


