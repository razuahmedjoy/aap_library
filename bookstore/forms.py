from django import forms
from .models import Address, Payment

class AddressForm(forms.ModelForm):

    district = forms.ChoiceField(required=True)
    upazilla = forms.ChoiceField(required=True)
    thana = forms.ChoiceField(required=True)
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