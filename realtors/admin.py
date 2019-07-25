from django.contrib import admin
from .models import Realtor
class RealtorAdmin(admin.ModelAdmin):
	list_display_links=('id', 'name')
	list_display = ('id','name','is_mvp','email','hire_date')
	search_fields=('name',)
	list_editable=('is_mvp',)
	list_per_page=25
# Register your models here.
admin.site.register(Realtor, RealtorAdmin)