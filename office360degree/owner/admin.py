from django.contrib import admin
from .models import CustomUser, Company, SBU

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(SBU)
