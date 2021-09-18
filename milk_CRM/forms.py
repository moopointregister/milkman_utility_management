from django import forms
from django.db import models
from django.db.models import fields
from .models import Customersdata, Milk_transaction, Payment_transact


class Customersform(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                              
                "class": "form-control"
            }
        ))
    class Meta:
        model = Customersdata
        fields = (
            'name',
        )

class Load_rate(forms.ModelForm): 
    class Meta:
        model = Milk_transaction
        fields = (
            'customer','rates','quantity','paid',
        )



        widgets = {
                'customer':forms.Select(attrs={'class':'form-control', 'required':'true'}),
                'rates' : forms.NumberInput(attrs={'class':'form-control', 'required':'true'}),
                'quantity':forms.NumberInput(attrs={'class':'form-control', 'required':'true'}),
                'paid' : forms.CheckboxInput(attrs={'class':'form-control'}),
                
                
            }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment_transact
        fields = (
            'customer','payment_amount'
        )
        
        widgets = {
                'customer':forms.Select(attrs={'class':'form-control'}),
                'payment_amount' : forms.NumberInput(attrs={'class':'form-control'}),
        }


