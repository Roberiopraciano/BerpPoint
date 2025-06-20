from django.contrib import admin
from .models import *

class FaceColletionInline(admin.StackedInline):
    model = FaceCollection
    extra = 0

class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    inlines = (FaceColletionInline,)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Training)
admin.site.register(EmployeeRegistration)