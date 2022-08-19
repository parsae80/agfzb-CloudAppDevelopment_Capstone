from django.contrib import admin
# from .models import related models
from .models import  CarMake, CarModel
# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['carmake','dealer_id', 'modelname', 'carType','year']
    list_filter = ['carType']
    search_fields = ['modelname', 'carType']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')
    list_filter = ['name','description']
    search_fields = ['name', 'description']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
