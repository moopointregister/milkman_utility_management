from django.shortcuts import render,redirect
from .forms import  Customersform, Load_rate, PaymentForm
from .models import Customer_sale_data, Customersdata,Milk_transaction, Payment_transact
from datetime import datetime, timedelta
from django.contrib import messages
import sys
from django.contrib.auth.decorators import login_required
sys.setrecursionlimit(1500)

# Create your views here.
@login_required(login_url='/admin/')
def tohome(request):
    response = redirect('home')
    return response

@login_required(login_url='/admin/')
def home(request):
    form = Load_rate()
    cust = Customersdata.objects.all()
    context = { 'form':form,'cust':cust}
    load_template      = request.path.split('/')[-1]
    context['segment'] = load_template


    if request.method=='POST':
        form = Load_rate(request.POST)
        
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity>0 and quantity<21 :
                rates =  form.cleaned_data['rates']
                if rates>40 and rates<65:
                    customer =  request.POST.get('customer1')
                    try:
                        order_customer = Customersdata.objects.get(name=customer)
                        value = quantity*rates
                        paid = form.cleaned_data['paid']
                        order_customer = Customersdata.objects.get(name=customer)
                        order_customer_sale = Customer_sale_data.objects.get(cust_id=order_customer)

                        val = form.save(commit=False)
                        val.value=value
                        val.customer = customer
                        val.cust_id = order_customer_sale
                        messages.info(request,f'''Milk entry successful: {quantity} to {customer}''')
                        val.save()
                    


                        # value update
                        order_customer_sale_update = Customer_sale_data.objects.get(cust_id=order_customer)
                        val_to_return = order_customer_sale_update.total_value + value
                        if paid:
                            tp = order_customer_sale_update.total_paid_amount + value
                            up = order_customer_sale_update.unpaid_amount
                            Customersdata.objects.filter(name=customer).update(unpaid_amount=up)
                        else:
                            tp = order_customer_sale_update.total_paid_amount
                            up = order_customer_sale_update.unpaid_amount + value
                            Customersdata.objects.filter(name=customer).update(unpaid_amount=up)
                    
                        # quantity update
                        quat = order_customer_sale_update.total_quantity + quantity

                        Customer_sale_data.objects.filter(cust_id=order_customer).update(total_value=val_to_return,total_quantity = quat,total_paid_amount=tp,unpaid_amount=up)
                        return redirect('home')
                    except Customersdata.DoesNotExist:
                        messages.error(request,'Check customer')

                        
                else:
                    messages.error(request,f'''Invalid rates {rates}''')
            else:
                messages.error(request,f'''invalid quantity {quantity}''')
        else:
            messages.error(request,'Please fill all fields correctly!!!')
        
    return render(request,'home.html',context)

def payment_section(request):
    context={}
    payform = PaymentForm()
    cust = Customersdata.objects.all()

    context = {'payform':payform,'cust':cust}
    load_template      = request.path.split('/')[-3]
    context['segment'] = load_template

    if request.method=='POST':
        payform = PaymentForm(request.POST)
        if payform.is_valid():
            amount =  payform.cleaned_data['payment_amount']
            if amount is not None and amount>0 and amount<10000:
                customer =  request.POST.get('customer1')
                try:
                    order_customer = Customersdata.objects.get(name=customer)
                    order_customer_sale = Customer_sale_data.objects.get(cust_id=order_customer)
                    wait_payform = payform.save(commit=False)
                    wait_payform.customer = customer
                    wait_payform.cust_id = order_customer_sale
                    messages.success(request,f'''Payment successful, {amount} paid by {customer}''')
                    wait_payform.save()

                    order_customer_sale_update = Customer_sale_data.objects.get(cust_id=order_customer)
                    up = order_customer_sale_update.unpaid_amount - amount
                    tp = order_customer_sale_update.total_paid_amount + amount

                    
                    
                    # quantity update
                    
                    Customer_sale_data.objects.filter(cust_id=order_customer).update(total_paid_amount=tp,unpaid_amount=up)
                    Customersdata.objects.filter(name=customer).update(unpaid_amount=up)


                    return redirect('home')
                except Customersdata.DoesNotExist:
                        messages.error(request,'Check customer')
            else:
                messages.error(request,f'''invalid amount {amount}''')
        else:
            messages.error(request,'Please fill all fields correctly!!!')
    return render(request,'payment_section.html',context)

def customers(request):
    customers = Customersdata.objects.all()
    
    
    load_template      = request.path.split('/')[-2]
    context ={'customers':customers}
    context['segment'] = load_template
    return render(request,'customers.html',context)

