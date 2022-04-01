from django.contrib import admin

# Register your models here.
from applications.product.models import *

admin.site.register(Category)
admin.site.register(Product)