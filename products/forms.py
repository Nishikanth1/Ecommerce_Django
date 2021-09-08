from django import forms
from django.core.exceptions import ValidationError
from .models import  Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','description','image','price','image','category','slug','in_stock',
                  'is_active','created_by']


    # def clean(self):
    #     cleaned_data = super.clean()
    #     title = cleaned_data.get('title')
    #     price = cleaned_data.get('price')
    #     if title and len(title) > 10:
    #         raise ValidationError("title cannot be more than 10 chars")

    def clean_title(self):
        print("in clean_title")
        title = self.cleaned_data.get('title')
        if title and len(title) > 10:
            raise ValidationError("title cannot be more than 10 chars")
        print("retunring title")
        return title
