from dataclasses import field
from django import forms
from .models import *

class AddressForm(forms.ModelForm):

    district = forms.ChoiceField(required=True,label="জেলা")
    area = forms.ChoiceField(required=True,label="অঞ্চল")
    address = forms.CharField(max_length=255,required=True, label="নিকটস্থ সুন্দরবন কুরিয়ার ঠিকানা")
    contact_no = forms.IntegerField(required=True, label="তোমার মোবাইল নাম্বার")

    
    class Meta:
        model = Address
        exclude = ('user',)

class PaymentForm(forms.ModelForm):
    
    sender_number = forms.IntegerField(required=True,label="Sender Number")
    transaction_id = forms.CharField(required=True,label="Transaction ID or Your Name")
    
    class Meta:
        model = Payment
        fields = ('sender_number','transaction_id')


class GuestNameForm(forms.ModelForm):
    guest_name = forms.CharField(required=True, label="নাম")
    
    class Meta:
        model = Customers
        exclude = ('user', 'name', 'contact_no', 'email', 'store_credit',
        'device')
    

# Review Form

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment', 'ratings')




# QA Form
class QnAForm(forms.ModelForm):
    class Meta:
        model = QnA
        fields = ('question',)


# Exchange Form

class DatePickerInput(forms.DateInput):
        input_type = 'date'
        

class ExchangeForm(forms.ModelForm):
    
    class Meta:
        model = Exchange
        fields = ('full_name', 'mobile_no', 'number_of_books', 'sending_date', 'comment')
    

        widgets = {
            'sending_date' : DatePickerInput(),
            
        }

        labels = {
            "number_of_books" : "How Many Books?",
            "comment" : "Comment (If Any)"
        }

        

       