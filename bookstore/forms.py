from django import forms
from .models import Address

class AddressForm(forms.ModelForm):

    district = forms.ChoiceField(required=True)
    upazilla = forms.ChoiceField(required=True)
    thana = forms.ChoiceField(required=True)
    address = forms.CharField(required=True, label="Road or House No.")
    contact_no = forms.IntegerField(required=True)
    
    class Meta:
        model = Address
        exclude = ('user',)