
from .views import  all_milk_transactions, create_new_customer, payment_section, profile, customers, home,  transactions,all_payments,tohome
from django.conf.urls import url
from django.urls import path


urlpatterns = [
    url('home/payments/',payment_section,name='topayments'),
    url('home/',home,name='home'),
    

    url('customers/create_new_customer/',create_new_customer,name='newcustomer'),
    url(r'customers/(?P<pk>.*)/',profile,name='profile'),
    url('customers/',customers,name='customerss'),
    url('transactions/all_payments/',all_payments,name='allpayments'),
    url('transactions/all_milk/',all_milk_transactions,name='allmilktrans'),
    url('transactions/',transactions,name='transactions'),
    url('home/payments/',payment_section,name='topayments'),
    url('home',home,name='home'),

    path('',tohome)

]