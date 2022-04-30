from dataclasses import field
from django import forms
from .models import Address, Payment, QnA, Review

class AddressForm(forms.ModelForm):

    district = forms.ChoiceField(required=True)
    area = forms.ChoiceField(required=True)
    address = forms.CharField(required=True, label="Road or House No.")
    contact_no = forms.IntegerField(required=True)
    
    class Meta:
        model = Address
        exclude = ('user',)

class PaymentForm(forms.ModelForm):
    
    sender_number = forms.IntegerField(required=True,label="Sender Number")
    transaction_id = forms.CharField(required=True,label="Transaction ID")
    
    class Meta:
        model = Payment
        fields = ('sender_number','transaction_id')



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