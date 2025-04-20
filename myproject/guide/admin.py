from django.contrib import admin
from django import forms
from django.shortcuts import render
from .models import ProductType, ProductModel, Product, Warranty, Movement

class GenerateProductsForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="Количество товаров")

class ProductModelInline(admin.TabularInline):
    model = ProductModel
    extra = 1

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductModelInline]
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type')
    list_filter = ('product_type',)
    search_fields = ('name',)

    actions = ['generate_products']

    def generate_products(self, request, queryset):
        if 'apply' in request.POST:
            form = GenerateProductsForm(request.POST)
            if form.is_valid():
                quantity = form.cleaned_data['quantity']
                for model in queryset:
                    for _ in range(quantity):
                        Product.objects.create(model=model)
                self.message_user(request, f"Создано {quantity} товаров для выбранных моделей")
                return
        else:
            form = GenerateProductsForm()

        return render(
            request,
            'admin/generate_products.html',
            {'form': form, 'models': queryset}
        )
    generate_products.short_description = "Сгенерировать товары для выбранных моделей"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'created_at')
    search_fields = ('serial_number', 'model__name')
    list_filter = ('model__product_type',)

@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = ('product', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('product__serial_number',)

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'get_move_type_display', 'location', 'date')
    list_filter = ('move_type', 'date')
    search_fields = ('product__serial_number', 'location')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)