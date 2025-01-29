from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_by', 'creation_time']
        widgets = {
            'category': forms.Select(attrs={'placeholder': 'Select a category'}),
        }