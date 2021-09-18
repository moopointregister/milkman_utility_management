from milk_CRM.forms import Load_rate
from django.contrib import admin
from .models import Customersdata,Customer_sale_data,Customer_relation_data, Milk_transaction, Payment_transact

admin.site.register(Customersdata)
admin.site.register(Customer_sale_data)
admin.site.register(Customer_relation_data)
admin.site.register(Milk_transaction)
admin.site.register(Payment_transact)


# Register your models here.