def transactions(request):
    time_threshold = datetime.now() - timedelta(hours=30)
    milk_trans = Milk_transaction.objects.filter(transaction_time__gt=time_threshold)
    payment_trans =  Payment_transact.objects.filter(payment_time__gt=time_threshold)

    context ={'milktrans':milk_trans,'pay':payment_trans}
    load_template      = request.path.split('/')[-2]
    context['segment'] = load_template
    return render(request,'transactions.html',context)

def create_new_customer(request):
    
    form = Customersform()
    context = {
        'form':form
    }
    load_template      = request.path.split('/')[-3]
    
    context['segment'] = load_template
    if request.method=='POST':
        form = Customersform(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            messages.success(request,f'''New customer {name} created succesfully''')
            return redirect('home')
        else:
            messages.error(request,'Customer with same name already exists, try another name or adding a prefix or suffix')
    return render(request,'new_customer.html',context)

def all_milk_transactions(request):
    # time_threshold = datetime.now() - timedelta(hours=30)
    milk_trans = Milk_transaction.objects.all()
    context ={'milktrans':milk_trans}
    if request.method=='GET':
        start = request.GET.get('start')
        end = request.GET.get('end')
        

        if start and end:
            date_1 = datetime.strptime(end, "%Y-%m-%d")
            date_1 =date_1 + timedelta(days=1)
                
            milk_trans = Milk_transaction.objects.filter(transaction_time__range = [start,date_1])
            context ={'milktrans':milk_trans,'start':start,'end':end}
            load_template      = request.path.split('/')[-3]
            context['segment'] = load_template
            return render(request,'all_milk_transactions.html',context)
        
    load_template      = request.path.split('/')[-3]
    context['segment'] = load_template
    return render(request,'all_milk_transactions.html',context)

def all_payments(request):
    # time_threshold = datetime.now() - timedelta(hours=30)
    pays = Payment_transact.objects.all()
    
    context ={'pays':pays}
    if request.method=='GET':
        start = request.GET.get('start')
        end = request.GET.get('end')
        

        if start and end:
            date_1 = datetime.strptime(end, "%Y-%m-%d")
            date_1 =date_1 + timedelta(days=1)
                
            pays = Payment_transact.objects.filter(payment_time__range = [start,date_1])
            context ={'pays':pays,'start':start,'end':end}
            load_template      = request.path.split('/')[-3]
            context['segment'] = load_template
            return render(request,'all_milk_transactions.html',context)

    load_template      = request.path.split('/')[-3]
    context['segment'] = load_template
    return render(request,'all_payments.html',context)

def profile(request,pk):
    cust_dat = Customersdata.objects.get(id=pk)
    obj = Customer_sale_data.objects.get(cust_id=cust_dat)
    milk_trans = Milk_transaction.objects.filter(customer = cust_dat.name)
    pays = Payment_transact.objects.all()

    if request.method=='GET':
        start_milk = request.GET.get('start_milk')
        end_milk = request.GET.get('end_milk')
        start_pay = request.GET.get('start_pay')
        end_pay = request.GET.get('end_pay')
        

        if start_milk and end_milk:
            date_1 = datetime.strptime(end_milk, "%Y-%m-%d")
            date_1 =date_1 + timedelta(days=1)
                
            milk_trans = Milk_transaction.objects.filter(transaction_time__range = [start_milk,date_1],customer = cust_dat.name)
            context ={'obj':obj,'cust':cust_dat,'milktrans':milk_trans,'start_milk':start_milk,'end_milk':end_milk,'pays':pays}
            load_template      = request.path.split('/')[-3]
            context['segment'] = load_template
            return render(request,'customer_profile.html',context)
        if start_pay and end_pay:
            date_2 = datetime.strptime(end_pay, "%Y-%m-%d")
            date_2 =date_2 + timedelta(days=1)
                
            pays = Payment_transact.objects.filter(payment_time__range = [start_pay,date_2],customer = cust_dat.name)
            context ={'obj':obj,'cust':cust_dat,'milktrans':milk_trans,'start_pay':start_pay,'end_pay':end_pay,'pays':pays}
            load_template      = request.path.split('/')[-3]
            context['segment'] = load_template
            return render(request,'customer_profile.html',context)

    
    context = {'obj':obj,'cust':cust_dat,'milktrans':milk_trans,'pays':pays}
    load_template      = request.path.split('/')[-3]
    context['segment'] = load_template

    return render(request,'customer_profile.html',context)