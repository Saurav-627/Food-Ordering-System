from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone', 'address')}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff']

admin.site.register(User, CustomUserAdmin)
