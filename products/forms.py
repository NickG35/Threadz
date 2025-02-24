from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_by', 'creation_time']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'price': forms.TextInput(attrs={'placeholder': 'Enter price'}),
            'description': forms.TextInput(attrs={'placeholder': 'Enter product description'}),
            'category': forms.Select(attrs={'placeholder': 'Select a category'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.label = ''