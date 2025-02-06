from django import forms
from django.utils.timezone import now

class CheckoutForm(forms.Form):
    address = forms.CharField(
        max_length=100, 
        required=True,
        error_messages={'required': "Please enter your address."}
    )
    
    city = forms.CharField(
        max_length=50, 
        required=True,
        error_messages={'required': "Please enter your city."}
    )
    
    zip = forms.CharField(
        min_length=5,
        max_length=10,
        required=True,
        error_messages={
            'required': "Please enter your ZIP code.",
        }
    )
    
    card_number = forms.CharField(
        min_length=16,
        max_length=16,
        required=True,
        error_messages={
            'required': "Please enter your card number.",
        }
    )
    
    expiration_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'required': "Please enter the card expiration date."}
    )
    
    cvv = forms.CharField(
        min_length=3,
        max_length=4,
        required=True,
        error_messages={
            'required': "Please enter your CVV.",
        }
    )
    
    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        
        if not card_number.isdigit():
            raise forms.ValidationError("Card number must contain only numbers.")
        
        if len(card_number) != 16:
            raise forms.ValidationError("Card number must be exactly 16 digits.")
        
        return card_number

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        
        if not cvv.isdigit():
            raise forms.ValidationError("CVV must contain only numbers.")
        
        if len(cvv) < 3 or len(cvv) > 4:
            raise forms.ValidationError("CVV must be 3 to 4 digits long.")
        
        return cvv

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date < now().date():
            raise forms.ValidationError("Card expired.")
        return expiration_date

    def clean_zip(self):
        zip_code = self.cleaned_data['zip']
        
        if not zip_code.isdigit():
            raise forms.ValidationError("ZIP code must contain only numbers.")
        
        if len(zip_code) < 5 or len(zip_code) > 10:
            raise forms.ValidationError("ZIP code must be between 5 and 10 digits.")
        
        return zip_code
