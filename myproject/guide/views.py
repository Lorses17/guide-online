from django.shortcuts import render, redirect
from .forms import SearchForm, ContactForm, ProductTypeForm, ProductModelForm
from .models import Product, ProductType, ProductModel


def search_product(request):
    form = SearchForm(request.GET or None)
    product = None
    if form.is_valid():
        serial = form.cleaned_data['serial_number']
        try:
            product = Product.objects.get(serial_number=serial)
        except Product.DoesNotExist:
            product = None
    return render(request, 'search.html', {'form': form, 'product': product})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            return render(request, 'home.html')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def add_product_type(request):
    if request.method == 'POST':
        form = ProductTypeForm(request.POST)
        if form.is_valid():
            # Сохранение нового типа техники
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            ProductType.objects.create(name=name, description=description)
            return redirect('home')
    else:
        form = ProductTypeForm()
    return render(request, 'add_product_type.html', {'form': form})

def add_product_model(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            # Сохранение новой модели техники
            product_type_id = form.cleaned_data['product_type']
            name = form.cleaned_data['name']
            specs = form.cleaned_data['specs']
            product_type = ProductType.objects.get(id=product_type_id)
            ProductModel.objects.create(product_type=product_type, name=name, specs=specs)
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = ProductModelForm()
    return render(request, 'add_product_model.html', {'form': form})
def home(request):
    return render(request, 'home.html')
def services(request):
    return render(request, 'services.html')
def about(request):
    return render(request, 'about.html')