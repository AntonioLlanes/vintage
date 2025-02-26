# myapp/forms.py
from django import forms
from .models import Product, ProductImage
from django.forms.widgets import FileInput

from django import forms
from django.forms.widgets import FileInput
from .models import Product, ProductImage

# ✅ Custom widget to allow multiple file uploads
from django import forms
from .models import Product, ProductImage


# ✅ Custom widget to allow multiple file uploads
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # ✅ Enable multiple file selection

    def value_from_datadict(self, data, files, name):
        """ Returns a list of uploaded files """
        if files:
            return files.getlist(name)  # ✅ Get multiple files as a list
        return None


    def value_from_datadict(self, data, files, name):
        """ Returns a list of uploaded files """
        if name in files:
            return files.getlist(name)  # ✅ Get multiple files as a list
        return None

class ProductForm(forms.ModelForm):
    images = forms.FileField(widget=MultipleFileInput(attrs={'multiple': True}), required=False)  # ✅ Use custom widget

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'size', 'category', 'brand']

    def save(self, commit=True):
        """ Save product and upload multiple images """
        product = super().save(commit=commit)  # Save product first
        images = self.files.getlist('images')
        if images:
            for image in images:
                ProductImage.objects.create(product=product, image=image)  # Save each image
        return product
