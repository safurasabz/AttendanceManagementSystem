from django.contrib import admin
from .models import Excel, Staff, Log, Permissions

# Register your models here.
admin.site.register(Excel)
admin.site.register(Staff)
admin.site.register(Log)
admin.site.register(Permissions)

