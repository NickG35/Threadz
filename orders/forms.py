from django import forms
from django.utils.timezone import now
from django.core.validators import RegexValidator

US_STATE_CHOICES = [("", "Select a state")] + [
    ("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"),
    ("AR", "Arkansas"), ("CA", "California"), ("CO", "Colorado"),
    ("CT", "Connecticut"), ("DE", "Delaware"), ("FL", "Florida"),
    ("GA", "Georgia"), ("HI", "Hawaii"), ("ID", "Idaho"),
    ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"),
    ("KS", "Kansas"), ("KY", "Kentucky"), ("LA", "Louisiana"),
    ("ME", "Maine"), ("MD", "Maryland"), ("MA", "Massachusetts"),
    ("MI", "Michigan"), ("MN", "Minnesota"), ("MS", "Mississippi"),
    ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"),
    ("NV", "Nevada"), ("NH", "New Hampshire"), ("NJ", "New Jersey"),
    ("NM", "New Mexico"), ("NY", "New York"), ("NC", "North Carolina"),
    ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"),
    ("OR", "Oregon"), ("PA", "Pennsylvania"), ("RI", "Rhode Island"),
    ("SC", "South Carolina"), ("SD", "South Dakota"), ("TN", "Tennessee"),
    ("TX", "Texas"), ("UT", "Utah"), ("VT", "Vermont"),
    ("VA", "Virginia"), ("WA", "Washington"), ("WV", "West Virginia"),
    ("WI", "Wisconsin"), ("WY", "Wyoming")
]

class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z\s]+$', 'First name can only contain letters.')
        ],
    )

    last_name = forms.CharField(
        max_length=50,
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z\s]+$', 'Last name can only contain letters.')
        ],
    )

    address = forms.CharField(
        max_length=100, 
        required=True,
    )
    
    city = forms.CharField(
        max_length=50, 
        required=True,
        validators=[
            RegexValidator(r'^[a-zA-Z\s]+$', 'City name can only contain letters.')
        ],
    )

    state = forms.ChoiceField(
        choices=US_STATE_CHOICES,
        required=True,
    )
    
    zip = forms.CharField(
        min_length=5,
        max_length=10,
        required=True,
    )
    
    card_number = forms.CharField(
        min_length=16,
        max_length=16,
        required=True,
    )
    
    expiration_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    
    cvv = forms.CharField(
        min_length=3,
        max_length=4,
        required=True,
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

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

