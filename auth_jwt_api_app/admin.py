from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserModel(admin.ModelAdmin):
   list_display = ('email', 'name', 'terms_condition', 'is_admin', 'is_staff')
   
   list_filter = ('is_admin',)
   
   fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),

   )