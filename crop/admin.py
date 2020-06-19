from django.contrib import admin
from .models import Category, Types, Unit, Crop

admin.site.register(Category)
admin.site.register(Types)
admin.site.register(Unit)
admin.site.register(Crop)