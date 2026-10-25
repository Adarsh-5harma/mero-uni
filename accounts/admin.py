from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class MeroUniUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Academic profile', {'fields': ('role', 'current_semester')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Academic profile', {'fields': ('email', 'role', 'current_semester')}),
    )
    list_display = UserAdmin.list_display + ('role', 'current_semester')
