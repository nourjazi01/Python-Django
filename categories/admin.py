from django.contrib import admin
from .models import category

class categoryAdmin(admin.ModelAdmin):
    search_fields=('title',)


admin.site.register(category,categoryAdmin)
