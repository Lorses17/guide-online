from django import forms

class SearchForm(forms.Form):
    serial_number = forms.CharField(
        max_length=50,
        label="Введите серийный номер",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: A1B2C3D4E5F6'
        })
    )

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Введите ваше сообщение'
        })
    )

class ProductTypeForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Название типа техники",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: Смартфоны'
        })
    )
    description = forms.CharField(
        label="Описание",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Добавьте описание типа техники'
        })
    )

class ProductModelForm(forms.Form):
    product_type = forms.ChoiceField(
        label="Тип техники",
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        max_length=100,
        label="Название модели",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: iPhone 15 Pro'
        })
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import ProductType
        self.fields['product_type'].choices = [
            (ptype.id, ptype.name) for ptype in ProductType.objects.all()
        ]