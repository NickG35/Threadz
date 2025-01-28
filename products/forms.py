from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_by']
        widgets = {
            'category': forms.Select(attrs={'placeholder': 'Select a category'}),
        }