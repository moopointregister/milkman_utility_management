from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey, ForeignObject, OneToOneField

# Create your models here.

class Customersdata(models.Model):
    name = models.CharField(max_length=25,unique=True)
    # rates = models.IntegerField(blank=True,null=True)
    unpaid_amount = models.IntegerField(default=0,auto_created=True)
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


    def save(self, force_insert=False, force_update=False):
        is_new = self.id is None
        super(Customersdata, self).save(force_insert, force_update)
        if is_new:
            Customer_relation_data.objects.create(cust_id=self)
            Customer_sale_data.objects.create(cust_id=self)

class Customer_relation_data(models.Model):
    cust_id = ForeignKey(Customersdata,on_delete=models.CASCADE)
    
    end_date = models.DateField(blank=True,null=True)

class Customer_sale_data(models.Model):
    cust_id = ForeignKey(Customersdata,on_delete=models.CASCADE)
    total_quantity = models.IntegerField(blank=True,null=True,default=0)
    total_value = models.IntegerField(blank=True,null=True,default=0)
    total_paid_amount = models.IntegerField(blank=True,null=True,default=0)
    unpaid_amount = models.IntegerField(default=0)

class Milk_transaction(models.Model):
    cust_id = ForeignKey(Customer_sale_data,default=None,on_delete=models.CASCADE)
    customer = models.CharField(max_length = 20,blank=True,null=True)
    rates = models.IntegerField(default=50)
    transaction_time = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    paid= models.BooleanField(default=False)
    value = models.IntegerField(blank=True,null=True)

class Payment_transact(models.Model):
    cust_id = ForeignKey(Customer_sale_data,default=None,on_delete=models.CASCADE)
    customer = models.CharField(max_length = 20,null=True,blank=True)
    payment_amount = models.IntegerField(null=True,blank=True)
    payment_time = models.DateTimeField(auto_now_add=True)